from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "structure-agentic-monorepo" / "scripts"
SCAFFOLD = SCRIPTS / "scaffold_agent_system.py"
VALIDATE = SCRIPTS / "validate_agent_system.py"


class ScriptTests(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_script(
                SCAFFOLD, directory, "--project", "Example", "--owner", "@owner"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Dry run only", result.stdout)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_write_validate_and_refuse_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            write = self.run_script(
                SCAFFOLD,
                directory,
                "--project",
                "Example",
                "--owner",
                "@owner",
                "--write",
            )
            self.assertEqual(write.returncode, 0, write.stderr)
            root = Path(directory)
            (root / "AGENTS.md").write_text(
                "# Instructions\n\n## Agent-team operating model\n\nUse the catalog.\n",
                encoding="utf-8",
            )
            valid = self.run_script(VALIDATE, directory)
            self.assertEqual(valid.returncode, 0, valid.stderr)
            self.assertIn("8 teams, 10 agents, 8 capabilities and 1 routes", valid.stdout)
            second = self.run_script(
                SCAFFOLD,
                directory,
                "--project",
                "Example",
                "--owner",
                "@owner",
                "--write",
            )
            self.assertEqual(second.returncode, 3)
            self.assertIn("Refusing to overwrite", second.stderr)

    def test_validator_detects_review_routing_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            write = self.run_script(
                SCAFFOLD,
                directory,
                "--project",
                "Example",
                "--owner",
                "@owner",
                "--write",
            )
            self.assertEqual(write.returncode, 0, write.stderr)
            root = Path(directory)
            (root / "AGENTS.md").write_text(
                "# Instructions\n\n## Agent-team operating model\n\nUse the catalog.\n",
                encoding="utf-8",
            )
            catalog_path = root / "docs" / "agent-system" / "catalog.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["routing_fixtures"][0]["reviewers"] = []
            catalog_path.write_text(
                json.dumps(catalog, indent=2) + "\n",
                encoding="utf-8",
            )

            invalid = self.run_script(VALIDATE, directory)

            self.assertEqual(invalid.returncode, 1)
            self.assertIn("reviewers", invalid.stderr)

    def test_validator_detects_reviewer_permission_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            write = self.run_script(
                SCAFFOLD,
                directory,
                "--project",
                "Example",
                "--owner",
                "@owner",
                "--write",
            )
            self.assertEqual(write.returncode, 0, write.stderr)
            root = Path(directory)
            (root / "AGENTS.md").write_text(
                "# Instructions\n\n## Agent-team operating model\n\nUse the catalog.\n",
                encoding="utf-8",
            )
            profile = root / ".codex" / "agents" / "adversarial-reviewer.toml"
            profile.write_text(
                profile.read_text(encoding="utf-8").replace(
                    'sandbox_mode = "read-only"',
                    'sandbox_mode = "workspace-write"',
                ),
                encoding="utf-8",
            )

            invalid = self.run_script(VALIDATE, directory)

            self.assertEqual(invalid.returncode, 1)
            self.assertIn("does not match catalog", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
