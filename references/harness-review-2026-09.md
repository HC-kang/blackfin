# Harness review — 2026-09-12

## Conclusion

Reduce procedural scaffolding for work the agent can reliably complete with observable checks. Preserve task boundaries, evidence, state continuity, and review where the consequence of a miss or the weakness of verification justifies it. This supports a lighter Blackfin default, not a claim that every harness or independent evaluator is obsolete.

## Primary-source findings

| Source | Finding | Limit when applying to Blackfin |
| --- | --- | --- |
| [OpenAI, Rethinking skills and prompts for GPT-6 Astra, 2026-09-11](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Narrow skill descriptions, load only relevant references, revisit rigid recipes and unnecessary approval stops. | Official model guidance, not a controlled Blackfin benchmark; other models may need different support. |
| [OpenAI, GPT-6 Astra guidance, accessed 2026-09-12](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra) | Audit conflicting instructions and calibrate testing, delegation, and persistence to the task. | Does not authorize removing user permissions or required checks. |
| [Anthropic, Harness design for long-running application development, 2026-03-24](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Newer models allowed removing context resets and sprint decomposition. Evaluator value depended on task difficulty; complex builds still benefited from independent runtime QA. | Qualitative application experiments with different scopes and budgets, not an equal-budget randomized comparison or a result for every current model. |
| [Gloaguen et al., Evaluating AGENTS.md, v2, 2026-06-23](https://arxiv.org/html/2602.11988v2) | LLM-written context increased average cost by 20%/23% on the two benchmarks without statistically significant success-rate improvement. | Four older model/agent combinations, 300 SWE-bench Lite and 138 CTXbench tasks; not Astra, Fable, or Blackfin. Does not establish that all memory is harmful. |
| [OpenAI, Harness engineering, 2026-02-11](https://openai.com/index/harness-engineering/) | A short navigation entrypoint and mechanically checked invariants replaced an oversized instruction manual. | One internal engineering experience; its extensive repository infrastructure is not a template to copy into this small protocol. |
| [Anthropic, Effective context engineering, 2025-09-29](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Minimal high-signal context, persistent notes, and selective multi-agent work address different needs. | General engineering guidance; context limits and task characteristics still matter. |

The AGENTS.md paper's revised analysis matters: small success-rate differences versus no context were not statistically significant. Reporting “AGENTS.md makes agents worse” would overstate the result. Its evidence supports testing the benefit of instructions and pruning redundant overviews, not deleting repository-specific constraints.

The Anthropic article also cautions against removing everything at once: radical simplification initially lost useful behavior. Its later simplification retained the evaluator at the edge of model capability. Neither a permanent three-agent pipeline nor a blanket ban on reviewers follows from that result.

## Review of Blackfin v0.2.1

The entrypoints were already short. The larger burden came from unconditional activation of deeper procedures:

- Every behavioral NORMAL change required three validated JSON artifacts and fresh Vigil. The Forge card blocked work if the schema validator or checkpoint tool was unavailable, even when the human request and local verification were straightforward.
- The default pipeline treated independent evaluation as equally useful for a localized deterministic edit and a complex/subjective change. Existing task labels did not express that difference.
- “PASS stops automation” could end a user-authorized release after review instead of continuing delivery. A stop on repairs and a stop on external authority are different conditions.
- Orca lifecycle instructions duplicated parts of the version-matched runtime guide. Skill descriptions mixed discovery with behavioral restrictions.
- Project memory placed historical v0.1 routing near the top without clearly distinguishing it from current policy.

The following remain load-bearing: externally owned acceptance, required checks, visible failures, source-state identity for review, read-only independent evaluation when required, bounded retries, high-risk approval, and verified Orca notes. The user specifically reported losing operational continuity when the note obligation was weakened. That correction is not speculative scaffolding.

## v0.3 decision

Use one session for clear low-impact behavior with meaningful verification. Keep a short outcome record rather than mandatory serialization. Add fresh review for requested/required review, broad regression exposure, subjective acceptance, or weak verification. High-risk/high-uncertainty and explicitly structured runs retain the existing JSON protocol and tools. Active structured runs cannot downgrade around a failed gate, missing prerequisite, or consumed retry budget.

Keep the four existing skills and compatible schemas. No new orchestrator, routing configuration, evaluator service, or dependency is needed. The local Orca operator defers execution mechanics to the current Orca guides and Blackfin policy to Blackfin, while retaining the worktree-note requirement.

## Evidence limits and follow-up

Prior Blackfin runs establish that structured handoffs, a failure/repair loop, and a bounded normal coding smoke can work. The Astra/Fable read-only audit and the later single coding smoke do not establish a performance advantage over a simpler baseline. Fable startup and lifecycle recovery also make that audit unsuitable as a clean provider comparison.

This release changes policy defaults; it makes no measured speed, cost, or quality claim. Deterministic package checks and fresh-agent behavioral checks can catch release regressions, but cannot prove broad model reliability. If routing proves too permissive in actual work, use the preserved structured route and record the concrete miss before adding a general rule.

For a useful later comparison, run the same representative tasks with the same model, effort, environment, externally fixed acceptance, and retry budget under both policies. Keep notes in both conditions. Compare independently checked outcomes, missed defects, elapsed time, tokens, and human interventions. Change one scaffolding component at a time; do not build a benchmark framework just to count prompt lines.
