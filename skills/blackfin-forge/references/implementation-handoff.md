# Implementation handoff card

For non-trivial work, Forge receives the Acceptance Contract as an artifact, not as remembered planner conversation.

The handoff shape is:

```json
{
  "schemaVersion": "0.1.0",
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
      "result": "PASS",
      "evidence": "<concise observed output>"
    }
  ],
  "criteriaClaimed": ["AC-1"],
  "knownRisks": [],
  "uncertainties": [],
  "blockers": []
}
```

Rules:

- `criteriaClaimed` is navigation metadata, not proof.
- Recompute the contract digest before work and handoff; a mismatch is a blocker.
- `revision.head` is the Git object ID. Run `python3 <skill-directory>/scripts/blackfin_checkpoint.py --repo <worktree> --json` after the final diff and gates. For `CLEAN`, require matching `head` plus empty tool `changedFiles` and omit `checkpoint`. For `DIRTY`, copy the tool's `checkpoint`, `head`, and exact `changedFiles` values into the handoff.
- Record failed or unrun checks honestly. `READY_FOR_EVALUATION` requires every mandatory deterministic gate to pass.
- Use `BLOCKED` with at least one actionable `blockers` entry when the contract cannot be implemented without an externally owned decision.
- Inspect the complete final diff before handoff. Unrelated pre-existing changes remain visible in `changedFiles` because they are part of the state Vigil receives.

Write run artifacts under `.blackfin/` or outside the worktree, then verify that the checkpoint remains unchanged. Read the shipped [checkpoint protocol](checkpoint.md) for its boundary and exclusions.

Validate the complete handoff with the schema shipped beside this card:

```bash
npx --yes ajv-cli@5 validate --spec=draft2020 \
  -s <skill-directory>/references/generator-handoff.schema.json \
  -d <forge-handoff.json>
```

If the validator or checkpoint tool cannot run, report `BLOCKED`; do not replace either with a partial ad hoc check.

The `TRIVIAL` route does not use this handoff. It is bound directly to the exact human task, and Forge returns only changed files plus observed gate results to the orchestrator. Any need to interpret behavior, compatibility, or acceptance upgrades the route to `NORMAL` and requires Atlas.
