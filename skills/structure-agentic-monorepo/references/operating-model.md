# Operating-model reference

## Contents

1. Artifact model
2. Team and interaction design
3. Decision and permission design
4. Validation strategy
5. Adversarial failure modes
6. Sources

## Artifact model

Use root instructions as a concise router and shared constitution. Use nested instructions only for durable path-local constraints. Store detailed charters, ownership, decision rights, permissions, status and evaluation plans in a discoverable documentation index. Use skills for repeatable procedures and scripts for deterministic, fragile operations.

A complete baseline normally contains:

- shared constitution;
- machine-readable team/capability catalog;
- one Team API/charter per durable capability;
- interaction modes and mission lifecycle;
- ownership and cross-team seam map;
- decision-rights and escalation table;
- permission matrix with human-only actions;
- shared Definition of Done and review severity language;
- decision-status register;
- static checks plus behavioral golden/adversarial evaluations;
- mission, decision, handoff and adversarial-review templates.

## Team and interaction design

Prefer teams aligned to a value stream or durable capability over teams named only after repository layers. When functional capability teams are useful for delegation, deliver important work through a temporary cross-functional mission crew.

Define each team by mission, stewardship, decision rights, non-responsibilities, inputs, outputs, required collaboration, quality bar and escalation triggers. Give it one primary cognitive responsibility and a bounded service surface.

Name every relationship as one of:

- collaboration for a time-bounded discovery or implementation interval;
- X-as-a-Service for a stable low-coordination interface;
- facilitation for temporary capability transfer.

Treat indefinite collaboration as evidence that a contract, tool, boundary or team design needs improvement.

## Decision and permission design

Assign one decision owner by decision class. Require advice from materially affected specialists, not unanimous consensus. Escalate regulated, clinical, destructive, sensitive-data, permission-expanding or external-system actions to a qualified human.

Ownership means stewardship, support and review responsibility. It does not imply exclusive editing rights. Protect ownership and permission definitions themselves.

Use least privilege. Match read/write/network/tool access to the delegated job. Keep independent research-only and adversarial reviewers read-only; a design/research agent may write requested repository artifacts. Do not let a team approve its own permission expansion.

## Validation strategy

Static checks should validate file presence, identifiers, supported TOML fields, sandbox policy, agent/catalog agreement, configuration, charter headings, path-pattern grammar, routing fixtures, contract/capability mappings, nested instructions, internal links, placeholders and instruction-size budgets. Give every governed path route one concrete fixture so a prose/catalog contradiction cannot pass unnoticed.

Behavioral evaluations should test scope adherence, consultation, refusal, escalation, handoff and integration. Grade outcomes and side effects rather than exact wording. Re-run evaluations after material instruction, skill, tool, permission or model changes.

## Adversarial failure modes

Challenge at least these risks:

1. Functional conveyor belt with no owner of the user outcome.
2. Team-local optimization that breaks the integrated feature.
3. Ownership monarchy that creates queues and knowledge silos.
4. Circular vetoes and no named decision owner.
5. Permanent collaboration because a stable interface never emerges.
6. Unowned contract or integration seam.
7. Architecture and permissions recorded only in Markdown, without checks.
8. Duplicated or contradictory root and local instructions.
9. Happy-path evaluation that ignores unsafe side effects or hostile inputs.
10. Reviewer monoculture that produces false independent confidence.
11. Metrics optimized for task count rather than user value and reliability.
12. Rules added after every failure until context becomes stale and contradictory.
13. Proposed research treated as accepted product or architecture.
14. Agents simulating legal, security or external-system approval.
15. A machine-readable router that drops conditional reviewers or uses patterns no tool interprets.
16. A decision class naming several possible owners instead of one deterministic owner.

## Sources

- [OpenAI: custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [OpenAI: subagents and project-scoped custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [OpenAI: build skills](https://learn.chatgpt.com/docs/build-skills)
- [Team Topologies: key concepts](https://teamtopologies.com/key-concepts)
- [Team Topologies: Team API template](https://github.com/TeamTopologies/Team-API-template)
- [Google Engineering Practices: code-review standard](https://google.github.io/eng-practices/review/reviewer/standard.html)
- [GitHub: CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Nx: enforce module boundaries](https://nx.dev/docs/features/enforce-module-boundaries)
