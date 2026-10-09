"""Learn and check real pytest, retaining unchanged PASS and deliberate-write REVIEW."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


class RecipeError(ValueError):
    """A native command or declared recipe assertion did not establish its outcome."""


def invoke(command: list[str], root: Path, name: str, expected: int) -> None:
    """Retain command, both streams and actual exit before checking expectation."""
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    try:
        result = subprocess.run(command, cwd=root, env=env, capture_output=True, timeout=60, check=False)
    except subprocess.TimeoutExpired as error:
        (root / (name + '.stdout')).write_bytes(error.stdout or b'')
        (root / (name + '.stderr')).write_bytes(error.stderr or b'')
        (root / (name + '-command.json')).write_text(json.dumps({'command': command, 'returncode': None, 'expectedReturncode': expected, 'outcome': 'timeout'}, indent=2) + '\n')
        raise
    (root / (name + '.stdout')).write_bytes(result.stdout)
    (root / (name + '.stderr')).write_bytes(result.stderr)
    receipt = {'command': command, 'returncode': result.returncode, 'expectedReturncode': expected}
    (root / (name + '-command.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    if result.returncode != expected:
        raise RecipeError(f'{name}: expected exit {expected}, got {result.returncode}; retained receipts: {root}')


def check(binary: str, python: str, root: Path, name: str, expected: int, verdict: str) -> None:
    """Assert the native structured verdict and unchanged reviewed baseline bytes."""
    command = [binary, 'check', '--baseline', str(root / 'execsurface.lock.json'), '--workspace', str(root), '--json-output', str(root / (name + '-verdict.json')), '--', python, '-m', 'pytest', '-q', '-s', '-p', 'no:cacheprovider', 'test_fixture.py']
    invoke(command, root, name, expected)
    report = json.loads((root / (name + '-verdict.json')).read_bytes())
    if report['target'] != {'exit_code': 0, 'signal': None}:
        raise RecipeError(f'{name}: pytest did not exit successfully; retained {root}')
    if report['policy']['source'] != 'builtin:review-unmatched-drift':
        raise RecipeError(f'{name}: selected built-in policy differs; retained {root}')
    if verdict == 'REVIEW' and not any(finding['change'] == 'added' and finding['effect_kind'] == 'file_write' and finding['evidence']['effect']['target']['value'] == '$WORKSPACE/drift.txt' for finding in report['findings']):
        raise RecipeError(f'{name}: deliberate file_write finding absent; retained {root}')
    if report['verdict'] != verdict.lower():
        raise RecipeError(f'{name}: expected {verdict} verdict; retained {root}')


def run(binary: Path, python: Path, output: Path) -> dict:
    """Create a fresh synthetic workspace and preserve both positive and drift evidence."""
    binary = binary.resolve(strict=True)
    # Do not resolve Python's venv symlink: that loses the selected test environment.
    python = python.absolute()
    output = output.absolute()
    output.mkdir(parents=True, exist_ok=False)
    fixture = Path(__file__).with_name('fixtures')
    for name in ('test_fixture.py', 'fixture.json'):
        shutil.copyfile(fixture / name, output / name)
    selected = {'binarySha256': hashlib.sha256(binary.read_bytes()).hexdigest(), 'pythonExecutable': str(python), 'fixtureSha256': hashlib.sha256((fixture / 'test_fixture.py').read_bytes()).hexdigest(), 'policy': 'unchanged built-in REVIEW for unmatched drift', 'privacy': 'public synthetic fixture; no environment or secret/file-content collection added'}
    (output / 'selection.json').write_text(json.dumps(selected, indent=2) + '\n')
    try:
        invoke([str(binary), '--version'], output, 'version', 0)
        if (output / 'version.stdout').read_text().strip() != 'execsurface 0.1.0-alpha.5':
            raise RecipeError('recipe requires explicitly selected ExecSurface Alpha.5')
        invoke([str(binary), 'doctor'], output, 'doctor', 0)
        command = [str(binary), 'learn', '--output', str(output / 'execsurface.lock.json'), '--label', 'python-pytest-fixture', '--workspace', str(output), '--', str(python), '-m', 'pytest', '-q', '-s', '-p', 'no:cacheprovider', 'test_fixture.py']
        invoke(command, output, 'learn', 0)
        before = (output / 'execsurface.lock.json').read_bytes()
        check(str(binary), str(python), output, 'unchanged', 0, 'PASS')
        # Only this public fixture value changes; command and pytest assertion stay the same.
        (output / 'fixture.json').write_text('{"left":2,"right":3,"write_extra":true}\n')
        check(str(binary), str(python), output, 'drift', 10, 'REVIEW')
        if (output / 'execsurface.lock.json').read_bytes() != before:
            raise RecipeError('baseline changed while checking drift')
        if (output / 'drift.txt').read_text() != 'controlled fixture drift\n':
            raise RecipeError('deliberate native write is missing')
        report = {'status': 'verified-recipe', 'unchanged': {'verdict': 'PASS', 'exit': 0}, 'drift': {'verdict': 'REVIEW', 'exit': 10}, 'baselineSha256': hashlib.sha256(before).hexdigest(), 'scope': 'same-operator Alpha.5 Python/pytest fixture; runtime drift example, not independent security validation', 'receipts': str(output)}
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        (output / 'failure.json').write_text(json.dumps({'status': 'failed', 'reason': str(error)}, indent=2) + '\n')
        raise
    (output / 'recipe-report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execsurface', type=Path, required=True)
    parser.add_argument('--python', type=Path, default=Path(sys.executable))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.execsurface, args.python, args.output), indent=2))
