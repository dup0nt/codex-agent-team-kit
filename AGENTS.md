# Agent Team Kit instructions

This private repository packages reusable guidance for coordinated agentic monorepo development.

- Keep the skill technology-neutral and concise. Product-specific rules belong in the target repository.
- Preserve progressive disclosure: core procedure in `SKILL.md`, detailed rationale in `references/`, deterministic work in `scripts/`, and output templates in `assets/`.
- Do not add model pins, tool permissions or external-service assumptions unless the reusable workflow requires them.
- Scaffold scripts must be dry-run by default, refuse overwrites and avoid creating product source directories.
- Validate the skill and run its script tests before publishing changes.
- Forward-test material workflow changes with a fresh, minimally briefed agent against a disposable repository.
