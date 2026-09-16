# Evaluation card

A routine review returns plain-text criterion observations and `PASS`, `FAIL`, or `BLOCKED` against standalone acceptance and an identified source state, checked before and after review. The JSON and checkpoint procedures below apply to high-risk, high-uncertainty, or explicitly structured runs only, and an active structured run is never downgraded around a blocked validator.

Evidence, strongest first: observable runtime behavior, integration or end-to-end execution, deterministic tests, static analysis, code inspection, agent explanation. Higher-order contradictory evidence wins. Derive at least one criterion-level observation independently from the contract rather than only from Forge-authored tests.

```json
{
  "schemaVersion": "0.2.0",
  "role": "VIGIL",
  "decision": "FAIL",
  "acceptanceContract": {
    "location": "<path-or-artifact-id>",
    "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  },
  "revision": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "worktreeState": "DIRTY",
    "checkpoint": "blackfin-checkpoint-v1:sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
  },
  "criteria": [
    {
      "id": "AC-1",
      "mandatory": true,
      "status": "FAIL",
      "evidence": ["Two concurrent requests both returned success"],
      "reproduction": ["Start two requests against the same token", "Observe both responses"]
    }
  ],
  "checks": [
    {"command": "<command>", "result": "PASS", "evidence": "<observed output>"}
  ],
  "blockers": [],
  "summary": "Concurrent single-use behavior is not enforced."
}
```

Rules:

- Evaluate every contract criterion exactly once, with its `mandatory` value copied unchanged and no extra IDs.
- `PASS` requires every mandatory criterion passing with available evidence. `FAIL` requires at least one failed mandatory criterion with reproduction. `BLOCKED` names the missing prerequisite or contradiction in `blockers`.
- Evidence from another revision is stale and cannot support `PASS`. A non-mandatory `FAIL` or `BLOCKED` stays visible in the criterion and summary without forcing overall failure.

State checks use the shipped tool and [checkpoint protocol](checkpoint.md). For a `DIRTY` handoff, before any behavior check and again after writing the evaluation:

```bash
python3 <skill-directory>/scripts/blackfin_checkpoint.py \
  --repo <worktree> --verify <handoff-checkpoint>
```

For a `CLEAN` handoff, run the tool with `--json` at both points: `head` must match and `changedFiles` must stay empty; do not add a checkpoint to a `CLEAN` artifact. A mismatch or an evaluator-caused implementation change is `BLOCKED`, not a repair opportunity.

Validate the complete evaluation, then confirm contract criterion IDs are unique and each appears once with its `mandatory` value unchanged:

```bash
npx --yes ajv-cli@5 validate --spec=draft2020 \
  -s <skill-directory>/references/evaluation.schema.json \
  -d <evaluation.json>
```

If full validation cannot run, report `BLOCKED`; do not claim validation from a partial check.
