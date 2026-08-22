---
name: structure-agentic-monorepo
description: Design or retrofit a coordinated agent-team operating system for a monorepo. Use when creating or changing AGENTS.md hierarchies, project-scoped Codex agents, team charters, ownership and decision rights, cross-functional mission workflows, permissions, shared quality gates, agent evaluations, or reusable governance validation. Do not use for ordinary feature implementation that does not change agent or team governance.
---

# Structure Agentic Monorepo

Build a reusable collaboration layer that gives specialized agents clear scope while keeping product delivery integrated. Preserve the target repository's accepted product and architecture decisions.

## Workflow

1. Inspect the target repository's worktree, root instructions, product specification, accepted decision records, layout, ownership and supported command interface. Preserve user changes.
2. Identify value streams, durable capabilities, shared seams and human-only decisions before naming teams. Keep capability teams stable; use temporary mission crews for cross-functional outcomes.
3. Read [`references/operating-model.md`](references/operating-model.md) when selecting artifacts, decision rights, interaction modes, permissions or adversarial scenarios.
4. Optionally run the safe scaffold in dry-run mode, then rerun with `--write` only after reviewing the proposed paths:

   ```sh
   python scripts/scaffold_agent_system.py /path/to/repo --project "Project Name" --owner "@owner"
   python scripts/scaffold_agent_system.py /path/to/repo --project "Project Name" --owner "@owner" --write
   ```

5. Customize every generated artifact. Remove generic statements that do not match the repository. Do not reorganize product source by department or create empty app/package trees.
6. Integrate a short root instruction router. Place only truly local constraints in nested instruction files. Keep mutable decisions out of root instructions.
7. Create narrow `.codex/agents/*.toml` profiles only for useful delegation handles. Inherit the active model by default, match tool and sandbox access to the job, and keep independent reviewers read-only.
8. Define one machine-readable catalog connecting team IDs, charters, agent profiles, path stewardship, capabilities and required review relationships.
   Document one path-pattern grammar, make conditional review triggers explicit, and add one concrete routing fixture for every route.
9. Add deterministic validation to the repository's existing command catalogue. Do not introduce a runtime or task orchestrator solely for governance.
10. Run the bundled validator as a supplemental check:

    ```sh
    python scripts/validate_agent_system.py /path/to/repo
    ```

11. Forward-test cross-team routing, refusal/escalation and integration with fresh read-only subagents. Pass raw artifacts and realistic requests, not the intended answer.
12. Run the target repository's full supported checks, perform an independent adversarial review, correct findings and report any external actions.

## Required design properties

- Create a shared constitution, team charters, explicit interaction modes, ownership without exclusivity, decision rights, a permission matrix, shared Definition of Done, decision-status register and evaluation plan.
- Require a mission brief for cross-team, contract, permission, public-claim or architectural work.
- Assign each cross-team seam a steward and consumer. Prefer a contract or service over permanent collaboration.
- Separate blocking review findings from required and advisory feedback.
- Mark legal, clinical, regulated, destructive or external-system decisions as human-owned.
- Protect review-routing and permission files themselves.
- Keep instruction context small and information single-sourced.

## Templates and scripts

- Use [`assets/templates/team-charter.md`](assets/templates/team-charter.md) for consistent team APIs.
- Use [`assets/templates/mission-brief.md`](assets/templates/mission-brief.md) for cross-functional work.
- Use [`assets/templates/handoff.md`](assets/templates/handoff.md) for integrated evidence.
- Use [`assets/templates/agent.toml`](assets/templates/agent.toml) as a starting point, then narrow its instructions and permissions.
- Treat scaffold output as a draft. Refuse overwrites unless the user explicitly resolves the conflict.

## Validation gates

- Confirm every catalog reference resolves and every charter uses the canonical sections.
- Confirm custom-agent TOML parses and contains no secrets or unnecessary model pins.
- Confirm path ownership and contract identifiers map to known teams and capabilities.
- Confirm agent names/sandboxes match the catalog, project agent configuration parses, and independent review profiles are read-only.
- Confirm every path route matches exactly one fixture and computes its declared required reviewers.
- Confirm the root instruction file stays within the repository's context budget and has no mutable status duplicated from deeper docs.
- Confirm the target repository's own containerized or documented checks pass.
- Confirm at least one independent review challenges local optimization, orphaned seams, permission expansion, instruction conflicts and happy-path-only tests.
