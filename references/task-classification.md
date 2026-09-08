# Task classification

The coordinator chooses the highest applicable class from repository evidence. Model capability alone never lowers risk.

| Class | Signals | Route |
| --- | --- | --- |
| `TRIVIAL` | Exact wording, comments, static renames; no behavioral effect | Direct edit -> diff and applicable checks |
| `NORMAL` | Bounded behavior with understood scope and verification | Coordinator contract -> Forge -> gates -> fresh Vigil |
| `HIGH_UNCERTAINTY` | Unknown root cause, unclear performance/concurrency behavior | Atlas + bounded diagnosis -> Forge -> gates -> fresh Vigil |
| `HIGH_RISK` | Auth, payment, migration, destructive data, shared-state concurrency, security, production infrastructure | Atlas -> Forge -> gates -> fresh Vigil -> human approval |

For `NORMAL`, the coordinator can use the Atlas authoring card/schema without a planner worker. Add Atlas when scope or verification needs material investigation. A focused existing test helps establish evidence, but does not by itself prove coverage or authorize skipping Vigil.

`TRIVIAL` excludes runtime, interface, data, dependency, configuration, generated-output, and security effects. Any ambiguity is at least `NORMAL`; trivial work needs neither role workers nor JSON/checkpoint artifacts.

Cap uncertain investigation by time or worker count. Use parallel workers only for distinct hypotheses or independent evidence sources. A missing requirement or environment may block the run before Forge; do not implement a guessed solution.
