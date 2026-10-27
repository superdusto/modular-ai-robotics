#!/usr/bin/env python3
"""Run governance tests; missing, empty, failed or skipped suites fail closed."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import unittest


def leaf_tests(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from leaf_tests(item)
        else:
            yield item


def run_tests(directory: Path) -> int:
    required = {"test_decision_gate", "test_decision_gate_workflow"}
    for module in sorted(required):
        if not (directory / (module + ".py")).is_file():
            print(f"ERROR: missing required test module {module}", file=sys.stderr)
            return 1
    loader = unittest.TestLoader()
    try:
        suite = loader.discover(str(directory), pattern="test_*.py")
    except (ImportError, OSError) as exc:
        print(f"ERROR: test discovery failed: {exc}", file=sys.stderr)
        return 1
    tests = list(leaf_tests(suite))
    modules = {test.id().split(".")[0] for test in tests}
    if not tests or required - modules or loader.errors:
        print("ERROR: required test suite is empty or failed to import", file=sys.stderr)
        return 1
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.skipped:
        print("ERROR: governance tests must not be skipped", file=sys.stderr)
    return 0 if result.wasSuccessful() and not result.skipped else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tests-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "tests")
    return run_tests(parser.parse_args().tests_dir.resolve())


if __name__ == "__main__":
    sys.exit(main())
