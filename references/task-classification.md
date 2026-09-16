# Task classification

The coordinator asks two questions and takes the highest row that applies: what breaks if this change is wrong, and how strong is the verification available? Model capability never lowers a row.

| Class | Signals | Route |
| --- | --- | --- |
| `TRIVIAL` | Exact wording, comments, static renames; no runtime, interface, data, dependency, configuration, generated-output, or security effect | Direct: edit, diff, applicable checks |
| `NORMAL` | Clear, low-impact behavior with understood scope and a focused check that proves it | Direct: implement, observed evidence, outcome. Add a fresh Vigil when review is requested or required, regression exposure is broad, acceptance is subjective, or verification is weak |
| `HIGH_UNCERTAINTY` | Unknown root cause, unclear scope, unclear performance or concurrency behavior | Structured: Atlas with bounded diagnosis, Forge, frozen gates, fresh Vigil |
| `HIGH_RISK` | Irreversible or shared: auth, payment, migration, data deletion, shared-state concurrency, security, production infrastructure | Structured plus human approval of the evaluated result |

Direct work uses the human request as acceptance and needs no planner session, JSON artifact, worker, or checkpoint tool. A focused test is evidence, not proof of complete coverage; without Vigil, report observed checks and gaps rather than an independent PASS.

Structured runs keep the validated contract, revision-bound handoff, and evaluation described in the orchestrator runbook. Use them also when the user or an automation consumer requires schema-validated artifacts. An existing structured run stays structured; neither relabeling nor model capability waives a required gate, missing evidence, approval, or a consumed repair budget.

Any ambiguity is at least `NORMAL`. Bound uncertain investigation by time or worker count; use parallel workers only for distinct hypotheses or independent evidence sources, never for parallel writes. A missing requirement or environment blocks the run before Forge; do not implement a guessed solution.
