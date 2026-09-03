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
