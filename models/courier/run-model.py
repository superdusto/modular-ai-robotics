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
            for name in ("CourierKernel.java", "CourierKernelChecks.java", "run-model.py")
        }
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
                    str(MODEL_ROOT / "CourierKernel.java"), str(MODEL_ROOT / "CourierKernelChecks.java"))
            run = execute(str(java), "-cp", classes, "CourierKernelChecks")
        result = json.loads(run.stdout)
        if (result.get("scope") != SCOPE or not isinstance(result.get("scenarios"), list)
                or not result["scenarios"] or result.get("scenarios_passed") != len(result["scenarios"])
                or not isinstance(result.get("assertions"), int) or result["assertions"] <= 0):
            raise ValueError("The check harness did not report a complete, nonempty model result.")
        report.update({key: result[key] for key in ("scenarios_passed", "assertions", "java_version", "scenarios")})
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
    else:
        print(report.get("diagnostic") or report["error"], file=sys.stderr)
    print(report_path)
    return 0 if report["execution_status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
