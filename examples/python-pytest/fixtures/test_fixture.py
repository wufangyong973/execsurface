"""One deterministic pytest test; optional extra write is deliberate runtime drift."""
import json
from pathlib import Path


def test_public_fixture():
    selection = json.loads(Path('fixture.json').read_text())
    assert selection['left'] + selection['right'] == 5
    if selection['write_extra']:
        Path('drift.txt').write_text('controlled fixture drift\n')
