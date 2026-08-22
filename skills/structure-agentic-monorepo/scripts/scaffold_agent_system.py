#!/usr/bin/env python3
"""Safely scaffold a draft coordinated agent-team operating system."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


TEAMS = (
    ("product", "Product", "product_lead", "workspace-write"),
    ("backend-data-ai", "Backend, Data and AI", "backend_data_ai", "workspace-write"),
    ("frontend", "Frontend", "frontend_engineer", "workspace-write"),
    ("design-research", "Design and User Research", "design_researcher", "workspace-write"),
    ("marketing-growth", "Marketing and Growth", "marketing_growth", "workspace-write"),
    ("quality", "Quality and Evaluation", "quality_evaluator", "workspace-write"),
    ("platform-security", "Platform and Security", "platform_security", "workspace-write"),
    ("domain-review", "Domain Review", "domain_reviewer", "read-only"),
)


def build_files(project: str, owner: str) -> dict[str, str]:
    files: dict[str, str] = {}
    team_records: list[dict[str, str]] = []
    for team_id, title, agent_name, sandbox in TEAMS:
        charter_path = f"teams/{team_id}.md"
        agent_path = f".codex/agents/{team_id}.toml"
        team_records.append(
            {
                "id": team_id,
                "charter": charter_path,
                "agent": agent_path,
                "agent_name": agent_name,
                "sandbox_mode": sandbox,
            }
        )
        files[f"docs/agent-system/{charter_path}"] = charter(title, team_id, agent_name)
        files[agent_path] = agent_profile(title, agent_name, team_id, sandbox)

    coordination_agents = [
        {
            "agent": ".codex/agents/mission-integrator.toml",
            "agent_name": "mission_integrator",
            "sandbox_mode": "workspace-write",
        },
        {
            "agent": ".codex/agents/adversarial-reviewer.toml",
            "agent_name": "adversarial_reviewer",
            "sandbox_mode": "read-only",
        },
    ]
    required = [
        "docs/agent-system/README.md",
        "docs/agent-system/constitution.md",
        "docs/agent-system/interactions.md",
        "docs/agent-system/ownership.md",
        "docs/agent-system/decision-rights.md",
        "docs/agent-system/definition-of-done.md",
        "docs/agent-system/permissions.md",
        "docs/agent-system/evaluation.md",
        "docs/agent-system/decision-status.md",
        "docs/agent-system/templates/mission-brief.md",
        "docs/agent-system/templates/handoff.md",
        "docs/agent-system/templates/decision-request.md",
        "docs/agent-system/templates/adversarial-review.md",
        ".codex/config.toml",
    ]
    catalog = {
        "schema_version": "agent-team-catalog.v1",
        "project": project,
        "human_owner": owner,
        "review_triggers": ["always", "affected_capability", "contract_change"],
        "dynamic_reviewers": ["$affected_capability_teams"],
        "local_instructions": ["AGENTS.md"],
        "teams": team_records,
        "coordination_agents": coordination_agents,
        "capabilities": [
            {"id": team_id, "team": team_id}
            for team_id, _, _, _ in TEAMS
        ],
        "path_ownership": [
            {
                "id": "agent-governance",
                "paths": [
                    "AGENTS.md",
                    ".codex/**",
                    "docs/agent-system/**",
                    "tools/agent_governance/**",
                ],
                "primary_team": "product",
                "review_rules": [
                    {
                        "when": "always",
                        "reviewers": ["quality", "platform-security"],
                    }
                ],
            }
        ],
        "routing_fixtures": [
            {
                "route": "agent-governance",
                "path": ".codex/agents/product.toml",
                "triggers": [],
                "primary_team": "product",
                "reviewers": ["platform-security", "quality"],
            }
        ],
        "required_artifacts": required,
    }
    files["docs/agent-system/catalog.json"] = json.dumps(catalog, indent=2) + "\n"
    files["docs/agent-system/README.md"] = index(project)
    files["docs/agent-system/constitution.md"] = constitution(project)
    files["docs/agent-system/interactions.md"] = interactions()
    files["docs/agent-system/ownership.md"] = ownership()
    files["docs/agent-system/decision-rights.md"] = decision_rights(owner)
    files["docs/agent-system/definition-of-done.md"] = definition_of_done()
    files["docs/agent-system/permissions.md"] = permissions(owner)
    files["docs/agent-system/evaluation.md"] = evaluation()
    files["docs/agent-system/decision-status.md"] = decision_status()
    files["docs/agent-system/templates/mission-brief.md"] = mission_template()
    files["docs/agent-system/templates/handoff.md"] = handoff_template()
    files["docs/agent-system/templates/decision-request.md"] = decision_template()
    files["docs/agent-system/templates/adversarial-review.md"] = review_template()
    files[".codex/agents/mission-integrator.toml"] = coordination_profile(
        "mission_integrator",
        "Integrates cross-functional mission outputs into one coherent change.",
        "workspace-write",
        "Read docs/agent-system/interactions.md and the exact mission-brief path "
        "supplied by the parent. Integrate seams and require independent review.",
    )
    files[".codex/agents/adversarial-reviewer.toml"] = coordination_profile(
        "adversarial_reviewer",
        "Independently challenges scope, permissions, seams, instructions and evidence.",
        "read-only",
        "Read docs/agent-system/evaluation.md and the exact mission-brief path "
        "supplied by the parent. Inspect raw artifacts, report findings and do not edit.",
    )
    files[".codex/config.toml"] = "[agents]\nenabled = true\nmax_concurrent_threads_per_session = 4\n"
    files["AGENTS.agent-team.fragment.md"] = root_fragment()
    return files


def charter(title: str, team_id: str, agent_name: str) -> str:
    return f"""# {title} team charter

Team ID: `{team_id}`  
Agent: `{agent_name}`  
Status: draft for repository-specific customization

## Mission

Own one durable capability outcome while improving the integrated product.

## Stewardship

List the real paths, public interfaces, quality responsibilities and service expectations this team maintains.

## Decision rights

Choose reversible, in-scope implementation details. Record cross-team, architectural, permission or hard-to-reverse decisions through the repository's decision process.

## Non-responsibilities

Do not own adjacent specialties, human-only approvals or the whole end-to-end outcome alone.

## Inputs

Require an outcome, acceptance criteria, relevant decisions, upstream contracts and risk context.

## Outputs

Return reviewable artifacts, validation evidence, affected seams, decisions and remaining uncertainty.

## Required collaboration

Name affected teams, choose collaboration/service/facilitation explicitly and time-box high-bandwidth work.

## Quality bar

Apply the shared Definition of Done and add evidence specific to this capability.

## Escalate when

Escalate conflicting authority, unowned seams, permission expansion, unsafe actions, missing evidence or human-only decisions.
"""


def agent_profile(title: str, name: str, team_id: str, sandbox: str) -> str:
    return f'''name = "{name}"
description = "Handles bounded {title} work under the project operating model."
sandbox_mode = "{sandbox}"
developer_instructions = """
Read the root instructions and docs/agent-system/teams/{team_id}.md before acting.
Stay inside the assigned mission scope, surface affected seams early, and return validation evidence.
Do not drift into adjacent decision rights or simulate human approval.
"""
'''


def coordination_profile(
    name: str,
    description: str,
    sandbox: str,
    instructions: str,
) -> str:
    return f'''name = "{name}"
description = "{description}"
sandbox_mode = "{sandbox}"
developer_instructions = """
{instructions}
"""
'''


def index(project: str) -> str:
    return f"""# {project} agent-team operating system

Status: draft for customization

Use capability teams for durable expertise and temporary mission crews for cross-functional outcomes. Start with the constitution, then route work through the catalog, relevant charters, interaction modes, decision rights, permissions, shared Definition of Done and evaluations.

Ownership means stewardship and review responsibility, never exclusive edit access. Integrate this system through a concise root `AGENTS.md` router and the repository's existing validation command. The scaffold maps governance files only; inspect the repository and replace that draft with real product/application routes and one fixture per route before accepting the system.
"""


def constitution(project: str) -> str:
    return f"""# {project} shared constitution

Status: draft for customization

- Optimize for one shared product outcome, not team-local task count.
- Treat accepted product and architecture records as authority and mark hypotheses explicitly.
- Use evidence over preference and preserve user work.
- Keep agent autonomy inside task-scoped, least-privilege boundaries.
- Express cross-team seams through owned contracts or reviewable artifacts.
- Require independent review proportional to risk.
- Prefer clearer contracts, tools, fixtures and checks over permanent instruction growth.
"""


def interactions() -> str:
    return """# Team interactions

Status: draft for customization

- Collaboration: time-bounded, high-bandwidth discovery or implementation.
- X-as-a-Service: a stable interface consumed with minimal coordination.
- Facilitation: temporary capability transfer or obstacle removal.

Every cross-team mission names one outcome, one decision owner, participating teams, non-overlapping scopes, seams, acceptance criteria, an integrator, an independent reviewer and an end condition.
"""


def ownership() -> str:
    return """# Ownership and seams

Status: draft for customization

Map each real path and public interface to a primary steward, affected consumers and required review triggers. Ownership creates maintenance and support responsibility; it never forbids contributions through the review process. Stop implementation when adjacent areas have owners but their seam does not.
"""


def decision_rights(owner: str) -> str:
    return f"""# Decision rights and escalation

Status: draft for customization

Assign one owner for product, design, architecture, contracts, claims, security/privacy and release decisions. Consultation provides evidence rather than ceremonial unanimity. Escalate regulated, clinical, destructive, sensitive-data, permission-expanding and external-system actions to `{owner}` or another qualified human.
"""


def definition_of_done() -> str:
    return """# Shared Definition of Done

Status: draft for customization

A change is complete only when the integrated outcome, affected seams, tests, documentation, security/privacy, accessibility, provenance and repository-supported checks are complete. Reviewers identify their lens and classify findings as blocking, required or advisory.
"""


def permissions(owner: str) -> str:
    return f"""# Agent permissions

Status: draft for customization

Allow repository reads and scoped edits by default. Require the repository's documented command interface for execution. Require `{owner}` approval for external writes, deployment, sensitive data, destructive actions or permission expansion. Keep independent research-only and adversarial review read-only; design/research agents may write requested repository artifacts. Never let a team approve its own permission expansion.
"""


def evaluation() -> str:
    return """# Agent-system evaluation

Status: draft for customization

Validate file structure, identifiers, charters, agent profiles, sandbox policy, ownership patterns, routing fixtures, internal links and instruction budgets mechanically. Forward-test scope adherence, consultation, refusal, escalation, integration and unsafe side effects with golden and adversarial scenarios. Grade outcomes, not exact prose.
"""


def decision_status() -> str:
    return """# Decision status register

Status: active

List current accepted decisions, proposals, experiments, superseded directions and the next human or evidence gate. Keep mutable status here instead of duplicating it in root instructions.
"""


def mission_template() -> str:
    return """# Mission brief: <user outcome>

Status: proposed | active | blocked | complete
Decision owner: <one owner>
Integrator: <agent/person>

## Outcome and evidence

Separate observable value, known evidence and hypotheses.

## Scope, teams and interactions

Name non-overlapping scopes, interaction modes, artifacts and end conditions.

## Seams, review triggers and permissions

Name each boundary, steward, consumer, routing trigger and human-only action.

## Acceptance and validation

Apply the shared Definition of Done and name rollback and adversarial evidence.
"""


def handoff_template() -> str:
    return """# Mission handoff

Record the outcome, artifacts, changed seams, decisions, validation evidence, reviewer lenses, side effects, remaining uncertainty and follow-up owners.
"""


def decision_template() -> str:
    return """# Decision request

Record one decision class, one owner, context, affected teams, evidence, viable options, consequences, human-only gate and reconsideration trigger.
"""


def review_template() -> str:
    return """# Adversarial review

Record the mission, raw artifacts inspected, independent reviewer, permissions, blocking/required/advisory findings, unsafe side effects and re-review disposition.
"""


def root_fragment() -> str:
    return """## Agent-team operating model

- Read `docs/agent-system/README.md` before delegating or changing more than one team domain.
- Route work through the catalog and relevant team charters; ownership is stewardship, not exclusive edit access.
- Use a mission brief for cross-team, contract, permission, public-claim or architectural work.
- Apply decision rights, least-privilege permissions and the shared Definition of Done.
- Require independent adversarial review proportional to risk.
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Existing repository root")
    parser.add_argument("--project", required=True, help="Human-facing project name")
    parser.add_argument("--owner", required=True, help="Human owner, e.g. @octocat")
    parser.add_argument("--write", action="store_true", help="Create files after conflict checks")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target = args.target.resolve()
    if not target.is_dir():
        print(f"ERROR: target is not an existing directory: {target}", file=sys.stderr)
        return 2
    files = build_files(args.project.strip(), args.owner.strip())
    conflicts = sorted(path for path in files if (target / path).exists())
    if conflicts:
        for path in conflicts:
            print(f"CONFLICT: {path}", file=sys.stderr)
        print("Refusing to overwrite existing files.", file=sys.stderr)
        return 3
    for path in sorted(files):
        print(f"CREATE: {path}")
    if not args.write:
        print("Dry run only. Re-run with --write after reviewing the paths.")
        return 0
    for relative, content in files.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"Created {len(files)} draft artifacts for {args.project.strip()}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
