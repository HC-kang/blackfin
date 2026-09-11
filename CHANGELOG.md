# Changelog

All notable Blackfin behavior changes are recorded here. Blackfin follows semantic versioning because skill changes alter agent behavior.

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
