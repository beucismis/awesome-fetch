"""Tests for readme_to_json.py (run with: python -m pytest tests/ -q)."""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "readme_to_json.py"

SAMPLE_README = """\
# Tools

- [Tool A](https://example.com/a) - Does things `Python`
- [Tool B](https://example.com/b) - Does other things `Go`
"""


def test_no_args_prints_usage_and_exits_2():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    assert "Usage:" in proc.stderr
    assert "Traceback" not in proc.stderr


def test_valid_readme_produces_expected_json(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(SAMPLE_README, encoding="utf-8")
    out = tmp_path / "api.json"
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(readme), str(out)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["total"] == 2
    assert [tool["name"] for tool in data["tools"]] == ["Tool A", "Tool B"]
