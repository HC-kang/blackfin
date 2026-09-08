---
name: blackfin-vigil
description: Independently evaluate a Blackfin revision after deterministic gates pass. Return evidence-based PASS, FAIL, or BLOCKED without modifying implementation.
---

# Blackfin / Vigil

Evaluate in a fresh context from the contract, diff, revision, and runtime. Forge's claims are navigation hints, not evidence. Do not edit implementation or invent requirements.

1. Read [the evaluation card](references/evaluation.md) and verify the contract digest and handoff revision before checking behavior.
2. Inspect the affected paths and derive criterion-level observations from the contract. Use the strongest practical evidence; target relevant unhappy paths. Do not repeat the entire gate suite unless evidence is stale, missing, or suspect.
3. Cover every criterion. Mandatory failure means `FAIL`; missing required evidence or a contradictory contract means `BLOCKED`. Neither can be averaged into `PASS`.
4. Validate the evaluation and verify the revision again. State drift is `BLOCKED`, not permission to repair. PASS ends automated iteration and leaves any required human approval pending.

Example: test a boundary and its neighboring value independently; for an authentication race, verify concurrent attempts and consumed-token reuse across instances.
