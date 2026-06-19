#!/usr/bin/env python3
"""Zero-dependency FineTuneKit smoke test.

This intentionally avoids pytest and training dependencies. It verifies the local
CLI can run, generate a demo project, and validate the generated data using only
Python stdlib plus this repo.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str], *, cwd: Path = REPO_ROOT) -> str:
    print("$", " ".join(args))
    completed = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return completed.stdout


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"missing expected file: {path}")


def main() -> None:
    python = sys.executable
    temp_root = Path(tempfile.mkdtemp(prefix="finetunekit-smoke-"))
    demo_dir = temp_root / "demo"

    try:
        run([python, "-m", "finetunekit", "--help"])
        run([python, "-m", "finetunekit", "doctor"])
        run([python, "-m", "finetunekit", "recommend", "--task", "support-bot", "--vram-gb", "24", "--no-detect"])
        run([python, "-m", "finetunekit", "demo", str(demo_dir)])

        expected_files = [
            "START_HERE.md",
            "README.md",
            "config.json",
            "train.py",
            "eval.py",
            "chat.py",
            "data/train.jsonl",
            "data/eval.jsonl",
            "notes/plan.md",
        ]
        for rel_path in expected_files:
            assert_exists(demo_dir / rel_path)

        config = json.loads((demo_dir / "config.json").read_text())
        if not config.get("task"):
            raise SystemExit("generated config.json is missing task")

        run([python, "-m", "finetunekit", "data", "check", str(demo_dir / "data/train.jsonl")])
        print(f"FineTuneKit smoke test passed: {demo_dir}")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    main()
