# Dirty worktree checkpoint

Use this protocol only when `revision.worktreeState` is `DIRTY`. A clean revision is identified by `revision.head` alone.

Run the copy of `scripts/blackfin_checkpoint.py` shipped with the active Forge or Vigil skill:

```bash
python3 <skill-directory>/scripts/blackfin_checkpoint.py --repo <worktree> --json
python3 <skill-directory>/scripts/blackfin_checkpoint.py --repo <worktree> --verify <checkpoint>
```

The tool creates a temporary Git index from `HEAD`, stages the current tracked and non-ignored untracked state into that index, and writes a Git tree without changing the worktree's real index. It computes:

```text
blackfin-checkpoint-v1:sha256:<digest>
```

The SHA-256 input is the protocol name, `HEAD` object ID, and generated Git tree object ID in that order. Each ASCII value is preceded by its byte length as an unsigned eight-byte big-endian integer. The shipped `blackfin-checkpoint-v1` script is authoritative. Git provides the canonical handling of paths, file modes, executable bits, symlinks, deletions, and repository object format. `changedFiles` is Git's no-renames recursive name diff from `HEAD` to the generated tree.

`.blackfin/` is reserved for run artifacts and excluded from the generated tree. Ignored untracked files are also excluded. Do not put implementation source changes in either location. The checkpoint binds source state, not runtime credentials, caches, or generated environments; Forge records relevant environment prerequisites separately and Vigil establishes or verifies them independently.

Clean, initialized submodules are represented by their Gitlink commit. The tool rejects uninitialized or dirty submodules because a superproject tree cannot capture their full working state.

Forge records the returned `checkpoint`, `head`, and exact `changedFiles`. Vigil verifies the checkpoint before evaluation and again after writing its result. A mismatch is `BLOCKED`; Vigil must not repair or normalize the worktree.

For a claimed CLEAN state, Forge and Vigil still run the tool with `--json`: `head` must match and `changedFiles` must be empty, but the artifact omits `checkpoint`.
