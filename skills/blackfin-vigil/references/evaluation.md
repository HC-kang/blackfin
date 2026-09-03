# Evaluation card

Prefer evidence in this order:

1. Observable runtime behavior
2. Integration or end-to-end execution
3. Deterministic tests
4. Static analysis
5. Code inspection
6. Agent explanation

Higher-order contradictory evidence wins. Forge's handoff helps locate checks but is not proof that they pass. When practical, derive at least one criterion-level observation independently from the contract instead of relying only on Forge-authored tests.

The evaluation shape is:

```json
{
  "schemaVersion": "0.1.0",
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

- Evaluate every criterion in the contract.
- Copy each criterion's `mandatory` value from the unchanged contract.
- Each evaluation `criteria[].id` equals one `requiredBehaviors[].id`; include every behavior exactly once and no extra IDs.
- `PASS` requires every mandatory criterion to pass and all mandatory evidence to be available.
- `FAIL` requires at least one failed mandatory criterion and should include reproducible evidence.
- `BLOCKED` requires at least one actionable `blockers` entry naming the missing prerequisite or contradiction.
- Evidence from another revision is stale and cannot support a PASS.
- A non-mandatory `FAIL` or `BLOCKED` does not force overall failure, but remains visible in the criterion result and summary.

For a dirty worktree, run the shipped tool before any behavior check and after writing the evaluation:

```bash
python3 <skill-directory>/scripts/blackfin_checkpoint.py \
  --repo <worktree> --verify <handoff-checkpoint>
```

Read the shipped [checkpoint protocol](checkpoint.md). A mismatch or evaluator-caused implementation change is `BLOCKED`, not a repair opportunity.

For a `CLEAN` handoff, run the same tool with `--json` before and after evaluation and require the handoff `head` to match plus `changedFiles` to remain empty. Do not add its computed checkpoint to a CLEAN artifact.

Validate the complete evaluation with the schema shipped beside this card:

```bash
npx --yes ajv-cli@5 validate --spec=draft2020 \
  -s <skill-directory>/references/evaluation.schema.json \
  -d <evaluation.json>
```

Also check that contract criterion IDs are unique and that the evaluation contains each required criterion exactly once with the unchanged `mandatory` value. If full validation cannot run, report `BLOCKED`; do not claim validation from a partial check.
