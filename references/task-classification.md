# Task classification

The coordinator chooses the highest applicable class from repository evidence. Model capability alone never lowers risk.

| Class | Signals | Route |
| --- | --- | --- |
| `TRIVIAL` | Exact wording, comments, static renames; no behavioral effect | Direct edit -> diff and applicable checks |
| `NORMAL` | Clear, low-impact behavior with understood scope and meaningful verification | Current agent -> focused checks -> outcome; add fresh Vigil when review is needed |
| `HIGH_UNCERTAINTY` | Unknown root cause, unclear performance/concurrency behavior | Atlas + bounded diagnosis -> Forge -> gates -> fresh Vigil |
| `HIGH_RISK` | Auth, payment, migration, destructive data, shared-state concurrency, security, production infrastructure | Atlas -> Forge -> gates -> fresh Vigil -> human approval |

For routine `NORMAL` work, the human request supplies acceptance; no planner worker, JSON artifacts, or checkpoint tool is required. Add fresh Vigil for requested/required review, broad regression exposure, subjective acceptance, or weak verification. A focused test is evidence, not proof of complete coverage. Without Vigil, report observed checks and gaps rather than independent acceptance.

High-risk and high-uncertainty work retains structured contracts, handoffs, and evaluation. Use the structured path also when the user or an automation consumer requires it. An existing structured run stays structured. Neither task relabeling nor model capability can waive required gates, missing evidence, approval, or a consumed repair budget.

`TRIVIAL` excludes runtime, interface, data, dependency, configuration, generated-output, and security effects. Any ambiguity is at least `NORMAL`; trivial work needs neither role workers nor JSON/checkpoint artifacts.

Cap uncertain investigation by time or worker count. Use parallel workers only for distinct hypotheses or independent evidence sources. A missing requirement or environment may block the run before Forge; do not implement a guessed solution.
