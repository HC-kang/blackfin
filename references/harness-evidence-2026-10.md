# Harness evidence — 2026-10-14

Fourth research pass, behind v0.6.0. It follows the [September record](harness-evidence-2026-09.md). Three parallel searches covered vendor guidance and user reports since 2026-09-15, recent papers, and information design for HTML reports. Quotes were checked against raw pages. Strength labels: official guidance, controlled benchmark, small study, practitioner report, anecdote.

## Worktree notes

| Change | Evidence | Strength |
| --- | --- | --- |
| Reconcile the note with HEAD before acting; a stale note is worse than none | Working Set / Coherence Debt (arXiv 2608.16630): "a stale convention file costs more than no file". MemTrace (2610.04838): checking recalled evidence against the current repository gained up to +21.2 points. | Controlled benchmark |
| Pin evidence to an exact command and a sha | Handoff Debt (2606.02875): short notes dropped the exact validation command. EA-Graph (2608.04278): claims anchored to artifact content beat prose notes. | Controlled benchmark, small study |
| Rebuild the note from the repository, not from the last note | CliffCompaction (2609.26779): "We never compact a compaction." | Controlled benchmark |
| An unreadable note is unknown | Anthropic, Building effective agent automations (2026-10-08): "Report a failed read as unreadable, never as a quiet day." | Official guidance |
| The trigger matters more than the rule | Local Orca data (2026-10-14): 54 of 65 in-progress worktrees had no note, and 1 of 14 notes named a next action; this worktree's own note was stale through the v0.5 work. | Operational evidence |

## Evidence, review, and convergence

| Change | Evidence | Strength |
| --- | --- | --- |
| Implementer-written passing tests are weak; a check that fails without the change is strong | Groundability (2610.01023): failing check reject precision 0.82, passing test accept precision 0.30. ExecCritic (2609.09133), 2610.03984. Cockroach Labs (2026-10-09): reviews start "by disabling the change and ensuring that all new tests fail." | Controlled benchmark, practitioner report |
| A syntax-only check or a check that failed to start is not evidence | Anthropic, Building with Claude Sonnet 5.5 (2026-09-28). | Official guidance |
| A new Vigil per review round; a different agent family for a second high-risk round | Audit-Repair Leniency (2608.16003): prior audit-repair context lowered false alarms by loosening the threshold. Cross-Model Review (2610.01471): 56.7% vs 42.7% planted errors found. | Controlled benchmark, small study |
| Blocking findings need a reproduction; non-blocking findings do not trigger work | Anthropic, Redesigning source control (2026-10-13): adversarial review "can also be myopic". Cockroach Labs: non-blocking nits spawned new issues. | Official experience, practitioner report |
| Bound automatic continuation and keep follow-ups out of the run | Opus 5.5 platform prompting guide: "stop after two or three automatic continuations". Codex issues #53748, #46904. | Official guidance, anecdotes |
| Name where the change lives | Codex issue #46853 and Claude Code issue #95968: completion claimed on the wrong checkout. | Anecdotes |
| Report unread files and unrun checks | OverclaimBench (2609.20812): 67.9% of runs skipped assigned files; 80.4% of those reported misleadingly. | Controlled benchmark |
| Small tasks stay serial; parallel branches merge by replay | Dynamic Concurrency (2610.10263): −24.0 points for Claude Code on SWE-bench Verified with 2–4x tokens. MERGEGYM (2610.04779): 47.3% of textual conflicts arose with disjoint write sets; `git merge-tree` replay cost 0.02 s. | Controlled benchmark, small study |
| Delegation to Vigil must be explicit for Codex | Codex subagents docs: delegation happens "when applicable AGENTS.md or skill instructions request it". | Official docs |
| Short handoff brief, not the transcript; the receiver reads back | Handoff Tax (2608.24358); Cockroach Labs read-back practice. | Controlled benchmark, practitioner report |

## HTML reports

| Change | Evidence | Strength |
| --- | --- | --- |
| HTML beats long Markdown for one-time reading | Shihipar, The unreasonable effectiveness of HTML (claude.dev, 2026-05-20): "Optimize it for someone reading it once." Example reports measured at 0–39% prose and at most 50 words per paragraph. | Vendor practice |
| Overview first, details on demand; inverted pyramid | Shneiderman 1996; NN/g: 79% of users scan, concise and scannable text 124% more usable. | Research |
| Encode with position and length | Heer & Bostock 2010 replicating Cleveland & McGill. | Controlled study |
| Default static; interaction answers a question; never hide what matters | Tse (NYT 2016): "If content is important for readers to see, don't hide it." Aisch 2017; Boy et al. CHI 2015. | Practitioner evidence, controlled study |
| Name the default looks to avoid | Opus 5.5 guide: "A list of specific patterns works much better." OpenAI frontend guidance and Anthropic design guidance list the patterns. | Official guidance |
| Detect with a script, confirm on the render | 2602.20084: models correct violations better than they detect them. VisJudge-Bench (2510.22373): MLLM ratings correlate 0.428 with humans. ArtifactsBench (2507.04952): screenshots plus checklists reach 94.4% ranking consistency. | Controlled benchmarks |
| Accessibility floor | WCAG 2.2: 1.4.1, 1.4.3, 1.4.11, 2.3.3. Okabe-Ito palette. | Standard |

## Local check

Four baseline runs without the report skill (Codex and Claude, a structured migration input and a prose research input) produced no text dump: prose share was 10–31%, and both models led with a verdict. All four lacked dark mode, the Claude pages had no interaction, one loaded remote fonts, and the prose-input Claude page encoded none of its data graphically. The skill therefore targets missing encoding, interaction, offline rendering, and delivery rather than a text dump the baselines did not show.

## Limits

Most paper results come from single studies, several small. The checker thresholds are calibrated on six vendor examples and these runs; they are judgment calls. Grok could not be exercised because the local CLI was not signed in.
