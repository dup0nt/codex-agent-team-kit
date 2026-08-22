# Codex Agent Team Kit

A personal, reusable skill and rule baseline for turning a monorepo into a coordinated agent-team environment without organizing source code by department.

## Contents

- `skills/structure-agentic-monorepo/` — workflow, templates and deterministic helpers.
- `rules/agentic-monorepo-baseline.md` — optional universal rules to adapt into a repository's root `AGENTS.md`.
- `tests/` — safety tests for the scaffold and validator.

## Install locally

Codex discovers personal skills under `$HOME/.agents/skills`. Symlink the skill directory there so this Git repository remains the editable source of truth:

```sh
mkdir -p "$HOME/.agents/skills"
ln -s "$(pwd)/skills/structure-agentic-monorepo" "$HOME/.agents/skills/structure-agentic-monorepo"
```

Invoke it with `$structure-agentic-monorepo`. Run `make check` before pushing changes.

The bundled scaffold is deliberately a draft: it creates governance artifacts, coordination profiles, templates, a documented routing grammar and one governance-route fixture without creating product source. The skill must inspect the target and replace the generic team/path map with repository-specific capabilities and routing fixtures before the operating model is accepted.
