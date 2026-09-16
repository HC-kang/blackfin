# Harness evidence — 2026-09-17

Second research pass behind v0.4.0, after the [September 12 review](harness-review-2026-09.md). Question: with GPT-6 Astra and Claude Fable 5.1 as the working models, which parts of a coding-agent harness are being removed, and which still earn their cost?

## Conclusion

What is being removed is procedural scaffolding that compensated for weaker models. What survives is structural: the parts that capability does not fix because they concern who grades the work, what counts as evidence, and what the work was supposed to be. v0.4 rewrites each skill as a short set of invariants and removes step recipes, verification nagging, and prohibition-heavy wording.

## Dying

| Element | Evidence | Strength |
| --- | --- | --- |
| Step-by-step recipes in skills | Anthropic Fable 5 prompting guide: skills written for prior models are "often too prescriptive" and "can degrade output quality". OpenAI, [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): "overly specific guidance can now hinder results". Anthropic prompting best practices: "Prefer general instructions over prescriptive steps." | Official guidance |
| Verification and approval nagging | Opus 5 guide: explicit verification instructions "cause over-verification". Astra guide: unchanged test instructions "can lead to unnecessary testing"; strong ask-first language makes the model "stop work where you'd actually be happy for it to continue". OpenAI's 2026-09-12 incident note: some older skills were "preventing the model from checking its work". | Official guidance, one incident |
| Long or overlapping skill descriptions | Codex caps the skill list at 2% of context or 8,000 characters and shortens descriptions first; this machine has more than 200 installed skills. | Official docs |
| Repository overviews in instruction files | Gloaguen et al., [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988) v2: LLM-written context, no significant success change, cost +20 to 23%. | Controlled benchmark |
| Forced context resets, sprint decomposition, tool zoos | Anthropic, [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps): both removed once newer models handled them natively. mini-SWE-agent and [The Scaffold Effect](https://arxiv.org/abs/2607.22585): harness choice moves pass rates by 0 to 8 points but tokens by up to 40x. | Internal experiment, small controlled study |

## Surviving

| Element | Evidence | Strength |
| --- | --- | --- |
| Fresh-context, read-only reviewer for work beyond reliable solo range | Fable 5 guide: "Separate, fresh-context verifier subagents tend to outperform self-critique." Anthropic harness post kept the evaluator: worth it "when the task sits beyond what the current model does reliably solo". Cognition: reviewers find more without the coder's context. [Cross-Context Review](https://arxiv.org/abs/2603.12123): fresh-session review beats same-session self-review (p = 0.008). Self-preference bias is uncorrelated or negatively correlated with capability ([Yang et al.](https://arxiv.org/abs/2604.22891)). OpenAI ships `$review-agent` read-only with detached mode. | Official guidance, controlled studies, product precedent |
| Evidence over claims | Fable 5 guide prompt "audit each claim against a tool result from this session" nearly eliminated fabricated status reports in Anthropic testing. Claude Code best practices: show the command and its output rather than asserting success. | Official guidance |
| Acceptance defined before non-trivial work; scope lock | Real-SWE (2026-09): 40.6% of failures are missed requirements. MAST: 43.9% of multi-agent failures are specification failures. Anthropic kept the planner because the generator under-scoped. Fable 5.1 guide: the request or approved plan "sets the scope, and the scope is the deliverable". Counter-signal: "If you could describe the diff in one sentence, skip the plan." | Benchmarks, official guidance |
| Reviewer probes behavior, not only tests | [SWE-ABS](https://arxiv.org/abs/2603.00520): strengthened tests reject one in five previously passing patches. | Benchmark |
| Single writer, centralized checking | Google, [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296): independent agents amplify errors up to 17.2x versus 4.4x with a central check. Cognition: writes stay single-threaded. | Controlled study, internal experience |
| Words only for counter-default rules | [Compact Constraint Encoding](https://arxiv.org/abs/2604.07192): constraints matching model defaults reach 99% compliance anyway; counter-default constraints fail 10 to 100%. OpenAI custom review rules: "state the invariant and the safe path" recovered 98% of required findings. Anthropic 2026-04-23 postmortem: an output-length rule cost about 3% on coding evals. | Controlled study, official guidance |
| User instructions outrank skills; pauses are attributable | Astra guide: make precedence explicit; when a skill causes a pause, name the file and quote the line. | Official guidance |
| Persistent notes for long-running work | Blackfin's own 2026-09-10 regression: losing the note obligation lost operational continuity. Long-context monitors miss more after very long transcripts ([Classifier Context Rot](https://arxiv.org/abs/2605.12366)). | Operational evidence, controlled study |
| Remove one piece at a time | Anthropic harness post: radical simplification lost performance and attribution; later removals went one component at a time. | Internal experiment |

## Local check

Two control runs on 2026-09-17 with no skill loaded (Claude Fable 5.1): a one-character boundary fix was reproduced, fixed, covered, and reported with test output; a planted zero-accepted defect with passing tests was caught by boundary probing and returned as FAIL with reproduction, without editing. Routine work needs no procedural guidance from Blackfin, which is why the Direct route carries none. These are two runs, not a benchmark.

## Limits

No controlled study compares a planner, implementer, and reviewer protocol against a single agent on coding tasks. The repair budget of two is a cap without a measured optimum. v0.4 changes wording and defaults; it claims no measured speed, cost, or quality gain.
