# Handoff protocol

Every non-trivial run passes validated, standalone artifacts from one Blackfin release:

1. Human or Atlas/coordinator -> Acceptance Contract.
2. Forge -> unchanged contract reference, exact revision, diff, check evidence, and Forge handoff.
3. Fresh Vigil -> criterion-level evaluation; FAIL returns to Forge, PASS stops automation, BLOCKED escalates.

Use absolute shared paths or artifact IDs across worktrees. Run artifacts belong under reserved `.blackfin/` or outside the implementation tree. Relative uncommitted files do not follow new worktrees.

Contract references bind location and SHA-256. Recompute before use; only the human or designated contract owner may issue an explicit replacement, invalidating old evaluations. Verify unique criterion IDs, one verification mapping each, and one evaluation result each with unchanged mandatory flags.

Forge's [handoff schema](../schemas/generator-handoff.schema.json) requires passing mandatory gates for READY. All checks declare `mandatory`; optional failed/unrun diagnostics require explanatory evidence and cannot conceal a failure of mandatory acceptance. The coordinator verifies actual execution evidence as defined in [evidence policy](evidence-policy.md).

For CLEAN revisions, the checkpoint tool must report matching HEAD and no changed files; omit the checkpoint field. For DIRTY revisions, use the canonical [checkpoint](checkpoint.md). Vigil verifies state before and after evaluation, and the coordinator rechecks before acceptance. Different source state makes the result stale.

Validate [Vigil's evaluation](../schemas/evaluation.schema.json). PASS requires all mandatory criteria and their evidence; FAIL includes reproduction; BLOCKED names the missing prerequisite. Forge may not accept its own behavioral changes and Vigil may not repair implementation.

Persist artifacts and the consumed repair count. Every failed-gate or Vigil-FAIL transition back to implementation consumes one cycle, default two after the initial attempt; session reuse or interruption does not reset it. Gate failure returns command/output without fabricating a Vigil report. Contract replacement invalidates prior evidence and cannot silently reset the repair budget.

If approval is required, record PENDING_HUMAN_APPROVAL with contract/evaluation digests and revision. Recheck the exact state before recording actor/time and shipping. A human rejection with unchanged acceptance uses a counted repair; changed requirements require an explicit replacement contract.

TRIVIAL work uses the exact human request, direct diff inspection, and applicable checks; no structured handoff is required.
