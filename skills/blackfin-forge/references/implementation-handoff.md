# Implementation handoff card

For a routine review, hand a fresh Vigil plain text: standalone acceptance, the exact source state or diff including untracked changes, the observed commands with their results, and remaining gaps. A clean commit or a content identity must let the reviewer detect drift.

The JSON below applies only to high-risk, high-uncertainty, or explicitly structured runs. Forge receives the Acceptance Contract as an artifact, not as remembered conversation, and preserves an active run's format.

```json
{
  "schemaVersion": "0.2.0",
  "role": "FORGE",
  "status": "READY_FOR_EVALUATION",
  "acceptanceContract": {
    "location": "<path-or-artifact-id>",
    "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  },
  "revision": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "worktreeState": "DIRTY",
    "checkpoint": "blackfin-checkpoint-v1:sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
  },
  "changedFiles": ["path/to/implementation", "path/to/regression-test"],
  "checks": [
    {
      "command": "<repository test command>",
      "mandatory": true,
      "result": "PASS",
      "evidence": "<concise observed output>"
    }
  ],
  "blockers": []
}
```

Rules:

- Recompute the contract digest before work and at handoff; a mismatch is a blocker.
- `revision.head` is the Git object ID. After the final diff and gates, run `python3 <skill-directory>/scripts/blackfin_checkpoint.py --repo <worktree> --json`. `CLEAN` requires a matching `head` and empty tool `changedFiles`, with `checkpoint` omitted. `DIRTY` copies the tool's `checkpoint`, `head`, and exact `changedFiles`. See the shipped [checkpoint protocol](checkpoint.md).
- Every check declares `mandatory`. `READY_FOR_EVALUATION` requires at least one passing mandatory check, every frozen gate passing, and no blockers. Optional diagnostics are `mandatory: false` with explanatory evidence; their failures and unrun results stay visible and never cover a mandatory failure.
- Evidence is the command's observed output plus the relevant environment at this revision; the coordinator verifies actual execution.
- `BLOCKED` with at least one actionable `blockers` entry when the contract cannot be implemented without an externally owned decision.
- Inspect the complete final diff before handoff. Pre-existing unrelated changes stay visible in `changedFiles`; they are part of the state Vigil receives.
- Optional `criteriaClaimed`, `knownRisks`, and `uncertainties` may be omitted when empty; claims are navigation metadata, not proof.

Write run artifacts under `.blackfin/` or outside the worktree, then confirm the checkpoint is unchanged. Validate the complete handoff:

```bash
npx --yes ajv-cli@5 validate --spec=draft2020 \
  -s <skill-directory>/references/generator-handoff.schema.json \
  -d <forge-handoff.json>
```

If the validator or the checkpoint tool cannot run, report `BLOCKED`; a partial ad hoc check does not replace either.
