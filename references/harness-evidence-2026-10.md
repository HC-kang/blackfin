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

## Update 2026-10-17

Fifth pass, behind v0.8.0: a fresh Codex read-only audit of the skill set (14 findings; 9 reproduced or confirmed against the source, 5 deferred), two research agents (skill authoring; workflow know-how since 2026-07), and fresh-session trigger probes. Quotes marked "checked" were re-read on the raw page in this session; the rest rely on the research agents' raw-page reads.

| Change | Evidence | Strength |
| --- | --- | --- |
| A later Vigil round reviews the repair diff and earlier blocking findings; pre-existing defects that break no criterion are non-blocking; findings name the class | Anthropic, How the Claude Code team does code review (2026-10-15, checked): "about 59% of it was code that had been there since the reviewer's first pass"; a round cap plus "Diff-only re-review after the first few passes" raised one-round pass from 65% to 78%. Matches the v0.6.0 four-round Vigil loop. | Official, internal data |
| Leave out style-only findings; start with the count | Same post (checked): findings "only about style, diagnostics, or cleanup get dropped"; summaries start "with a count". | Official |
| Vigil is never a fork | Claude Code 2.1.302 changelog (2026-10-16, checked): fork subagents are on by default in `claude -p`, the SDK, desktop, and VS Code; a fork reuses the conversation. | Official |
| The task file keeps finish line, route, approvals, constraints, repairs | Lost in Context Compaction, arXiv 2608.11242 (checked): compactors "retain only 17% of injected SCs on average"; 30/100 sessions deleted email without approval after compaction. | Controlled benchmark |
| The shipped code path must produce the behavior | Building to the Test, arXiv 2606.28430 (checked): with the oracle visible, the score was near-perfect "from a demo holding the tested behavior directly". 18 runs. | Small study |
| New tests assert an outcome | All Smoke, No Alarm, arXiv 2606.18168 (checked abstract): 86,156 agent-authored test-file patches; weak or missing oracles were common. | Large empirical study |
| Change approach or model after the same failure twice | Anthropic, Spending your effort and What a task costs on Opus 5.5 (2026-09-25): more effort "does not fix when the model has the wrong approach". | Official, internal eval |
| A trigger must name something in the model's context; use a SessionStart hook for Orca | Local probes (2026-10-17): fresh `claude -p` ×2 and `codex exec` ×1 did a file task in an Orca worktree without loading orca-operator or touching the card; the cue was an env var. Claude Code skills docs (checked): a loaded skill is not re-read on later turns. Claude and Codex hooks docs (checked): SessionStart plain stdout becomes context. | Operational evidence, official docs |
| Name exact flags | orca-operator never named `--workspace-status`; guessing `--status` failed. arXiv 2610.04832: rules naming a command or path held across model generations. | Operational evidence, controlled benchmark |
| The report description excludes app pages | openai/codex #33164 (2026-07-14, checked): a visualization skill "over-triggers on standalone HTML requests". | Anecdote |
| Report the evaluated location and the undo path | Anthropic code review post (checked): add "How to revert" to the PR template. | Official |

Not adopted: risk wording shifts reviewer decisions (arXiv 2608.02677), but the contract schema requires `taskClass`; vendors disagree on pushy descriptions (agentskills.io vs OpenAI, 2026-09-11), so descriptions stay narrow and trigger probes measure them; the Codex validator also accepts `license`, `allowed-tools`, and `metadata` but rejects `compatibility`, and Blackfin keeps `name` and `description` only. Supporting evidence without a rule change: SkillsBench (arXiv 2602.12670 v4) found self-generated skills below the no-skill baseline, so agent-edited skills need a baseline comparison; arXiv 2608.11888 found harm when skills turn checklists into mandatory work.

Limits: trigger probes were one or two runs per CLI. Grok was not signed in. The five deferred audit findings (blocked-result identity fields, out-of-criteria FAIL, shared-worktree checkpoints, two checker heuristics) were not reproduced.
