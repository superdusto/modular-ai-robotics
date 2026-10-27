"""Negative and positive tests for the mechanical ADR validator."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_decisions import check_all  # noqa: E402

REQUIRED = ("Context", "Decision", "Alternatives", "Consequences", "Evidence and uncertainty", "Verification plan", "Revisit triggers")


def valid_metadata() -> dict:
    return {
        "schema_version": 1,
        "id": "ADR-1234",
        "title": "An independent test architecture decision",
        "status": "accepted",
        "owner": "superdusto",
        "recorded_on": "2026-10-26",
        "issue": "https://github.com/superdusto/modular-ai-robotics/issues/2",
        "impact": "high",
        "verification_state": "not_run",
        "test_evidence": [],
        "claims": [{
            "id": "C1", "kind": "documented_fact", "status": "ESTABLISHED",
            "statement": "An official source documents a specific versioned interface.",
            "scope": "Minecraft 26.1.2 running NeoForge with approved mod integration",
            "sources": ["https://docs.neoforged.net/docs/inventories/capabilities/"]
        }]
    }


def render(meta: dict, names: tuple = REQUIRED) -> str:
    return "# ADR-1234: Demonstration\n\n<!-- decision-gate\n" + json.dumps(meta, indent=2) + "\n-->\n\n" + "\n".join(f"## {n}\n\nDocument the reasoning and checks in a concrete reproducible manner.\n" for n in names)


class DecisionGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.directory = self.base / "docs/decisions"
        self.directory.mkdir(parents=True)
        self.path = self.directory / "1234-demonstration.md"
        self.meta = valid_metadata()

    def check(self, content: str | None = None) -> list[str]:
        self.path.write_text(content if content is not None else render(self.meta), encoding="utf-8")
        return check_all(self.base)

    def test_valid_accepted_but_unverified_implementation(self):
        self.assertEqual(self.check(), [])

    def test_requires_metadata(self):
        self.assertTrue(any("metadata" in s for s in self.check("# ADR\n## Context\nDocumented context here.")))

    def test_requires_matching_id(self):
        self.meta["id"] = "ADR-0001"
        self.assertTrue(any("match filename" in s for s in self.check()))

    def test_requires_sections(self):
        self.assertTrue(any("Verification plan" in s for s in self.check(render(self.meta, REQUIRED[:-2]))))

    def test_supported_claim_requires_source(self):
        self.meta["claims"][0]["sources"] = []
        self.assertTrue(any("sources is required" in s for s in self.check()))

    def test_unverified_claim_can_have_no_source(self):
        self.meta["claims"][0]["status"] = "UNVERIFIED"
        self.meta["claims"][0]["sources"] = []
        self.assertEqual(self.check(), [])

    def test_not_available_requires_source(self):
        self.meta["claims"][0]["status"] = "NOT AVAILABLE"
        self.meta["claims"][0]["sources"] = []
        self.assertTrue(self.check())

    def test_passed_test_requires_test_evidence(self):
        self.meta["verification_state"] = "passed"
        self.assertTrue(any("test_evidence" in s for s in self.check()))

    def test_rejects_invalid_date(self):
        self.meta["recorded_on"] = "2026-02-31"
        self.assertTrue(any("real ISO" in s for s in self.check()))

    def test_rejects_untrusted_ftp_source(self):
        self.meta["claims"][0]["sources"] = ["ftp://example.com/foo"]
        self.assertTrue(any("sources must" in s for s in self.check()))

    def test_requires_real_issue_link(self):
        self.meta["issue"] = "https://github.com/someone/else/issues/2"
        self.assertTrue(any("numbered issue" in s for s in self.check()))

    def test_cannot_mark_nonexistent_successor(self):
        self.meta["status"] = "superseded"
        self.meta["superseded_by"] = "ADR-1999"
        self.assertTrue(any("existing unique ADR" in s for s in self.check()))


if __name__ == "__main__":
    unittest.main()