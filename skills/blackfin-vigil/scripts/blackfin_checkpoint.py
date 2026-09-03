#!/usr/bin/env python3
"""Create or verify a Blackfin checkpoint for a dirty Git worktree."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

VERSION = "blackfin-checkpoint-v1"


def clean_git_env():
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(name, None)
    return env


def git(repo: Path, *args: str, env=None) -> bytes:
    return subprocess.run(
        ["git", "-C", os.fspath(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env or clean_git_env(),
    ).stdout


def reject_dirty_submodules(root: Path, index_env):
    for record in git(root, "ls-files", "--stage", "-z", env=index_env).split(b"\0"):
        if not record or not record.startswith(b"160000 "):
            continue
        submodule = root / os.fsdecode(record.split(b"\t", 1)[1])
        try:
            submodule_root = Path(
                os.fsdecode(git(submodule, "rev-parse", "--show-toplevel").strip())
            )
        except subprocess.CalledProcessError as error:
            raise RuntimeError(f"submodule is not initialized: {submodule}") from error
        if submodule_root.resolve() != submodule.resolve():
            raise RuntimeError(f"submodule is not initialized: {submodule}")
        if git(submodule, "status", "--porcelain", "--untracked-files=normal"):
            raise RuntimeError(f"dirty submodule is unsupported: {submodule}")


def checkpoint(repo: Path):
    root = Path(os.fsdecode(git(repo, "rev-parse", "--show-toplevel").strip()))
    head = git(root, "rev-parse", "HEAD").strip().decode("ascii")

    with tempfile.TemporaryDirectory(prefix="blackfin-checkpoint-") as directory:
        index = Path(directory) / "index"
        env = clean_git_env()
        env["GIT_INDEX_FILE"] = os.fspath(index)
        git(root, "read-tree", "HEAD", env=env)
        git(
            root,
            "add",
            "-A",
            "--",
            ".",
            ":(exclude).blackfin",
            ":(exclude).blackfin/**",
            env=env,
        )
        reject_dirty_submodules(root, env)
        tree = git(root, "write-tree", env=env).strip().decode("ascii")
        changed = git(
            root,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "--no-renames",
            "-r",
            "-z",
            "HEAD",
            tree,
        ).split(b"\0")

    digest = hashlib.sha256()
    for value in (VERSION, head, tree):
        encoded = value.encode("ascii")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)

    return {
        "checkpoint": f"{VERSION}:sha256:{digest.hexdigest()}",
        "head": head,
        "tree": tree,
        "changedFiles": [os.fsdecode(path) for path in changed if path],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--verify", metavar="CHECKPOINT")
    args = parser.parse_args()

    try:
        result = checkpoint(args.repo)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        detail = getattr(error, "stderr", b"")
        message = os.fsdecode(detail).strip() or str(error)
        print(f"blackfin checkpoint error: {message}", file=sys.stderr)
        return 2
    if args.verify and result["checkpoint"] != args.verify:
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        return 1
    print(
        json.dumps(result, ensure_ascii=True, sort_keys=True)
        if args.json
        else result["checkpoint"]
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
