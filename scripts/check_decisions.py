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
import subprocess
from pathlib import Path
from urllib.parse import urlparse

PATTERN = re.compile(r"<!--\s*decision-gate\s*\n(.*?)\n\s*-->", re.DOTALL)
HEADINGS = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.MULTILINE)
FILENAME = re.compile(r"^([0-9]{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
ISSUE = re.compile(r"^https://github\.com/superdusto/modular-ai-robotics/issues/[1-9][0-9]*$")
REQUIRED_SECTIONS = (
    "Context", "Decision", "Alternatives", "Consequences",
    "Evidence and uncertainty", "Verification plan", "Revisit triggers",
)
EVIDENCE_STATUSES = {"ESTABLISHED", "CONDITIONAL", "UNVERIFIED", "NOT AVAILABLE"}
VERIFICATION_STATES = {"not_run", "passed", "not_applicable"}
DECISION_STATUSES = {"proposed", "accepted", "superseded"}
CLAIM_KINDS = {"documented_fact", "source_observation", "runtime_observation", "inference", "risk", "requirement"}

# Template instructions are not decision-specific content.
TEMPLATE_TEXT = {
    "Replace this line with a specific decision title",
    "State one material and version-scoped factual claim that needs checking.",
    "Name the exact Minecraft version, mod/API and applicable runtime boundary.",
    "Describe the problem, user goal, dependencies, constraints and why a decision is required.",
    "State the owner-selected decision or, if proposed, the candidate choice and exact scope.",
    "Record realistic alternatives, why they were considered and why they are not selected.",
    "Describe advantages, costs, backward compatibility, maintenance and failure behavior.",
    "For each material claim in metadata, explain its source, the date/version it governs, what remains unverified, and any nontransferable assumptions.",
    "Specify a testable acceptance criterion, dependencies and how the expected result will be demonstrated. Use \x60verification_state=not_run\x60 until evidence from an actual test exists.",
    "Identify concrete changes or test failures that would justify superseding this decision.",
}


def unique_object(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def load_metadata(text: str) -> dict:
    blocks = list(PATTERN.finditer(text))
    if len(blocks) != 1:
        raise ValueError("expected exactly one <!-- decision-gate ... --> JSON metadata block")
    result = json.loads(blocks[0].group(1), object_pairs_hook=unique_object,
                        parse_constant=reject_constant)
    if not isinstance(result, dict):
        raise ValueError("metadata must be a JSON object")
    return result


def visible_prose(text: str) -> str:
    """Extract supported ADR prose, excluding comments and code blocks.

    Raw HTML in the remaining prose is rejected by check_record. This limited
    Markdown contract deliberately does not claim to be a complete renderer.
    """
    text = re.sub(r"<!--.*?(?:-->|\Z)", "", text, flags=re.DOTALL)
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(\x60{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            lines.append("")
        elif marker:
            fence = marker[1]
            lines.append("")
        elif line.startswith(("    ", "\t")):
            lines.append("")
        else:
            lines.append(line)
    return "\n".join(lines)


def member(value: object, choices: set[str]) -> bool:
    return isinstance(value, str) and value in choices



def valid_https(value: object) -> bool:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        return False
    try:
        p = urlparse(value)
        p.port  # Reject malformed ports.
    except ValueError:
        return False
    return p.scheme == "https" and bool(p.hostname) and p.username is None and p.password is None and not any(x.isspace() for x in value)


def substantial(value: object) -> bool:
    if not isinstance(value, str):
        return False
    s = value.strip()
    normalized = " ".join(s.split())
    return (len(s) >= 20 and normalized not in TEMPLATE_TEXT
            and len(set(c.lower() for c in s if c.isalnum())) >= 4
            and not re.fullmatch(r"(?i)(?:todo|tbd|placeholder|fill in|[\W_])+", s))


def check_record(path: Path, base: Path) -> list[str]:
    errors: list[str] = []

    def fail(message: str) -> None:
        errors.append(f"{path.relative_to(base)}: {message}")

    m = FILENAME.fullmatch(path.name)
    if not m:
        return [f"{path.relative_to(base)}: ADR filename must be NNNN-kebab-case.md"]
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"cannot read UTF-8 ADR: {exc}")
        return errors
    matches = list(PATTERN.finditer(text))
    if len(matches) != 1:
        fail("expected exactly one <!-- decision-gate ... --> JSON metadata block")
        return errors
    block = matches[0]
    if block.start() > 500:
        fail("metadata block must be near the top (within first 500 characters)")
    try:
        meta = load_metadata(text)
    except (ValueError, RecursionError) as exc:
        fail(f"invalid JSON metadata: {exc}")
        return errors
    if not isinstance(meta, dict):
        fail("metadata must be a JSON object")
        return errors
    keys = {"schema_version", "id", "title", "status", "owner", "recorded_on", "issue", "impact", "verification_state", "test_evidence", "claims"}
    missing = sorted(keys - set(meta))
    unknown = sorted(set(meta) - keys - {"superseded_by"})
    if unknown:
        fail("unknown metadata keys: " + ", ".join(unknown))
    if missing:
        fail("missing metadata keys: " + ", ".join(missing))
    if meta.get("schema_version") != 1 or type(meta.get("schema_version")) is not int:
        fail("schema_version must be integer 1")
    if meta.get("id") != f"ADR-{m.group(1)}":
        fail(f"id must match filename: ADR-{m.group(1)}")
    if not substantial(meta.get("title")):
        fail("title must explain the decision (>=20 characters)")
    if not member(meta.get("status"), DECISION_STATUSES):
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
    if not member(meta.get("impact"), {"low", "medium", "high"}):
        fail("impact must be low, medium or high")
    verification_state = meta.get("verification_state")
    if not member(verification_state, VERIFICATION_STATES):
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
            if not member(claim.get("kind"), CLAIM_KINDS):
                fail(where + ".kind is not a supported claim kind")
            status = claim.get("status")
            if not member(status, EVIDENCE_STATUSES):
                fail(where + ".status must be ESTABLISHED, CONDITIONAL, UNVERIFIED or NOT AVAILABLE")
            if not substantial(claim.get("statement")):
                fail(where + ".statement must be substantial")
            if not substantial(claim.get("scope")):
                fail(where + ".scope must identify the relevant environment and boundary")
            sources = claim.get("sources")
            if not isinstance(sources, list) or any(not valid_https(s) for s in sources):
                fail(where + ".sources must be a list of HTTPS URLs")
            elif member(status, {"ESTABLISHED", "CONDITIONAL", "NOT AVAILABLE"}) and not sources:
                fail(where + ".sources is required for a supported or negative claim")
            # URLs are *not* dereferenced: document validity is not evidence truth.
    prose = visible_prose(text)
    if re.search(r"</?[A-Za-z][^>]*>", prose):
        fail("raw HTML is not supported in ADR prose")
    titles = re.findall(r"^#[ \t]+ADR-([0-9]{4}):[ \t]+(.+)$", prose, re.MULTILINE)
    if len(titles) != 1 or titles[0][0] != m.group(1):
        fail("visible H1 must identify the matching ADR-NNNN")
    sections: dict[str, str] = {}
    hits = list(HEADINGS.finditer(prose))
    for i, hit in enumerate(hits):
        name = hit.group(1).strip()
        if name in sections:
            fail(f"duplicate H2 heading: {name}")
        sections[name] = prose[hit.end():hits[i + 1].start() if i + 1 < len(hits) else len(prose)].strip()
    for name in REQUIRED_SECTIONS:
        if name not in sections:
            fail("missing required section: ## " + name)
        elif not substantial(sections[name]):
            fail(f"section {name} needs meaningful content (>=20 characters)")
    return errors


def check_all(base: Path, base_ref: str | None = None) -> list[str]:
    directory = base / "docs" / "decisions"
    if directory.is_symlink() or (base / "docs").is_symlink():
        return ["docs/decisions must not be reached through a symbolic link"]
    if not directory.is_dir():
        return ["docs/decisions directory is required"]
    errors: list[str] = []
    paths = []
    for path in sorted(directory.iterdir()):
        if path.is_symlink() or not path.is_file():
            errors.append(f"{path.relative_to(base)}: only regular top-level ADR files are allowed")
        elif path.name not in {"README.md", "TEMPLATE.md"}:
            paths.append(path)
    if not paths:
        errors.append("no numbered Architecture Decision Records found")
    records: dict[str, dict] = {}
    for path in paths:
        errors.extend(check_record(path, base))
        match = FILENAME.fullmatch(path.name)
        if not match:
            continue
        identifier = "ADR-" + match[1]
        if identifier in records:
            errors.append(f"{path.relative_to(base)}: duplicate ADR ID {identifier}")
        try:
            records[identifier] = load_metadata(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, RecursionError):
            continue  # check_record already reports the malformed file.
    for identifier, meta in records.items():
        if meta.get("status") != "superseded":
            continue
        seen = {identifier}
        target = meta.get("superseded_by")
        while isinstance(target, str) and target in records:
            if target in seen:
                errors.append(f"{identifier}: supersession cycle involving {target}")
                break
            seen.add(target)
            successor = records[target]
            if successor.get("status") == "accepted":
                break
            if successor.get("status") != "superseded":
                errors.append(f"{identifier}: successor chain must end at an accepted ADR")
                break
            target = successor.get("superseded_by")
    if base_ref is not None:
        errors.extend(check_history(base, base_ref, {p.name for p in paths}))
    return errors


def check_history(base: Path, base_ref: str, current_names: set[str]) -> list[str]:
    """Compare filenames with a caller-selected trusted commit; never execute it."""
    if not re.fullmatch(r"[0-9a-fA-F]{40}", base_ref):
        return ["base-ref must be a full 40-character Git commit SHA"]
    try:
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "-z", base_ref + "^{commit}",
             "--", "docs/decisions/"], cwd=base, check=True, capture_output=True,
            text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [f"cannot read trusted ADR history: {exc}"]
    previous = {Path(p).name for p in result.stdout.split("\0")
                if p.startswith("docs/decisions/") and FILENAME.fullmatch(Path(p).name)}
    return [f"docs/decisions/{name}: historical ADR removed or renamed; preserve it and supersede it instead"
            for name in sorted(previous - current_names)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--base-ref", help="trusted base commit for ADR history preservation")
    args = parser.parse_args()
    errors = check_all(args.root.resolve(), args.base_ref)
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