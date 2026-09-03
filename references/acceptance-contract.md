# Acceptance Contract

The Acceptance Contract is Atlas's provider-independent description of what must be true for a Blackfin run to succeed. Forge and Vigil must be able to consume it without Atlas's conversation.

Validate contracts with [`../schemas/acceptance-contract.schema.json`](../schemas/acceptance-contract.schema.json).

## Required semantics

- `schemaVersion`: artifact format version, currently `0.1.0`.
- `objective`: one bounded outcome.
- `taskClass`: `TRIVIAL`, `NORMAL`, `HIGH_UNCERTAINTY`, or `HIGH_RISK`.
- `requiredBehaviors`: uniquely identified, observable outcomes. Mandatory items are hard gates. Each behavior ID equals exactly one `verification[].criterion`, with no extra verification IDs.
- `constraints`: compatibility, architecture, security, operational, or scope boundaries that materially restrict valid solutions.
- `assumptions`: conditions the plan relies on, the failure if false, and mitigation.
- `unknowns`: unresolved facts that do not yet block implementation. A material product decision is a blocker, not an unknown to hide.
- `verification`: criterion-to-method mappings describing evidence, not merely a command name.
- `humanApprovalRequired`: whether Vigil PASS still requires explicit human approval.

## Example

```json
{
  "schemaVersion": "0.1.0",
  "objective": "Prevent duplicate refresh-token rotation",
  "taskClass": "HIGH_RISK",
  "requiredBehaviors": [
    {
      "id": "AC-1",
      "description": "Concurrent use of one refresh token permits at most one successful rotation",
      "mandatory": true
    },
    {
      "id": "AC-2",
      "description": "A consumed refresh token cannot be reused by another application instance",
      "mandatory": true
    }
  ],
  "constraints": [
    "Existing public API behavior remains compatible",
    "Correctness holds across multiple application instances"
  ],
  "assumptions": [
    {
      "statement": "Application instances share one durable token store",
      "ifFalse": "Cross-instance single-use enforcement cannot be guaranteed",
      "mitigation": "Escalate the storage boundary before implementation"
    }
  ],
  "unknowns": [],
  "verification": [
    {
      "criterion": "AC-1",
      "method": "integration",
      "requirement": "Issue concurrent rotations for one token and observe exactly one success"
    },
    {
      "criterion": "AC-2",
      "method": "runtime",
      "requirement": "Rotate against instance A, then retry the original token against instance B"
    }
  ],
  "humanApprovalRequired": true
}
```

## Ownership

After handoff, Forge and Vigil may challenge a contradiction but may not revise the contract. Atlas or the human must issue an explicit replacement. A revised contract invalidates evaluations against the prior version.
