# Orca integration

Orca owns execution and lifecycle. Blackfin owns acceptance and evidence. For supervised work, resolve the CLI through the installed `orchestration` skill and read its version-matched guide once. Read `orca-cli` only for additional workspace or browser operations. Workers use the injected lifecycle preamble.

Before dispatch, confirm model/effort, workspace trust, required artifact/runtime access, and lifecycle permissions. Inspect launch receipts; a terminal existing is not proof that an agent accepted the task. Do not bypass provider trust prompts. Failed lifecycle reporting requires an explicit coordinator recovery record after inspecting evidence, not a forged worker completion.

## Routine work

Use the current session for a clear low-impact bug: read the existing worktree note, implement the human's requested behavior, run focused checks, inspect the diff, and save/verify the outcome note. No Run or worker is required. If independent review is warranted, send standalone acceptance, identified source state, and observed check evidence to one fresh Vigil.

## Structured example: authentication race

1. Coordinator creates a tracked Orca Run and asks Atlas for observable cross-instance single-use acceptance. The structured contract requires human approval; investigation is bounded.
2. Forge implements in the task worktree and supplies its revision-bound handoff. The coordinator checks actual frozen-gate output at that state before evaluation.
3. A fresh Vigil gets only the contract, source state/diff, handoff, and runtime access. It reproduces concurrent use and consumed-token retries; it does not edit implementation.
4. FAIL returns evidence to Forge within the persisted repair budget. PASS stops repairs and awaits required approval against that revision before shipping.

Use the current `orchestration` guide's Run, worker-start, inbox, and settlement commands rather than copying a second CLI manual here. Task specifications name the target, expected result, constraints, write ownership, and observable acceptance; pass absolute artifact paths and skill locations.

Continue rolling waits until expected dispatches settle; timeouts are liveness checkpoints. Follow the loaded guide for questions, failed starts, retries, and cleanup. Verify task/dispatch provenance before claiming orchestration.

Return gate failures as commands/output, Vigil failures as evaluation artifacts, and preserve the contract and consumed repair count. Default two repairs after the initial attempt. Reverify source state after Vigil and before delivery; continue already-authorized delivery only when required approval is satisfied.

Use one resulting implementation state for evaluation and absolute paths across worktrees. Never treat worktrees as credential or network sandboxes. Follow the installed [orchestrator's worktree-note requirement](../skills/blackfin-orchestrator/SKILL.md), including task completion on the trivial route. Read the current `orca-cli` guide for comment operations; unrelated file edits do not require loading Orca guides.
