# Blackfin

Blackfin is a version-controlled engineering protocol for running coding agents through Orca. It separates planning, implementation, and independent evaluation without coupling any role to a model provider.

| Role | Owns | Must not own |
| --- | --- | --- |
| **Atlas** | Problem boundary and Acceptance Contract | Production implementation |
| **Forge** | Implementation and deterministic checks | Acceptance criteria or final acceptance |
| **Vigil** | Independent, evidence-based PASS/FAIL | Implementation changes |

The normal flow is:

```text
Atlas -> Forge -> deterministic gates -> Vigil
                    ^                  |
                    +------ FAIL ------+
```

A PASS ends automated iteration. High-risk work, and any run configured to require it, then waits for human review.

## Install

Install all four skills globally from the latest development state:

```bash
npx --yes skills@latest add https://github.com/HC-kang/blackfin \
  --skill blackfin-atlas \
  --skill blackfin-forge \
  --skill blackfin-vigil \
  --skill blackfin-orchestrator \
  --global \
  --yes
```

Verify the installation:

```bash
npx --yes skills@latest list --global
```

For production use, replace the repository URL with a stable release URL such as `https://github.com/HC-kang/blackfin/tree/v0.1.0`. `main` is development state.

The skills are provider-independent. Select providers at run time, separately from roles:

```text
Atlas -> <planner-capable agent>
Forge -> <implementation-capable agent>
Vigil -> <evaluation-capable agent>
```

## Use

Start a complete run:

```text
Use Blackfin to fix the duplicate refresh-token rotation bug.
```

Or invoke one role with its artifact input:

```text
Use Blackfin / Forge. Implement the Acceptance Contract at <path>.
Use Blackfin / Vigil. Evaluate <revision> against the contract at <path>.
```

Role handoffs use JSON artifacts validated by the schemas in [`schemas/`](schemas):

- Atlas emits an Acceptance Contract.
- Forge consumes that contract and emits a Forge handoff.
- Vigil consumes the contract, repository state, diff, and runtime; it emits an evaluation.
- Conversational reasoning is not required at either handoff.

Each installed role includes its required schema. Forge and Vigil also include the canonical dirty-worktree checkpoint tool, so agents do not need the Blackfin source checkout to validate a handoff. A dirty run reserves `.blackfin/` for protocol artifacts and requires Git plus Python 3.

Without Orca, run the same roles manually in separate agent contexts and pass the files plus exact repository state between them. Orca is the preferred tracked execution layer, not a prerequisite for the artifact protocol.

See [`references/handoff-protocol.md`](references/handoff-protocol.md) for artifact flow and [`references/orca-integration.md`](references/orca-integration.md) for a concrete supervised Orca workflow.

## Task routes

| Class | Route |
| --- | --- |
| Trivial | Exact human task -> Forge -> deterministic checks -> orchestrator completion |
| Normal | Atlas -> Forge -> deterministic gates -> Vigil |
| High uncertainty | Atlas + bounded investigation -> Forge -> gates -> Vigil |
| High risk | Atlas -> optional investigation -> Forge -> gates -> Vigil -> human approval |

The orchestrator defaults to at most two Forge repair cycles after the initial implementation. Each transition from a failed mandatory gate or Vigil `FAIL` back to implementation consumes one cycle, even inside the same agent session. A run may set a different positive limit before execution; reaching it escalates to a human.

The trivial route is only for changes with no runtime, interface, data, dependency, configuration, generated-output, or security effect. It uses the exact human request instead of an Atlas contract and does not emit the non-trivial Forge handoff. Any ambiguity upgrades the task to `NORMAL`.

## Repository contents

```text
skills/       Installable role skills
references/   Detailed protocol policy
schemas/      JSON Schema 2020-12 artifact contracts
scripts/      Canonical dirty-worktree checkpoint tool
tests/        Protocol and packaging checks
CHANGELOG.md  Behavioral changes by release
VERSION       Current protocol version
```

Repository-local instructions remain authoritative for architecture, commands, conventions, and domain invariants. Effective working context is the selected Blackfin role, repository instructions, the Acceptance Contract, and the current task.

## Versioning

Blackfin uses semantic versioning. Any instruction change that can alter agent behavior is a behavioral deployment and must be recorded in [`CHANGELOG.md`](CHANGELOG.md). Stable tags are recommended for production use.

Repository checks run with:

```bash
python3 -m unittest discover -s tests -v
```
