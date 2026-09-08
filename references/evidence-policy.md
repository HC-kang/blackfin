# Evidence policy

Prefer observable runtime behavior, integration/E2E execution, deterministic tests, static analysis, code inspection, then agent explanation. Choose evidence appropriate to the criterion; higher-order contradictory observations win. Forge claims never prove acceptance.

Bind evidence to the evaluated revision and relevant command/environment. Missing required evidence is BLOCKED, observed mandatory failure is FAIL, and all mandatory criteria passing is PASS. Optional failures remain visible and cannot excuse a mandatory failure.

Freeze mandatory gate commands before Forge. Forge cannot omit or demote them. Before Vigil, the coordinator inspects runner-observed command output and exit results at the handoff revision, or executes the gates itself when only agent summaries are available. Unbound logs and Forge's PASS labels cannot open the gate.

READY requires at least one passing mandatory deterministic check and no failing/unrun mandatory gates. If the repository has no gates, use the smallest meaningful contract-specific check. If none is possible, report BLOCKED. For trivial prose edits, a direct diff inspection plus applicable repository checks is sufficient; no synthetic runtime test is needed.

Record optional diagnostics with `mandatory: false` and explanatory evidence; otherwise checks are mandatory. Optional failures/unrun checks can coexist with READY only if they do not contradict mandatory criteria. A failed frozen gate remains mandatory whatever Forge labels it.

Do not broaden or repeat passing checks without changed code, stale/missing/suspect evidence, or an unresolved concern. Vigil derives criterion-level observations from the contract; merely rerunning Forge's tests proves reproducibility, not independent acceptance.
