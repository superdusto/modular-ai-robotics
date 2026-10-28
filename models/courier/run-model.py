#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 superdusto
"""Compile and run the standalone candidate with an already installed JDK 25."""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


MODEL_ROOT = Path(__file__).resolve().parent
DEFAULT_REPORT = MODEL_ROOT.parent.parent / "build/courier-model/model-results.json"
SCOPE = "candidate_in_memory_model_only"
BASELINE_PATH = MODEL_ROOT / "scenario-baseline.json"
REQUIRED_IDS = {f"M{i:02d}" for i in range(1, 28)}
REQUIRED_GAP_IDS = {f"KG{i:02d}" for i in range(1, 6)}


def indexed(records, count_field=None):
    if not isinstance(records, list) or not records:
        raise ValueError("Expected a nonempty list of identified checks.")
    result = {}
    for record in records:
        if (not isinstance(record, dict) or not isinstance(record.get("id"), str) or not record["id"]
                or not isinstance(record.get("name"), str) or not record["name"]):
            raise ValueError("Each check must have a nonempty ID and name.")
        if record["id"] in result:
            raise ValueError(f"Duplicate check ID: {record['id']}")
        if count_field and (type(record.get(count_field)) is not int or record[count_field] <= 0):
            raise ValueError(f"Invalid assertion count for {record['id']}")
        result[record["id"]] = record
    return result


def validate_baseline(baseline):
    if (not isinstance(baseline, dict) or baseline.get("schema_version") != 1
            or baseline.get("reviewed_source_commit") != "5f765847cde9f4ca5556dd89334c98391ff80e5e"):
        raise ValueError("Unrecognized reviewed scenario baseline.")
    scenarios = indexed(baseline.get("scenarios"), "minimum_assertions")
    if not REQUIRED_IDS.issubset(scenarios):
        raise ValueError("The baseline must retain M01-M27.")
    minimum = baseline.get("minimum_total_assertions")
    if (type(minimum) is not int or minimum < 210
            or sum(item["minimum_assertions"] for item in scenarios.values()) < 210):
        raise ValueError("The reviewed baseline must retain at least 210 assertions.")
    if not REQUIRED_GAP_IDS.issubset(indexed(baseline.get("known_gaps"))):
        raise ValueError("The known-gap baseline must retain KG01-KG05 until reviewed fixes replace them.")


def validate_model_result(result, baseline):
    if not isinstance(result, dict) or result.get("scope") != SCOPE:
        raise ValueError("Unexpected model result scope.")
    observed = indexed(result.get("scenario_results"), "assertions")
    expected = indexed(baseline["scenarios"], "minimum_assertions")
    missing = set(expected) - set(observed)
    if missing:
        raise ValueError("Missing reviewed scenarios: " + ", ".join(sorted(missing)))
    for identifier, requirement in expected.items():
        actual = observed[identifier]
        if actual["name"] != requirement["name"] or actual["assertions"] < requirement["minimum_assertions"]:
            raise ValueError(f"Reviewed scenario changed or lost assertions: {identifier}")
    if (type(result.get("scenarios_passed")) is not int or result["scenarios_passed"] != len(observed)
            or result.get("scenarios") != [item["name"] for item in result["scenario_results"]]
            or type(result.get("assertions")) is not int
            or result["assertions"] != sum(item["assertions"] for item in observed.values())
            or result["assertions"] < baseline["minimum_total_assertions"]):
        raise ValueError("Model totals do not match the retained scenario coverage.")
    if not isinstance(result.get("java_version"), str) or not re.match(r"^25(?:[.+\-]|$)", result["java_version"]):
        raise ValueError("Model result must identify Java 25.")
    return {"status": "verified", "required_ids": sorted(expected),
            "minimum_assertions": baseline["minimum_total_assertions"]}


def validate_known_gaps(result, baseline):
    if (not isinstance(result, dict) or result.get("scope") != "candidate_known_gap_observations"
            or result.get("status") != "observed_unfixed"):
        raise ValueError("Known-gap observations must be explicitly marked observed_unfixed.")
    observed = indexed(result.get("observations"), "assertions")
    for identifier, requirement in indexed(baseline["known_gaps"]).items():
        if identifier not in observed or observed[identifier]["name"] != requirement["name"]:
            raise ValueError(f"Missing or changed known-gap observation: {identifier}")
    if (type(result.get("assertions")) is not int
            or result["assertions"] != sum(item["assertions"] for item in observed.values())):
        raise ValueError("Known-gap observation counts are inconsistent.")


def jdk_tools():
    """Honor an explicit home; otherwise use javac and its sibling JVM."""
    executable_suffix = ".exe" if os.name == "nt" else ""
    for variable in ("MAR_JAVA_HOME", "JAVA_HOME"):
        if os.environ.get(variable):
            directory = Path(os.environ[variable]).expanduser().resolve() / "bin"
            return directory / ("javac" + executable_suffix), directory / ("java" + executable_suffix), variable
    compiler = shutil.which("javac")
    if not compiler:
        raise ValueError("JDK 25 not found. Set MAR_JAVA_HOME or JAVA_HOME, or put javac on PATH.")
    compiler = Path(compiler).resolve()
    return compiler, compiler.with_name("java" + executable_suffix), "PATH"


def execute(*command):
    return subprocess.run(command, check=True, capture_output=True, text=True, timeout=120)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT,
                        help="JSON result path; defaults to ignored build/courier-model/model-results.json")
    args = parser.parse_args()
    report = {
        "report_schema_version": 2,
        "model_id": "mar-courier-kernel-candidate@0.2.0",
        "scope": SCOPE,
        "executed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "runtime_or_gameplay_fixtures_executed": False,
        "required_java_major": 25,
        "evidence_limit": "Standalone in-memory model, not Minecraft or NeoForge. Trusted fixture "
            "evidence and snapshot copying do not assess real authentication, physical inventories, "
            "provider hooks, disk saves, crash consistency or energy. Complete RCN cases remain not_run.",
    }
    try:
        report["source_sha256"] = {
            name: hashlib.sha256((MODEL_ROOT / name).read_bytes()).hexdigest()
            for name in ("CourierKernel.java", "CourierKernelChecks.java", "CourierKernelKnownGapChecks.java",
                         "scenario-baseline.json", "run-model.py")
        }
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        validate_baseline(baseline)
        compiler, java, selection = jdk_tools()
        report["jdk_selection"] = selection
        version = execute(str(compiler), "-version")
        report["compiler"] = (version.stdout + version.stderr).strip()
        version = execute(str(java), "-version")
        report["runtime"] = (version.stdout + version.stderr).strip()
        if not re.search(r"^javac\s+25(?:[.\s+\-]|$)", report["compiler"]) or not re.search(
                r'\bversion "25(?:[.\-+]|\")', report["runtime"]):
            raise ValueError("JDK 25 is required for both javac and java; no version fallback is allowed.")
        with tempfile.TemporaryDirectory(prefix="mar-courier-kernel-") as classes:
            execute(str(compiler), "--release", "25", "-d", classes,
                    str(MODEL_ROOT / "CourierKernel.java"), str(MODEL_ROOT / "CourierKernelChecks.java"),
                    str(MODEL_ROOT / "CourierKernelKnownGapChecks.java"))
            run = execute(str(java), "-cp", classes, "CourierKernelChecks")
            result = json.loads(run.stdout)
            report["baseline_coverage"] = validate_model_result(result, baseline)
            gaps = json.loads(execute(str(java), "-cp", classes, "CourierKernelKnownGapChecks").stdout)
            validate_known_gaps(gaps, baseline)
        report.update({key: result[key] for key in ("scenarios_passed", "assertions", "java_version", "scenarios",
                                                   "scenario_results")})
        report["known_gap_observations"] = gaps
        report["execution_status"] = "passed"
    except (subprocess.SubprocessError, OSError, ValueError, KeyError, TypeError) as error:
        report["execution_status"] = "failed"
        report["error"] = str(error)
        if isinstance(error, (subprocess.CalledProcessError, subprocess.TimeoutExpired)):
            diagnostic = []
            for value in (error.stdout, error.stderr):
                if value:
                    diagnostic.append(value.decode(errors="replace") if isinstance(value, bytes) else value)
            report["diagnostic"] = "".join(diagnostic)
    try:
        report_path = args.report.expanduser().resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except OSError as error:
        print(f"Could not save model report: {error}", file=sys.stderr)
        return 1
    if report["execution_status"] == "passed":
        print(f"{report['scenarios_passed']} model scenarios passed; {report['assertions']} assertions; "
              f"Java {report['java_version']}.")
        print(f"{len(report['known_gap_observations']['observations'])} known-gap observations confirmed; defects remain unfixed.")
    else:
        print(report.get("diagnostic") or report["error"], file=sys.stderr)
    print(report_path)
    return 0 if report["execution_status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
