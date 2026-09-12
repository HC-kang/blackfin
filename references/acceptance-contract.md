# Acceptance Contract

The human or designated Atlas/coordinator owns acceptance. Routine NORMAL work can use the human's observable request without a separate planner or JSON. High-risk, high-uncertainty, and explicitly structured runs use the contract below. Forge and Vigil consume it without planner conversation and cannot silently change it.

Use the [schema](../schemas/acceptance-contract.schema.json) and [authoring example](../skills/blackfin-atlas/references/contract-authoring.md).

- `schemaVersion`: `0.2.0`; reject other versions for this release.
- `objective`: one bounded outcome.
- `taskClass`: `NORMAL`, `HIGH_UNCERTAINTY`, or `HIGH_RISK`. Trivial work needs no contract.
- `requiredBehaviors`: unique observable criteria, with mandatory flags.
- `verification`: exactly one mapping per criterion, no extra IDs.
- `humanApprovalRequired`: always true for high risk.
- Optional `constraints`, `assumptions`, and `unknowns`: include only material facts. Assumptions name the failure if false and mitigation; a blocking decision must not be hidden as an unknown.

Specify WHAT/WHY, not an implementation recipe. Required changes to acceptance go to the designated owner for explicit replacement, which invalidates earlier evaluations.
