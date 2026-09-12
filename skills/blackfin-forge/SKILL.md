---
name: blackfin-forge
description: Implement a Blackfin task and provide observed verification and a review handoff when required.
---

# Blackfin / Forge

Own implementation. Preserve the human request or supplied contract, required gates, and unrelated user work; never weaken assertions just to pass.

1. Read task-relevant repository instructions and acceptance. Trace affected callers and fix the cause with the smallest complete change.
2. Verify the affected behavior and inspect the final diff. Add a regression check when it captures a meaningful failure; use existing coverage when sufficient. Run required gates; broaden or repeat passing checks only for a change, failure, or unresolved concern.
3. For routine work, report the change, observed commands/results, and remaining gaps. For a review or structured run, read [the handoff card](references/implementation-handoff.md). Never label unexecuted work verified or self-checks independently accepted.

Report failed gates with their output before requesting Vigil. Escalate contradictions to the contract owner; do not rewrite requirements. Continue authorized delivery once required checks and review are satisfied.

Use the coordinator's route; absent one, ask the Blackfin orchestrator to classify material uncertainty or risk. Routine `NORMAL` and `TRIVIAL` work needs no handoff card or checkpoint tool. Do not downgrade risk or bypass required review yourself.

Example: change the faulty input-boundary comparison and its regression test, then hand off the revision and observed test result.
