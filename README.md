# Blackfin

Blackfin is a small, provider-independent engineering protocol for coding agents. Orca owns execution; Blackfin keeps three things outside the implementer's hands: acceptance, evidence, and review. Everything else is the model's judgment.

Route by two questions: what breaks if the change is wrong, and how strong is the available verification?

| Situation | Route |
| --- | --- |
| Local and reversible, and a focused check proves it (exact wording and static edits included) | Direct: implement, show observed evidence, done |
| Review requested or required, broad regression exposure, subjective acceptance, weak verification | Direct, then a fresh Vigil |
| Root cause or scope unclear | Structured: Atlas -> Forge -> frozen gates -> fresh Vigil |
| Irreversible or shared: auth, payment, migration, data deletion, shared-state concurrency, security, production infrastructure | Structured plus one human approval of the evaluated result |

Atlas owns WHAT and WHY, Forge writes only its assigned scope, Report turns a finished result into a self-contained HTML page, and Vigil reviews in a fresh read-only context. Roles are responsibilities, not mandatory sessions. Model strength lowers no row. The user's instructions outrank Blackfin, and a Blackfin-caused pause names the skill and line. Each run names its finish line, keeps going while no step needs the user, and stops only for a blocker, a required approval, or a destructive or out-of-scope action.

## Install

Node.js/npm is required for the installer. Structured runs additionally use the documented JSON Schema validator, Git, and Python 3 checkpoints; routine work does not require these artifact tools.

Install the stable release globally:

```bash
npx --yes skills@latest add https://github.com/HC-kang/blackfin/tree/v0.6.1 \
  --skill blackfin-atlas --skill blackfin-forge \
  --skill blackfin-vigil --skill blackfin-orchestrator \
  --skill blackfin-report \
  --agent codex claude-code --global --yes
npx --yes skills@latest list --global
```

The example targets Codex and Claude Code; replace `--agent` with your intended clients that support global installation. Project-only clients such as PromptScript cannot use `--global`.

Rerun the command to update to this release. Use the repository URL without `/tree/v0.6.1` only to follow development on `main`. Each role ships its required schemas, checkpoint, and report resources; install all five for coordinated runs. Grok Build also reads `~/.agents/skills` and `~/.claude/skills`, so it needs no separate target; cloud sessions do not receive globally installed skills.

## Use

```text
Use Blackfin to fix this input-boundary bug.
Use Blackfin / Vigil to evaluate <revision> against <contract-path>.
Use Blackfin / Report to show this run as an HTML report.
```

Direct work uses the human request as acceptance and ends with the change, the observed commands and output, and remaining gaps; no JSON, checkpoint tool, or workers. Forge audits each claim against a tool result before reporting and does not stop at a first implementation. The final report leads with what needs the user. Add a fresh Vigil for the signals above; without one, self-checks are never an independent PASS.

Structured runs pass three validated JSON artifacts: Acceptance Contract, Forge handoff, and Vigil evaluation. Mandatory gates are frozen before Forge; evidence is bound to the contract and the exact source revision; every failed gate or Vigil FAIL consumes one of two default repair cycles; a structured run cannot be downgraded around a blocker. High-risk approval binds to the evaluated revision after everything else is prepared.

Vigil starts each criterion at FAIL, probes behavior beyond the shipped tests, and reports every finding with file, line, cause, and reproduction, blocking findings first. Child agents may investigate or implement in parallel on scopes that do not overlap; each result is accepted only after its evidence is checked, and review results never become coordinator edits. State is checked before and after review.

Under Orca, read the worktree note on start or resume and replace it when it disagrees with the repository. Update it at meaningful transitions and before completion as `state: change | command → result @sha | 다음: next action`, set the card's attention flag when the user must act, and verify it saved. Chat and project memory do not replace the note.

Report builds one offline HTML file from a shipped template: verdict and unit bar first, then open decisions as a picker that composes a reply, comparison bars, a filterable table, and evidence on demand. A stdlib checker blocks text dumps, remote resources, and missing encodings, and the rendered page is checked against a short list before delivery. Pages go to `.blackfin/reports/` and their path goes into the worktree note.

See [task classification](references/task-classification.md), [evidence](references/evidence-policy.md), [handoffs](references/handoff-protocol.md), and [the Orca example](references/orca-integration.md) when relevant. Repository-local commands, conventions, and domain rules remain authoritative.

## Versioning and validation

Skill changes are behavioral releases: record them in [CHANGELOG.md](CHANGELOG.md), update `VERSION`, merge reviewed changes to `main`, then tag the tested merge commit. Never move a published tag.

v0.4 through v0.6 change skill wording and add the report skill, not artifact formats: structured artifacts still use `schemaVersion: "0.2.0"`; checkpoints remain `blackfin-checkpoint-v1`. Finish active runs with their selected rules or explicitly replace the contract.

[October evidence](references/harness-evidence-2026-10.md), [September evidence](references/harness-evidence-2026-09.md), and the earlier [harness review](references/harness-review-2026-09.md) record the research and its limits. No release claims a measured speed or quality gain on Blackfin tasks.

```bash
python3 -m unittest discover -s tests -v
```

`skills/` contains installable instructions; `references/` contains policy; `schemas/` and `scripts/` are canonical sources mirrored into the relevant role packages. Tests check schema semantics, checkpoint behavior, package drift, and skill entrypoints (portable frontmatter, size, links, note obligation).
