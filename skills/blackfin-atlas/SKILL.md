---
name: blackfin-atlas
description: Plan ambiguous or high-risk Blackfin work into observable acceptance; unnecessary for routine edits.
---

# Blackfin / Atlas

Own WHAT and WHY. Do not edit production code or prescribe HOW unless an external constraint requires it.

1. Read task-relevant repository instructions and trace the affected behavior. Identify material assumptions, compatibility boundaries, and blockers.
2. Define a bounded objective, observable criteria, and appropriate verification. Current implementation choices are not requirements by default.
3. Read [the authoring card](references/contract-authoring.md), validate the contract, and hand it off without requiring this conversation. Report `BLOCKED` for contradictory requirements or missing decisions.

Only the human or designated contract owner may replace acceptance criteria. Replacement is explicit and invalidates prior evaluation; Forge never owns this decision.

Example: for duplicate token rotation, specify at most one success across application instances and failed reuse, without prescribing a lock or storage library.
