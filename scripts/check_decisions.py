#!/usr/bin/env python3
"""Validate machine-checkable architecture decision records (standard library only).

This tool verifies document structure, metadata, declared evidence provenance,
and verification bookkeeping. It cannot establish technical truth or approval.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

PATTERN = re.compile(r"<!--\s*decision-gate\s*\n(.*?)\n\s*-->", re.DOTALL)
HEADINGS = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
FILENAME = re.compile(r"^(\d{4})-[a-z0-9][a-z0-9-]*\.md$")
ISSUE = re.compile(r"^https://github\.com/superdusto/modular-ai-robotics/issues/[1-9][0-9]*$")
REQUIRED_SECTIONS = (
    "Context", "Decision", "Alternatives", "Consequences",
    "Evidence and uncertainty", "Verification plan", "Revisit triggers",
)
EVIDENCE_STATUSES = {"ESTABLISHED", "CONDITIONAL", "UNVERIFIED", "NOT AVAILABLE"}
VERIFICATION_STATES = {"not_run", "passed", "not_applicable"}
DECISION_STATUSES = {"proposed", "accepted", "superseded"}
CLAIM_KINDS = {"documented_fact", "source_observation", "runtime_observation", "inference", "risk", "requirement"}


def valid_https(value: object) -> bool:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        return False
    try:
        p = urlparse(value)
    except ValueError:
        return False
    return p.scheme == "https" and bool(p.hostname) and p.username is None and p.password is None and not any(x.isspace() for x in value)


def substantial(value: object) -> bool:
    if not isinstance(value, str):
        return False
    s = value.strip()
    return len(s) >= 20 and s.lower() not in {"tbd", "todo", "none", "n/a", "placeholder", "fill in"}


def check_record(path: Path, base: Path) -> list[str]:
    errors: list[str] = []

    def fail(message: str) -> None:
        errors.append(f"{path.relative_to(base)}: {message}")

    m = FILENAME.fullmatch(path.name)
    if not m:
        return [f"{path.relative_to(base)}: ADR filename must be NNNN-kebab-case.md"]
    text = path.read_text(encoding="utf-8")
    matches = list(PATTERN.finditer(text))
    if len(matches) != 1:
        fail("expected exactly one <!-- decision-gate ... --> JSON metadata block")
        return errors
    block = matches[0]
    if block.start() > 500:
        fail("metadata block must be near the top (within first 500 characters)")
    try:
        meta = json.loads(block.group(1))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON metadata: {exc.msg}")
        return errors
    if not isinstance(meta, dict):
        fail("metadata must be a JSON object")
        return errors
    keys = {"schema_version", "id", "title", "status", "owner", "recorded_on", "issue", "impact", "verification_state", "test_evidence", "claims"}
    missing = sorted(keys - set(meta))
    if missing:
        fail("missing metadata keys: " + ", ".join(missing))
    if meta.get("schema_version") != 1 or type(meta.get("schema_version")) is not int:
        fail("schema_version must be integer 1")
    if meta.get("id") != f"ADR-{m.group(1)}":
        fail(f"id must match filename: ADR-{m.group(1)}")
    if not substantial(meta.get("title")):
        fail("title must explain the decision (>=20 characters)")
    if meta.get("status") not in DECISION_STATUSES:
        fail("status must be proposed, accepted or superseded")
    if not isinstance(meta.get("owner"), str) or not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", meta["owner"]):
        fail("owner must be a GitHub username")
    try:
        dt.date.fromisoformat(meta.get("recorded_on", ""))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["recorded_on"]):
            raise ValueError("invalid format")
    except (ValueError, TypeError):
        fail("recorded_on must be a real ISO YYYY-MM-DD date")
    if not isinstance(meta.get("issue"), str) or not ISSUE.fullmatch(meta["issue"]):
        fail("issue must be a link to a numbered issue in this repository")
    if meta.get("impact") not in {"low", "medium", "high"}:
        fail("impact must be low, medium or high")
    verification_state = meta.get("verification_state")
    if verification_state not in VERIFICATION_STATES:
        fail("verification_state must be not_run, passed or not_applicable")
    test_evidence = meta.get("test_evidence")
    if not isinstance(test_evidence, list) or any(not valid_https(v) for v in test_evidence):
        fail("test_evidence must be a list of HTTPS URLs (possibly empty)")
    if verification_state == "passed" and not test_evidence:
        fail("verification_state=passed needs at least one test_evidence URL")
    if meta.get("status") == "superseded":
        target = meta.get("superseded_by")
        if not isinstance(target, str) or not re.fullmatch(r"ADR-\d{4}", target) or target == meta.get("id"):
            fail("superseded decisions need a distinct superseded_by ADR-NNNN")
        else:
            successor = list((base / "docs/decisions").glob(target[4:] + "-*.md"))
            if len(successor) != 1:
                fail("superseded_by must identify an existing unique ADR file")
    claims = meta.get("claims")
    if not isinstance(claims, list) or not claims:
        fail("claims must contain at least one classified material claim")
    else:
        identifiers: set[str] = set()
        for i, claim in enumerate(claims, 1):
            where = f"claims[{i}]"
            if not isinstance(claim, dict):
                fail(where + " must be an object")
                continue
            cid = claim.get("id")
            if not isinstance(cid, str) or not re.fullmatch(r"C[1-9]\d*", cid) or cid in identifiers:
                fail(where + ".id must be a unique C1-style claim ID")
            else:
                identifiers.add(cid)
            if claim.get("kind") not in CLAIM_KINDS:
                fail(where + ".kind is not a supported claim kind")
            status = claim.get("status")
            if status not in EVIDENCE_STATUSES:
                fail(where + ".status must be ESTABLISHED, CONDITIONAL, UNVERIFIED or NOT AVAILABLE")
            if not substantial(claim.get("statement")):
                fail(where + ".statement must be substantial")
            if not substantial(claim.get("scope")):
                fail(where + ".scope must identify the relevant environment and boundary")
            sources = claim.get("sources")
            if not isinstance(sources, list) or any(not valid_https(s) for s in sources):
                fail(where + ".sources must be a list of HTTPS URLs")
            elif status in {"ESTABLISHED", "CONDITIONAL", "NOT AVAILABLE"} and not sources:
                fail(where + ".sources is required for a supported or negative claim")
            # URLs are *not* dereferenced: document validity is not evidence truth.
    sections: dict[str, str] = {}
    hits = list(HEADINGS.finditer(text))
    for i, hit in enumerate(hits):
        name = hit.group(1).strip()
        if name in sections:
            fail(f"duplicate H2 heading: {name}")
        sections[name] = text[hit.end():hits[i + 1].start() if i + 1 < len(hits) else len(text)].strip()
    for name in REQUIRED_SECTIONS:
        if name not in sections:
            fail("missing required section: ## " + name)
        elif not substantial(sections[name]):
            fail(f"section {name} needs meaningful content (>=20 characters)")
    return errors


def check_all(base: Path) -> list[str]:
    directory = base / "docs" / "decisions"
    if not directory.is_dir():
        return ["docs/decisions directory is required"]
    paths = sorted(p for p in directory.glob("*.md") if p.name not in {"README.md", "TEMPLATE.md"})
    if not paths:
        return ["no numbered Architecture Decision Records found"]
    errors: list[str] = []
    for path in paths:
        errors.extend(check_record(path, base))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = check_all(args.root.resolve())
    if errors:
        for error in errors:
            print("ERROR: " + error, file=sys.stderr)
        print(f"Decision Gate FAIL ({len(errors)} problems)", file=sys.stderr)
        return 1
    print("Decision Gate PASS: every ADR meets the machine-checkable document contract")
    print("NOTE: this does not verify external facts, semantic correctness or human approval")
    return 0


if __name__ == "__main__":
    sys.exit(main())