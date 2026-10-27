"""Regression checks for the deliberately small Decision Gate workflow contract.

These source checks are defense in depth, not an independent security boundary:
PR authors can edit them, so GitHub review requirements remain essential.
"""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def workflow_errors(text):
    errors = []
    # Limit the reviewed workflow to direct, unconditional steps. This is not a
    # general YAML parser; unexpected advanced YAML requires explicit review.
    for forbidden in ("if", "continue-on-error", "needs", "secrets", "pull_request_target", "paths", "paths-ignore", "branches-ignore"):
        if re.search(r"(?m)^\s*(?:-\s*)?[\"']?" + re.escape(forbidden) + r"[\"']?\s*:", text):
            errors.append("forbidden workflow key: " + forbidden)
    for line in text.splitlines():
        if re.search(r"(?:^|\s)[&*][A-Za-z_]", line):
            errors.append("YAML anchors/aliases require review")
    if text.count("permissions:") != 1 or not re.search(r"(?m)^permissions:\n  contents: read\n\n", text):
        errors.append("only root contents: read permissions are allowed")
    for trigger in ("pull_request", "push", "merge_group", "workflow_dispatch"):
        if not re.search(r"(?m)^  " + trigger + r":\s*$", text):
            errors.append("missing trigger " + trigger)
    actions = re.findall(r"(?m)^\s*(?:-\s*)?uses:\s*(\S+)", text)
    if not actions or any(not re.fullmatch(r"actions/checkout@[0-9a-f]{40}", action) for action in actions):
        errors.append("checkout must use a full commit SHA")
    for required in ("name: decision-gate", "persist-credentials: false", "fetch-depth: 0",
                     "python3 -B scripts/run_decision_gate_tests.py",
                     'python3 -B scripts/check_decisions.py --root . --base-ref "$BASE_SHA"',
                     "github.event.pull_request.base.sha", "github.event.merge_group.base_sha", "github.event.before"):
        if required not in text:
            errors.append("missing workflow contract: " + required)
    return errors


class WorkflowTests(unittest.TestCase):
    def test_current_workflow_contract(self):
        text = (ROOT / ".github/workflows/decision-gate.yml").read_text()
        self.assertEqual(workflow_errors(text), [])

    def test_unsafe_workflow_mutations_are_rejected(self):
        text = (ROOT / ".github/workflows/decision-gate.yml").read_text()
        changes = [
            text.replace("steps:", "if: false\n    steps:"),
            text.replace("contents: read", "contents: write"),
            text.replace("pull_request:", "pull_request_target:"),
            re.sub(r"actions/checkout@[0-9a-f]{40}", "actions/checkout@v7", text),
            text.replace("fetch-depth: 0", "fetch-depth: 1"),
            text.replace("merge_group:", "removed_merge_group:"),
            text.replace("pull_request:", "pull_request:\n    paths: [docs/**]"),
            text.replace("steps:", "continue-on-error: true\n    steps:"),
            text.replace("scripts/run_decision_gate_tests.py", "-c 'pass'"),
        ]
        for candidate in changes:
            with self.subTest(candidate=candidate):
                self.assertTrue(workflow_errors(candidate))

    def test_all_workflow_actions_are_pinned(self):
        for path in (ROOT / ".github/workflows").iterdir():
            if path.suffix in {".yml", ".yaml"}:
                for action in re.findall(r"(?m)^\s*(?:-\s*)?uses:\s*(\S+)", path.read_text()):
                    self.assertRegex(action, r"^[\w.-]+/[\w./-]+@[0-9a-f]{40}$")

    def test_codeowners_covers_entire_governance_surface(self):
        owners = (ROOT / ".github/CODEOWNERS").read_text()
        for pattern in ("/.github/workflows/", "/scripts/", "/tests/", "/docs/decisions/", "/.github/CODEOWNERS"):
            self.assertIn(pattern + " @superdusto @justdustn", owners)


class TestRunnerTests(unittest.TestCase):
    def invoke(self, files):
        with tempfile.TemporaryDirectory() as tmp:
            for name, content in files.items():
                (Path(tmp) / name).write_text(content)
            return subprocess.run([sys.executable, "-B", str(ROOT / "scripts/run_decision_gate_tests.py"),
                                   "--tests-dir", tmp], text=True, capture_output=True)

    def fixture(self, body="self.assertTrue(True)"):
        content = "import unittest\nclass Sample(unittest.TestCase):\n    def test_case(self):\n        " + body + "\n"
        return {name: content for name in ("test_decision_gate.py", "test_decision_gate_workflow.py")}

    def test_positive_suite_runs(self):
        result = self.invoke(self.fixture())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ran 2 tests", result.stderr)

    def test_missing_or_renamed_module_fails(self):
        for files in ({}, {"test_renamed.py": ""}):
            self.assertNotEqual(self.invoke(files).returncode, 0)

    def test_empty_required_module_fails_even_with_other_tests(self):
        files = self.fixture()
        files["test_decision_gate.py"] = ""
        self.assertNotEqual(self.invoke(files).returncode, 0)

    def test_import_failure_fails(self):
        files = self.fixture()
        files["test_decision_gate.py"] = "raise ImportError('deliberate fixture')"
        self.assertNotEqual(self.invoke(files).returncode, 0)

    def test_failed_and_skipped_tests_fail(self):
        for body in ("self.fail('deliberate fixture')", "self.skipTest('deliberate fixture')"):
            self.assertNotEqual(self.invoke(self.fixture(body)).returncode, 0)


if __name__ == "__main__":
    unittest.main()
