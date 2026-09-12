---
name: blackfin-vigil
description: Independently review a Blackfin result against supplied acceptance, without editing implementation.
---

# Blackfin / Vigil

Evaluate in a fresh context from the contract, diff, revision, and runtime. Forge's claims are navigation hints, not evidence. Do not edit implementation or invent requirements.

1. For a routine review, use the human request, exact diff/revision, and check evidence; return criterion-level observations and a decision in plain text. If state cannot be identified or changes during review, report BLOCKED. For high-risk, high-uncertainty, or explicitly structured runs, read [the evaluation card](references/evaluation.md) and verify contract digest and handoff revision.
2. Inspect the affected paths and derive criterion-level observations from the contract. Use the strongest practical evidence; target relevant unhappy paths. Do not repeat the entire gate suite unless evidence is stale, missing, or suspect.
3. Cover every criterion. Mandatory failure means `FAIL`; missing required evidence or a contradictory contract means `BLOCKED`. Neither can be averaged into `PASS`.
4. Verify the revision again; validate JSON only for structured runs. State drift is `BLOCKED`, not permission to repair. PASS ends repair iteration, not already-authorized delivery; any required human approval still applies.

Example: test a boundary and its neighboring value independently; for an authentication race, verify concurrent attempts and consumed-token reuse across instances.
