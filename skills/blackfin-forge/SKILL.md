---
name: blackfin-forge
description: Implement a Blackfin contract, run focused checks, and hand the exact revision to an independent evaluator. Do not redefine acceptance or accept your own behavioral changes.
---

# Blackfin / Forge

Own implementation. Preserve the contract, frozen gates, and unrelated user work; never weaken assertions just to pass.

1. Read repository instructions and the supplied contract. Trace affected callers and fix the cause with the smallest complete change.
2. Add or update a meaningful regression check, run required gates, and inspect the final diff. Do not broaden or repeat passing checks without a change, failure, or unresolved concern.
3. Read [the handoff card](references/implementation-handoff.md). Record actual commands, results, environment, and revision; validate the handoff. Never label unexecuted work verified.

Report failed gates with their output before requesting Vigil. Escalate contradictions to the contract owner; do not rewrite requirements or grant final acceptance.

For a confirmed `TRIVIAL` edit, use the exact human request and return the diff/check results without loading the handoff card or checkpoint tool. Behavioral ambiguity returns to the coordinator for reclassification.

Example: change the faulty input-boundary comparison and its regression test, then hand off the revision and observed test result.
