#!/usr/bin/env python3
"""Audit, build, commit, and push the current documentation batch to GitHub."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from datetime import datetime, timezone, timedelta


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}", flush=True)
    executable = shutil.which(cmd[0]) or cmd[0]
    subprocess.run([executable, *cmd[1:]], check=True)


def has_staged_changes() -> bool:
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    return result.returncode != 0


def main() -> None:
    tz = timezone(timedelta(hours=8))
    default_message = f"docs: publish batch update {datetime.now(tz).strftime('%Y-%m-%d %H:%M')}"
    parser = argparse.ArgumentParser(description="Publish current docs changes through GitHub Pages.")
    parser.add_argument("-m", "--message", default=default_message, help="Git commit message.")
    parser.add_argument("--skip-git", action="store_true", help="Audit and build only; do not commit or push.")
    parser.add_argument("--skip-audit", action="store_true", help="Skip docs audit.")
    args = parser.parse_args()

    if not args.skip_audit:
        run(["python3", "scripts/audit_docs.py"])
    run(["npm", "run", "build"])

    if args.skip_git:
        return

    run(["git", "add", "-A"])
    if has_staged_changes():
        run(["git", "commit", "-m", args.message])
        run(["git", "push", "origin", "master"])
    else:
        print("No git changes to commit.")


if __name__ == "__main__":
    main()
