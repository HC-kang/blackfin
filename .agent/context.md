# Blackfin project memory

## Decisions

- v0.1.0 is a documentation-and-schema protocol only; Orca remains the execution runtime.
- Roles are provider-independent: Atlas plans, Forge implements, and Vigil evaluates.
- Normal work uses Atlas -> Forge -> deterministic gates -> Vigil; trivial work skips Atlas and Vigil.
- Automated repair defaults to two attempts after the initial Forge implementation, then escalates.
- Installed skills are self-contained at the decision boundary and keep expanded protocol policy in small skill-local reference cards; repository-level canonical detail lives under `references/`.

## Constraints

- Acceptance criteria remain externally owned by Atlas or the human.
- Vigil never modifies implementation code, and agent claims never substitute for executable evidence.
- Orca commands must come from the installed, version-matched `orca-cli` and `orchestration` guides rather than memory.
- Worktree isolation is not a security sandbox; execution permissions require separate controls.

## Validation

- Validate all `SKILL.md` files with the Codex skill validator.
- Parse and compile all schemas as JSON Schema 2020-12.
- Exercise installation discovery and a clean project-scope install through the `skills` CLI.

## v0.1 bootstrap wrap-up — 2026-09-03

- User correction: when a complete implementation PRD is supplied to this otherwise empty repository, proceed with the implementation instead of asking them to restate or confirm the obvious intent.
- `skills@latest` discovered and copied all four skills in a clean temporary project, including each skill-local reference card. Global installation was not executed to avoid changing the user's installed skills; the same CLI exposes the documented `--global` path.
- All four skills passed the Codex skill validator. All three schemas compiled under JSON Schema 2020-12; valid examples passed and seven hard-gate, digest, checkpoint, and blocker violations were rejected.
- A cold-read and evaluation-leakage pass exposed and fixed ambiguous trivial completion, duplicate classification ownership, Forge-test circularity, missing cross-worktree artifact rules, and revision/contract identity gaps.

## Behavioral validation wrap-up — 2026-09-03

- Orca Run `run_4b5e756483ba` exercised the real HIGH_RISK route with three fresh agents: Atlas -> Forge -> deterministic gate -> Vigil. Each role loaded its Blackfin skill, used artifact-only handoff, completed its dependency-tracked task, and released its worker terminal.
- The fixture began with a reproducible refresh-token race. Atlas produced a schema-valid four-criterion contract without changing code; Forge fixed the shared-store race with a store-owned lock and passed the repository gate; Vigil did not modify protected files and independently returned PASS.
- Vigil's stress evidence was 100 rounds of 64 simultaneous rotations with exactly one success per round, 32,000 rejected consumed-token retries, correct token state, preserved API shape, and stdlib-only imports. Evaluation schema, mandatory-criterion mapping, and hard-gate consistency passed an independent coordinator check.
- Practical gap: DIRTY checkpoint generation has no canonical documented algorithm or manifest field. Vigil eventually reverse-engineered Forge's digest, but spent several minutes trying encodings; define one reproducible algorithm before calling v0.1 frictionless.
- Packaging gap: installed skill directories contain their local cards but not the root JSON schemas, so standalone agents can only validate structured artifacts when the source repository or another schema location is supplied.
- Anti-happy-path Run `run_b6dfda382082` proved the repair loop. Vigil rejected a schema-valid Forge handoff whose PASS claim contradicted execution (`1 != 2`; 32 successes in each 32-worker race), emitted a reproducible FAIL, Forge consumed that artifact without evaluator conversation and repaired/committed the root cause, and a fresh Vigil emitted PASS after 250 rounds x 128 workers (32,000 attempts).
- Role boundaries held across the failure loop: Vigil agents changed only evaluation artifacts, Forge did not alter the contract/evaluation, hard-gate semantics survived schema validation, all worker terminals were released, and PASS stopped at configured human review.
- Operational overhead is material: dispatched role workers repeatedly loaded the full current Orca CLI and orchestration guides (about 850 lines total) to perform a small worker lifecycle. A narrow worker-lifecycle card or orchestrator-supplied protocol would preserve version matching with less context and latency.

## Operational hardening wrap-up — 2026-09-03

- DIRTY worktrees now use `blackfin-checkpoint-v1`: a shipped stdlib Python tool builds a temporary Git index/tree, binds it to HEAD, excludes reserved `.blackfin/`, and rejects dirty or uninitialized submodules. CLEAN claims require the same tool to report matching HEAD and no changed files.
- Role installs are self-contained: Atlas carries its contract schema; Forge and Vigil carry their schemas, checkpoint card, and checkpoint tool. Repository-level files remain canonical, and tests fail on mirror drift.
- `TRIVIAL` is now a distinct exact-human-task route without an Atlas contract or non-trivial handoff. It is narrowly classified, baseline-bound, and accepted only after the orchestrator independently inspects the diff and reruns frozen gates.
- Mandatory gates are frozen before Forge, and orchestrator execution rather than Forge claims opens the Vigil gate. Every failed-gate or Vigil-FAIL transition back to implementation consumes a repair cycle regardless of session reuse.
- High-risk approval is pending rather than accepted: durable approval binds actor/time to contract digest, evaluation digest, and exact revision after a final state recheck.
- Fresh cold reads exposed the trivial-route, gate-ownership, retry, CLEAN-state, and stale-approval gaps; a final independent audit marked all five operational paths fixed.
- Cross-provider smoke tests: Claude Code Haiku produced an Atlas contract from the installed skill and exposed an unvalidated-output ambiguity that was fixed; Grok loaded the installed Vigil skill and correctly blocked a legacy noncanonical checkpoint without executing semantic tests or modifying implementation.
- Final local checks cover strict JSON Schema hard gates, CLEAN/DIRTY checkpoint behavior, dirty submodule rejection, installed-asset drift, all four skill validators, and a clean four-skill copy installation.
- The v0.1.0 tag CI passed but exposed GitHub's Node 20 deprecation annotation for `actions/checkout@v4` and `setup-python@v5`; main should use their Node 24-based v6 releases. This is CI maintenance, not an agent-behavior version change, so do not move the published v0.1.0 tag.

## Fable/Astra orchestration audit — 2026-09-08

- Orca Run `run_200af58f63b0` launched fresh `gpt-6-astra` and `fable` low-effort workers against the same read-only Blackfin routing audit. Both concluded `TRIM`: keep the trivial fast path and full high-risk/high-uncertainty routes, but allow a bounded normal-lite route that folds Atlas into an externally owned or orchestrator-authored contract while retaining independent evaluation.
- Astra completed its tracked audit in 39 seconds. The normal Fable `worker-start` failed at Claude Code's workspace-trust prompt (`agent_prompt_stalled`); a tracked noninteractive retry produced the audit but denied web/out-of-worktree reads and `worker_done`, requiring lifecycle-only recovery from the same terminal. Treat provider startup/permission preflight as operational evidence, not a Blackfin role failure.
- Confirmed protocol defects: `NORMAL` is too coarse for localized changes with explicit acceptance and focused tests; `references/orca-integration.md` advances from a Forge gate claim without showing the orchestrator's independent gate execution; and the Forge handoff schema requires every recorded check to pass although policy permits optional failed/unrun checks when mandatory gates pass.
- Rejected stale worker findings: installed role schemas are now self-contained, and current policy already prevents role workers from loading full Orca guides solely for lifecycle commands.

## v0.2 lean protocol — 2026-09-08

- Supersedes v0.1 routing above: trivial edits stay in the current session without JSON/workers; clear NORMAL work uses a coordinator-authored contract, Forge, actual gates, and fresh Vigil. Atlas remains for uncertainty/high risk, and shared-state concurrency remains HIGH_RISK. No new task class or orchestration runtime was added.
- Reuse trustworthy runner-observed evidence at the exact revision; Forge summaries alone still cannot open the Vigil gate. Preserve externally owned criteria, hard mandatory gates, revision identity, human approval for high risk, and the shared two-repair limit.
- Artifact schemas are 0.2.0; optional empty metadata can be omitted, handoff checks explicitly declare `mandatory`, and optional diagnostics cannot conceal mandatory failures. Checkpoint format remains v1.
- Prior Fable/Astra audit was read-only, not a paired implementation benchmark. Fable required operator-assisted lifecycle recovery, so it does not establish clean autonomous provider startup/completion. Never bypass trust or impersonate worker completion.
- Real Orca Run `run_db651489fdf8` exposed an untested operational defect: Git rejects an excluded `.blackfin/` path when that directory is ignored. Enumerate eligible tracked/nonignored paths first and pass NUL-delimited literal paths to the temporary-index add; do not force-add ignored data or suppress errors. Regression tests cover ignored artifacts/caches, deletions, literal paths, and unchanged real index.
- Independent protocol review and checkpoint follow-up passed. The latter additionally probed unusual path names, file/directory swaps, staged-index preservation, clean/changed submodules, and dirty/uninitialized rejection.
- Role entrypoints decreased from 131 to 71 lines. `/Users/ford/agent-skills/orca-operator/SKILL.md` and its separate installed copy now share 19 lines, down from 187; the previous source is retained at `/tmp/blackfin-orca-operator-v0.1-backup.md`. The external skills directory has no Git repository, so that edit is separate from the Blackfin release.
- The real NORMAL smoke completed after the checkpoint prerequisite was repaired: Forge produced a schema-valid handoff, coordinator executed frozen gates and checked identity, and a fresh Vigil from a clean four-skill installation passed 50 independently derived boundary cases without repeating the suite. Contract/criterion mapping and before/after revision checks passed; workers reported their own lifecycle outcomes and were released. This is one bounded workflow smoke, not a general performance benchmark.

## Post-merge status — 2026-09-08

- User merged PR #3 at `7af671034c61f33cd116b04a4a18debed28d129c`; main CI run `34198669927` passed. At this status check the remote still had only v0.1.0 and no GitHub releases: merging does not automatically create v0.2.0. Do not describe the release as published until its tag exists.
- For targeted global updates, rerun `skills add` with the local source path for orca-operator or the Blackfin `/tree/main` URL and all four skill names. This avoids pulling into the existing feature worktree; the user requested commands, not installation execution.
- Installation correction: omitting `--agent` broadened this user's global installs across many agent targets and produced per-skill PromptScript failures (project-only), even though the shared skills and supported agent links succeeded. Recommend explicit `--agent codex claude-code` for those intended clients; a PromptScript failure does not mean the other targets failed. Do not remove already-created links without user approval.

## Orca note requirement audit — 2026-09-10

- Compression weakened an operational invariant: old orca-operator explicitly required worktree checkpoint updates at meaningful transitions and completion; the current source/install retains only concise Korean comment style. The transition rule survives in repository-only `references/orca-integration.md`, not the installed Blackfin orchestrator. Preserve explicit note-writing triggers when trimming skills; formatting guidance alone is not a recording obligation. This turn diagnosed the gap without changing skill behavior.
- Restored the obligation after user approval: task owner reads the current Orca comment on start/resume, records meaningful transitions and completion (also trivial tasks), preserves unresolved items, and verifies persistence. Shared-worktree notes belong to the coordinator; chat and project memory are not substitutes, and failed writes must be surfaced. Synced orca-operator source/install and Blackfin orchestrator source/install; four skill validations, source/install comparisons, and diff checks passed. Orca 1.4.199 accepted the actual start/final comments and a separate worktree-show returned the exact final note. Repository edits remain uncommitted/unpushed; installed copies already include the rule.

## v0.2.1 release preparation — 2026-09-11

- Ship the restored note obligation as patch 0.2.1; artifact `schemaVersion` remains 0.2.0 and checkpoint format remains v1. Release/package versions do not require relabeling compatible artifacts.
- Scope the stable global install example to explicit supported agents; provider targeting in an install example does not couple models to Blackfin roles.
- All three regression-test methods, changed-skill validation, source/install comparisons, four-skill discovery, and diff checks passed. Tag only the reviewed main commit, verify tag CI and installation from the remote tag, and keep final release state in the Orca worktree note. The separate local orca-operator source is not part of this GitHub repository.
