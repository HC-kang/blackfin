# Contract authoring card

Use this card for high-risk, high-uncertainty, or explicitly structured runs. Routine work can use the human's observable request without this card or a planner session. For structured acceptance, use JSON with these fields:

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

- Describe outcomes, not preferred code shapes.
- Do not turn current implementation mechanisms into requirements unless an external constraint requires them.
- Every mandatory behavior needs verification.
- An assumption states what must be true, what breaks if false, and the mitigation.
- Put repository facts in repository instructions, not in a reusable Blackfin contract template.
- For clear NORMAL work, the coordinator may author this contract without a planner worker. Only the human or designated Atlas/coordinator may explicitly replace it; Forge cannot. Replacement invalidates earlier evaluations and does not reset the repair budget.
- Omit empty constraints, assumptions, or unknowns. High-risk contracts require human approval.
- Criterion IDs must be unique. Every required behavior ID must equal exactly one `verification[].criterion` value, with no extra verification IDs.

Validate the complete artifact with the schema shipped beside this card. One tested command is:

```bash
npx --yes ajv-cli@5 validate --spec=draft2020 \
  -s <skill-directory>/references/acceptance-contract.schema.json \
  -d <acceptance-contract.json>
```

Schema validation cannot enforce cross-field ID uniqueness and mapping. Check those two rules separately.

When planning is blocked, do not manufacture a contract. Send this minimal result through the orchestrator escalation channel:

```json
{
  "role": "ATLAS",
  "status": "BLOCKED",
  "blockers": ["<missing decision or contradiction>"],
  "evidence": ["<repository observation that makes it blocking>"]
}
```
