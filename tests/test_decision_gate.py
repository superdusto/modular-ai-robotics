"""Negative and positive tests for the mechanical ADR validator."""
from __future__ import annotations

import json
import sys
import subprocess
from copy import deepcopy
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
    return "# " + meta["id"] + ": Demonstration\n\n<!-- decision-gate\n" + json.dumps(meta, indent=2) + "\n-->\n\n" + "\n".join(f"## {n}\n\nDocument the reasoning and checks in a concrete reproducible manner.\n" for n in names)


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

    def test_duplicate_adr_ids(self):
        (self.directory / "1234-duplicate.md").write_text(render(self.meta))
        self.assertTrue(any("duplicate ADR ID" in e for e in self.check()))

    def test_unsupported_inventory(self):
        for name in ("1235-hidden.MD", "1235-hidden.txt", "1235-hidden.md.bak"):
            with self.subTest(name=name):
                extra = self.directory / name
                extra.write_text("malformed")
                self.assertTrue(any("filename" in e for e in self.check()))
                extra.unlink()
        nested = self.directory / "archive"
        nested.mkdir()
        (nested / "1235-hidden.md").write_text("malformed")
        self.assertTrue(any("top-level" in e for e in self.check()))

    def test_symlink_record_is_rejected(self):
        (self.directory / "1235-link.md").symlink_to(self.path)
        self.assertTrue(any("regular" in e for e in self.check()))

    def test_symlink_decision_directory_is_rejected(self):
        other = self.base / "other"
        other.mkdir()
        (other / self.path.name).write_text(render(self.meta))
        self.directory.rmdir()
        self.directory.symlink_to(other, target_is_directory=True)
        self.assertTrue(any("symbolic link" in e for e in check_all(self.base)))

    def test_duplicate_json_keys_at_every_level(self):
        text = render(self.meta)
        for old, new in (
            ('"status": "accepted"', '"status": "invalid", "status": "accepted"'),
            ('"kind": "documented_fact"', '"kind": "risk", "kind": "documented_fact"'),
        ):
            with self.subTest(old=old):
                self.assertTrue(any("duplicate JSON key" in e for e in self.check(text.replace(old, new))))

    def test_nonfinite_json_is_rejected(self):
        self.assertTrue(any("non-finite" in e for e in self.check(render(self.meta).replace('"impact": "high"', '"impact": NaN'))))

    def test_enum_types_report_errors_without_crashing(self):
        for field in ("status", "impact", "verification_state"):
            for value in ([], {}, None, 42, True):
                with self.subTest(field=field, value=value):
                    meta = deepcopy(self.meta)
                    meta[field] = value
                    self.assertTrue(self.check(render(meta)))
        for field in ("kind", "status"):
            for value in ([], {}, None, 42, True):
                with self.subTest(field=field, value=value):
                    meta = deepcopy(self.meta)
                    meta["claims"][0][field] = value
                    self.assertTrue(self.check(render(meta)))

    def test_hidden_headings_do_not_count(self):
        text = render(self.meta)
        prefix, body = text.split("## Context", 1)
        body = "## Context" + body
        for opening, closing in (("\x60\x60\x60markdown\n", "\n\x60\x60\x60"), ("~~~\n", "\n~~~"), ("<!--\n", "\n-->")):
            with self.subTest(opening=opening):
                self.assertTrue(any("missing required section" in e for e in self.check(prefix + opening + body + closing)))

    def test_comment_and_code_only_section_bodies_are_empty(self):
        text = render(self.meta)
        body = "Document the reasoning and checks in a concrete reproducible manner."
        for replacement in ("<!-- " + body + " -->", "\x60\x60\x60\n" + body + "\n\x60\x60\x60", "    " + body):
            with self.subTest(replacement=replacement):
                self.assertTrue(any("meaningful content" in e for e in self.check(text.replace(body, replacement))))

    def test_raw_html_cannot_hide_sections(self):
        text = render(self.meta).replace("## Context", '<div hidden>\n## Context') + "\n</div>"
        self.assertTrue(any("raw HTML" in e for e in self.check(text)))

    def test_visible_title_id_must_match(self):
        self.assertTrue(any("visible H1" in e for e in self.check(render(self.meta).replace("# ADR-1234:", "# ADR-9999:", 1))))

    def test_template_cannot_be_accepted_unchanged(self):
        template = Path(__file__).resolve().parents[1] / "docs/decisions/TEMPLATE.md"
        target = self.directory / "9999-copy.md"
        target.write_text(template.read_text())
        self.assertTrue(check_all(self.base))
        # Correcting the ID alone must not make the instructional body valid.
        target.write_text(template.read_text().replace("ADR-NNNN:", "ADR-9999:"))
        self.assertTrue(check_all(self.base))

    def test_repeated_filler_is_rejected(self):
        self.meta["title"] = "x" * 30
        self.assertTrue(any("title" in e for e in self.check()))

    def write_successor(self, identifier, status="accepted", target=None):
        meta = deepcopy(self.meta)
        meta.update(id=identifier, status=status)
        if target:
            meta["superseded_by"] = target
        (self.directory / (identifier[4:] + "-successor.md")).write_text(render(meta))

    def test_supersession_cycles_are_rejected(self):
        for length in (2, 3):
            with self.subTest(length=length):
                self.meta.update(status="superseded", superseded_by="ADR-1235")
                self.write_successor("ADR-1235", "superseded", "ADR-1234" if length == 2 else "ADR-1236")
                if length == 3:
                    self.write_successor("ADR-1236", "superseded", "ADR-1234")
                self.assertTrue(any("cycle" in e for e in self.check()))

    def test_successor_chain_ends_at_accepted_record(self):
        self.meta.update(status="superseded", superseded_by="ADR-1235")
        self.write_successor("ADR-1235", "superseded", "ADR-1236")
        self.write_successor("ADR-1236", "proposed")
        self.assertTrue(any("accepted ADR" in e for e in self.check()))
        self.write_successor("ADR-1236", "accepted")
        self.assertEqual(self.check(), [])

    def test_invalid_utf8_reports_error(self):
        self.path.write_bytes(b"\xff")
        self.assertTrue(any("UTF-8" in e for e in check_all(self.base)))

    def test_invalid_and_missing_base_fail_closed(self):
        self.check()
        for ref in ("main", "--help", "0" * 40):
            with self.subTest(ref=ref):
                self.assertTrue(check_all(self.base, ref))

    def test_history_preserves_existing_records(self):
        self.check()
        def git(*args):
            return subprocess.run(["git", *args], cwd=self.base, check=True,
                                  capture_output=True, text=True).stdout.strip()
        git("init", "-q")
        git("add", ".")
        git("-c", "user.name=Gate Test", "-c", "user.email=gate-test@example.invalid",
            "commit", "-qm", "baseline")
        baseline = git("rev-parse", "HEAD")
        self.write_successor("ADR-1235")
        self.assertEqual(check_all(self.base, baseline), [])
        self.path.unlink()
        self.assertTrue(any("historical ADR" in e for e in check_all(self.base, baseline)))
        self.check()
        self.path.rename(self.directory / "1234-renamed.md")
        self.assertTrue(any("historical ADR" in e for e in check_all(self.base, baseline)))



if __name__ == "__main__":
    unittest.main()