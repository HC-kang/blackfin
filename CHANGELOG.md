# Changelog

All notable Blackfin behavior changes are recorded here. Blackfin follows semantic versioning because skill changes alter agent behavior.

## [0.8.0] - 2026-10-17

- Review convergence: a later Vigil round reviews the repair diff and checks each earlier blocking finding; a defect outside the repair diff that breaks no acceptance criterion is non-blocking. Findings name the defect class, leave out style-only remarks, and the result starts with the blocking count. Vigil runs as a subagent without the conversation, never a fork. Anthropic reported that about 59% of re-review findings were code present since the first pass.
- Evidence: Vigil copies new tests into the exported base revision and requires them to fail at the assertion; a test-only stand-in proves nothing, so the shipped code path must produce the behavior. Forge's new tests assert an observable outcome. The evaluation schema rejects `PASS` with blockers.
- Orchestrator: rows run from least to most consequential and the lowest applicable row wins; each return to Forge consumes one repair however many findings it carries; a step that fails twice the same way changes approach or model; waiting on a live worker in a supervised Run follows Orca's wait rules. Long runs keep the finish line, route, approvals, user constraints, and repair count in the task file, because compaction drops constraints. When orca-operator is installed it owns card mechanics.
- Reports: page text follows the user's writing rules or an installed writing skill such as `k-ste`; the fallback for Korean is 한다체 body text, 합니다체 buttons (decision options included) and hints, and noun-phrase labels. The verdict names where the change lives and how to undo it. The description excludes app pages. Printing shows rows a filter hid. The exclusion step runs only in a Git repository.
- Checkpoint card states that the tool checks both states and only `DIRTY` carries a checkpoint. Research and limits are in [October evidence](references/harness-evidence-2026-10.md#update-2026-10-17). Artifact schemas remain 0.2.0; checkpoint format remains v1.

## [0.7.0] - 2026-10-14

- Report pages follow ASD-STE100 wording in the user's language: complete one-idea sentences (20 words for instructions, 25 for descriptions), one register across the page (in Korean, 합니다체 prose and noun-phrase labels), active voice, one term per thing and one verb per action, at most one hedge, no filler, and every condition and number kept. The checker warns on sentences over 25 words; the template text follows the same rules.

## [0.6.1] - 2026-10-14

- Report template: metadata labels no longer wrap one character per line on narrow screens.

## [0.6.0] - 2026-10-14

- Add `blackfin-report`: a self-contained HTML report for finished work. The page leads with the verdict and a unit bar, puts open decisions in a picker that composes a reply line, shows numbers beside their comparisons, makes long item lists filterable and sortable, and keeps evidence on demand while gaps stay visible. It ships a template (dark mode, print, Okabe-Ito status colors, keyboard controls), a visual grammar with named default looks to avoid, a stdlib checker (`report_check.py`), and a render checklist.
- Worktree notes become the shared record: reconcile the note with branch, HEAD, and uncommitted files on start; replace a stale note; treat an unreadable note as unknown; read sibling notes before shared changes; write `state: change | command → result @sha | 다음: next action` rebuilt from the repository; set the attention flag when the user must act; keep the report path in the note.
- Evidence: implementer-written passing tests locate behavior; checks that fail with the change disabled, or owner-fixed checks, are stronger; syntax-only checks and commands that failed to start are not evidence. Forge shows fail-before and pass-after for bug fixes, names where the change lives, and lists unread files and unrun checks.
- Review and convergence: delegate explicitly to a new Vigil each round, preferring another agent family for a high-risk second round; Vigil disables the change to confirm new tests fail and marks findings blocking (with reproduction) or non-blocking. Non-blocking and out-of-scope work goes to one follow-up list; the same unfinished item continues automatically at most twice.
- Parallel implementation is for long, separable work; parallel branches merge by `git merge-tree` replay and are gated on the merged result. Handoff briefs carry state and evidence instead of the transcript, and the receiver restates the finish line.
- Research and limits are in [October evidence](references/harness-evidence-2026-10.md). Artifact schemas remain 0.2.0; checkpoint format remains v1. v0.5.0 was not tagged separately; its changes ship in this release.

## [0.5.0] - 2026-09-23

- Align with the Claude Opus 5.5 guide (2026-09-22) and the GPT-6 family prompting guide (Astra, Sol, Luna). Evidence and limits are in [harness evidence](references/harness-evidence-2026-09.md#update-2026-09-23).
- The orchestrator names the finish line before work, keeps going while no step needs the user, and stops only for a blocker, a required approval, or a destructive or out-of-scope action. Long runs keep the task list in a file. The final report leads with what needs the user.
- Harmonize with Orca 1.4.207 built-in orchestration rules. Child agents may investigate or implement in parallel on scopes that do not overlap, with named edit ownership and separate worktrees when writes conflict or land as separate PRs; each result is accepted only after its evidence is checked. Vigil stays read-only, and a review result authorizes synthesis, not coordinator edits. A handoff carries acceptance, route, and consumed repairs and ends at the accepted send. Dispatched workers ask their coordinator and report in the `worker_done` format.
- Forge does not stop at a first implementation, does not write tests that mirror a reversible low-impact change, and repeats checks only for a new change, failure, or concern. Vigil reports each finding with file, line, cause, and reproduction, blocking findings first. Atlas marks what it could not confirm and where it looked.
- A pause caused by Blackfin says whether it follows an explicit rule or an interpretation. A mid-run user change is folded into Direct work and is an explicit replacement in a structured run. The runbook passes a model only when the user named one, an effort only when the model supports it, and confirms both from `launch.effective`.
- Artifact schemas remain 0.2.0; checkpoint format remains v1.

## [0.4.0] - 2026-09-17

- Rewrite each skill as a short set of invariants for current models: acceptance owned outside the implementer, observed evidence at the evaluated state, one writer per worktree, fresh read-only Vigil, bounded repairs, structured runs that stay structured, and one approval of the evaluated result. Step recipes, verification reminders, and prohibition-heavy wording are removed.
- Route with two questions, consequence and verification strength, mapped to the existing classes; `TRIVIAL` and `NORMAL` run Direct with no ceremony. The user's instructions outrank Blackfin, and a Blackfin-caused pause must name the skill and line.
- Forge audits each claim against a session tool result and keeps the requested scope. Vigil starts every criterion at FAIL, probes beyond shipped tests, and reports the whole diff before marking what affects acceptance.
- Skill descriptions state purpose, trigger, and boundary in under 260 characters; frontmatter is limited to `name` and `description` for Codex and Claude Code. A package test enforces both plus the Orca note obligation.
- Reference cards keep only structured-run JSON, rules, and commands. [Harness evidence](references/harness-evidence-2026-09.md) records the research behind this release. Artifact schemas remain 0.2.0; checkpoint format remains v1.

## [0.3.0] - 2026-09-12

- Routine, clear low-impact behavior can complete in the current session with observed checks and an outcome record. Workers, three JSON artifacts, and checkpoint tooling are no longer the default for NORMAL work.
- Independent review remains required for requested/required review, broad regression exposure, subjective acceptance, or weak verification. High-risk and high-uncertainty routes retain Atlas, structured artifacts, and fresh Vigil; high risk still requires human approval. Active structured runs cannot downgrade around blockers.
- Plain-text routine reviews bind acceptance to identified source state and evidence. Self-checks never imply independent PASS; required checks, permission boundaries, bounded repairs, and verified Orca notes remain.
- Stop repairs after passing checks/review, then continue already-authorized delivery instead of adding an unnecessary approval stop. Shorten skill discovery descriptions and defer format-specific instructions and Orca commands until needed.
- Document primary-source research and its limits. No measured Blackfin performance improvement is claimed. Structured schemaVersion remains 0.2.0; checkpoint format remains v1.

## [0.2.1] - 2026-09-11

- Restore mandatory Orca worktree notes at meaningful transitions and task completion, including trivial tasks. Read existing notes on resume, preserve unresolved items, assign shared notes to the coordinator, and verify persistence; chat or repository memory alone is insufficient.
- Scope the global installation example to explicitly selected agents so project-only targets do not cause partial installation failures. Artifact schemas remain 0.2.0; checkpoint format remains v1.

## [0.2.0] - 2026-09-08

- Fix checkpoint creation when the reserved `.blackfin/` artifact directory is gitignored; preserve the checkpoint format and cover ignored artifacts, deletions, and literal filenames.

- Clear normal work uses a coordinator-authored contract; a separate Atlas session is reserved for ambiguity and higher-risk work. Trivial edits complete directly without role workers or JSON/checkpoint ceremony.
- Reuse task worktrees and runner-observed gate evidence at the exact revision. Vigil retains independent contract probes without mandatory duplicate full-suite runs.
- Shorten role entrypoints; load Orca guides only for operations actually needed. Preflight provider startup, artifact access, and lifecycle permissions without bypassing trust prompts.
- Handoff checks explicitly distinguish mandatory gates from optional diagnostics. Optional failures remain reportable without hiding mandatory failures; high-risk contracts enforce human approval.
- Artifact schemas advance to 0.2.0; omit empty optional contract/handoff metadata. v0.1 artifacts require their original assets or an explicit replacement contract. Checkpoint v1 is unchanged.

## [0.1.0] - 2026-09-03

### Added

- Atlas, Forge, Vigil, and Orchestrator skills.
- Structured Acceptance Contract, Forge handoff, and Vigil evaluation schemas.
- Evidence hierarchy, hard-gate evaluation, task classification, repair-loop limits, and Orca integration guidance.
- Global installation and versioning documentation.
- Self-contained role-local schemas and a canonical dirty-worktree checkpoint shared by Forge and Vigil.
- Orchestrator-supplied Orca worker lifecycle instructions to avoid repeated full-guide loading by role workers.
- Protocol, schema hard-gate, packaging-drift, and checkpoint checks in CI.
