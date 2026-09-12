# Implementation handoff card

For routine review, provide standalone acceptance, exact source state/diff (including untracked changes), observed commands/results, and remaining gaps. A clean commit or content identity must let the reviewer detect drift. Plain text is sufficient; a claimed PASS is not evidence.

The JSON protocol below applies only to high-risk, high-uncertainty, or explicitly structured runs. Forge receives the Acceptance Contract as an artifact, not remembered planner conversation. Preserve an active run's format and requirements.

The handoff shape is:

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

- Optional `criteriaClaimed`, `knownRisks`, and `uncertainties` can be omitted when empty. Claims are navigation metadata, not proof.
- Recompute the contract digest before work and handoff; a mismatch is a blocker.
- `revision.head` is the Git object ID. Run `python3 <skill-directory>/scripts/blackfin_checkpoint.py --repo <worktree> --json` after the final diff and gates. For `CLEAN`, require matching `head` plus empty tool `changedFiles` and omit `checkpoint`. For `DIRTY`, copy the tool's `checkpoint`, `head`, and exact `changedFiles` values into the handoff.
- Every check declares `mandatory`. READY requires at least one mandatory passing check, all mandatory gates passing, and no blockers. Mark optional diagnostics `mandatory: false` with explanatory evidence; keep failures or unrun results visible. Never omit or demote a frozen gate, or use an optional label to conceal a mandatory-criterion failure.
- Include command output and relevant environment in evidence; the coordinator verifies actual execution at this revision. Do not rerun passing suites without a change or unresolved concern.
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

Routine `NORMAL` and `TRIVIAL` work requires no JSON or checkpoint tool. This does not waive required review, checks, evidence, or approval; follow the coordinator's routing decision.
