# Task classification

Choose the highest class whose signals apply. Classification controls ceremony, not implementation style.

The orchestrator owns routing classification. Atlas confirms it after repository inspection and reports evidence that requires escalation to a higher class; Atlas does not silently change the active route.

| Class | Signals | Required route |
| --- | --- | --- |
| `TRIVIAL` | Typo, comment-only update, obvious static rename | Forge -> deterministic checks -> orchestrator completion |
| `NORMAL` | Business logic, endpoint, UI behavior, bounded bug with understood cause | Atlas -> Forge -> gates -> Vigil |
| `HIGH_UNCERTAINTY` | Unknown production bug, unclear root cause, performance regression, concurrency | Atlas plus bounded investigation when useful -> Forge -> gates -> Vigil |
| `HIGH_RISK` | Authentication, authorization, payment, migration, destructive data, security boundary, production infrastructure | Atlas -> optional investigation -> Forge -> gates -> Vigil -> human approval |

## Classification checks

- Assumption -> what breaks if false -> mitigation.
- Partial failure or retry -> data or state consequence -> recovery path.
- Missing runtime, credentials, fixtures, or observability -> whether meaningful verification remains possible.
- Migration or destructive action -> rollback and human approval.

Do not create multiple agents merely because a task is non-trivial. Independent investigators are useful only for distinct hypotheses or evidence sources. Prefer the smallest route that preserves the required independence and risk controls.

`TRIVIAL` is limited to wording, comment-only changes, and obvious static renames with no runtime, interface, data, dependency, configuration, generated-output, or security effect. Any ambiguity is at least `NORMAL`. The trivial route uses the exact human request and gate evidence; every other class requires an Acceptance Contract and Forge handoff.
