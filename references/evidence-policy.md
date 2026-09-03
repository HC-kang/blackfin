# Evidence policy

Blackfin accepts observed evidence, not agent confidence.

## Strength order

1. Observable runtime behavior
2. Integration or end-to-end execution
3. Deterministic tests
4. Static analysis
5. Code inspection
6. Agent explanation

Use the strongest practical evidence for the behavior. When evidence conflicts, the higher-order observation wins. A Forge claim, including `criteriaClaimed`, is navigation metadata only.

Re-running a Forge-authored test proves reproducibility, not independent acceptance by itself. When practical, Vigil derives at least one criterion-level observation directly from the Acceptance Contract. If only lower-order evidence is possible, the evaluation must say so and may not overstate confidence.

## Evidence requirements

Evidence must identify the exact evaluated revision and enough environment or command detail to reproduce the observation. Never report an unexecuted check as passed. Evidence from a different revision is stale.

For every mandatory criterion:

- record the observed result;
- distinguish pass, fail, and unavailable evidence;
- include a minimal reproduction for failures when practical;
- exercise unhappy paths that are part of the contract, such as empty input, partial failure, retries, races, authorization boundaries, and rollback behavior.

## Deterministic gates

Run repository-defined compilers, format checks, linters, type checks, tests, schema checks, migration checks, and similar deterministic verification before Vigil.

Before Forge starts, the orchestrator freezes the mandatory command set from repository instructions and deterministic checks required by the Acceptance Contract. Forge may add checks but may not omit a frozen gate from its handoff. The orchestrator executes the frozen commands independently before Vigil; Forge's check claims alone cannot open the gate.

If a mandatory deterministic gate fails, stop semantic evaluation and return the evidence to Forge. Do not spend evaluator work explaining a compiler or test failure.

A `READY_FOR_EVALUATION` handoff requires at least one passing check. When a repository defines no gates, Forge must run the smallest contract-specific deterministic check; if no meaningful check is possible, the run is `BLOCKED` rather than green by default.

## Decisions

- `PASS`: all mandatory criteria have sufficient passing evidence.
- `FAIL`: at least one mandatory criterion has contradictory evidence.
- `BLOCKED`: required evidence cannot be obtained, or the contract is contradictory, impossible, or materially incomplete.

Mandatory criteria are hard gates. Quality elsewhere cannot average away a failure.
