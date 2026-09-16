# Contract authoring card

Use this card for high-risk, high-uncertainty, or explicitly structured runs. For clear scope the coordinator may author the contract without a separate Atlas session; the human or designated owner still owns it.

```json
{
  "schemaVersion": "0.2.0",
  "objective": "Prevent duplicate refresh-token rotation",
  "taskClass": "HIGH_RISK",
  "requiredBehaviors": [
    {
      "id": "AC-1",
      "description": "Concurrent use of one refresh token permits at most one successful rotation",
      "mandatory": true
    }
  ],
  "constraints": [
    "Existing public API behavior remains compatible",
    "Correctness holds across application instances"
  ],
  "assumptions": [
    {
      "statement": "All instances share the same durable token store",
      "ifFalse": "Cross-instance single-use enforcement cannot be guaranteed",
      "mitigation": "Escalate the storage boundary before implementation"
    }
  ],
  "verification": [
    {
      "criterion": "AC-1",
      "method": "integration",
      "requirement": "Run concurrent rotations and observe exactly one success"
    }
  ],
  "humanApprovalRequired": true
}
```

Rules:

- Describe outcomes, not code shapes; a current mechanism becomes a requirement only under an external constraint.
- Every required behavior has exactly one `verification` mapping and a unique ID; there are no extra verification IDs. Schema validation cannot check these two rules, so check them separately.
- `taskClass` is `NORMAL`, `HIGH_UNCERTAINTY`, or `HIGH_RISK`; high risk requires `humanApprovalRequired: true`.
- Omit empty `constraints`, `assumptions`, and `unknowns`. Repository facts belong in repository instructions, not in a reusable contract.
- Replacement is explicit, comes only from the owner, invalidates earlier evaluations, and does not reset the repair budget.

Validate the complete artifact with the schema shipped beside this card:

```bash
npx --yes ajv-cli@5 validate --spec=draft2020 \
  -s <skill-directory>/references/acceptance-contract.schema.json \
  -d <acceptance-contract.json>
```

When planning is blocked, do not manufacture a contract. Send this minimal result through the orchestrator escalation channel:

```json
{
  "role": "ATLAS",
  "status": "BLOCKED",
  "blockers": ["<missing decision or contradiction>"],
  "evidence": ["<repository observation that makes it blocking>"]
}
```
