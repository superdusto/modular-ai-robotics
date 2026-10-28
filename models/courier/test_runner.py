#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 superdusto
"""Coverage-guard regressions; no JDK or Minecraft installation required."""

import copy
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("courier_model_runner", ROOT / "run-model.py")
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)
BASELINE = json.loads((ROOT / "scenario-baseline.json").read_text(encoding="utf-8"))


def valid_result():
    records = [{"id": entry["id"], "name": entry["name"], "assertions": entry["minimum_assertions"]}
               for entry in BASELINE["scenarios"]]
    return {"scope": RUNNER.SCOPE, "java_version": "25.0.2", "scenario_results": records,
            "scenarios": [entry["name"] for entry in records], "scenarios_passed": len(records),
            "assertions": sum(entry["assertions"] for entry in records)}


def refresh_totals(result):
    records = result["scenario_results"]
    result.update(scenarios=[entry["name"] for entry in records], scenarios_passed=len(records),
                  assertions=sum(entry["assertions"] for entry in records))


def valid_gaps():
    return {"scope": "candidate_known_gap_observations", "status": "observed_unfixed",
            "observations": [{**entry, "assertions": 1} for entry in BASELINE["known_gaps"]],
            "assertions": len(BASELINE["known_gaps"])}


class CoverageGuardTests(unittest.TestCase):
    def test_reviewed_baseline_and_complete_result(self):
        RUNNER.validate_baseline(BASELINE)
        proof = RUNNER.validate_model_result(valid_result(), BASELINE)
        self.assertEqual(set(proof["required_ids"]), RUNNER.REQUIRED_IDS)

    def test_one_remaining_scenario_cannot_self_certify(self):
        result = valid_result()
        result["scenario_results"] = result["scenario_results"][:1]
        refresh_totals(result)
        with self.assertRaisesRegex(ValueError, "Missing reviewed scenarios"):
            RUNNER.validate_model_result(result, BASELINE)

    def test_single_removed_scenario_is_detected(self):
        result = valid_result()
        result["scenario_results"].pop()
        refresh_totals(result)
        with self.assertRaisesRegex(ValueError, "M27"):
            RUNNER.validate_model_result(result, BASELINE)

    def test_duplicate_id_cannot_replace_missing_scenario(self):
        result = valid_result()
        result["scenario_results"][-1] = copy.deepcopy(result["scenario_results"][0])
        refresh_totals(result)
        with self.assertRaisesRegex(ValueError, "Duplicate check ID"):
            RUNNER.validate_model_result(result, BASELINE)

    def test_changed_name_cannot_reuse_reviewed_id(self):
        result = valid_result()
        result["scenario_results"][0]["name"] = "unrelated check"
        refresh_totals(result)
        with self.assertRaisesRegex(ValueError, "M01"):
            RUNNER.validate_model_result(result, BASELINE)

    def test_per_scenario_floor_survives_compensating_assertions(self):
        result = valid_result()
        result["scenario_results"][0]["assertions"] -= 1
        result["scenario_results"][1]["assertions"] += 1
        refresh_totals(result)
        self.assertEqual(result["assertions"], 210)
        with self.assertRaisesRegex(ValueError, "M01"):
            RUNNER.validate_model_result(result, BASELINE)

    def test_self_reported_total_must_match_details(self):
        result = valid_result()
        result["assertions"] += 1
        with self.assertRaisesRegex(ValueError, "totals"):
            RUNNER.validate_model_result(result, BASELINE)

    def test_self_reported_pass_count_must_match_details(self):
        result = valid_result()
        result["scenarios_passed"] = 1
        with self.assertRaisesRegex(ValueError, "totals"):
            RUNNER.validate_model_result(result, BASELINE)

    def test_names_without_identified_results_are_insufficient(self):
        result = valid_result()
        del result["scenario_results"]
        with self.assertRaises(ValueError):
            RUNNER.validate_model_result(result, BASELINE)

    def test_boolean_is_not_an_assertion_count(self):
        result = valid_result()
        result["scenario_results"][0]["assertions"] = True
        with self.assertRaisesRegex(ValueError, "assertion count"):
            RUNNER.validate_model_result(result, BASELINE)

    def test_new_scenarios_can_extend_the_retained_baseline(self):
        result = valid_result()
        result["scenario_results"].append({"id": "M28", "name": "additional check", "assertions": 2})
        refresh_totals(result)
        RUNNER.validate_model_result(result, BASELINE)

    def test_reduced_manifest_cannot_drop_required_id(self):
        baseline = copy.deepcopy(BASELINE)
        baseline["scenarios"].pop()
        with self.assertRaisesRegex(ValueError, "retain M01-M27"):
            RUNNER.validate_baseline(baseline)

    def test_manifest_cannot_lower_total_floor(self):
        baseline = copy.deepcopy(BASELINE)
        baseline["minimum_total_assertions"] = 1
        with self.assertRaisesRegex(ValueError, "210 assertions"):
            RUNNER.validate_baseline(baseline)

    def test_manifest_cannot_silently_drop_known_gap(self):
        baseline = copy.deepcopy(BASELINE)
        baseline["known_gaps"].pop()
        with self.assertRaisesRegex(ValueError, "KG01-KG06"):
            RUNNER.validate_baseline(baseline)

    def test_known_gap_observations_are_separate(self):
        RUNNER.validate_known_gaps(valid_gaps(), BASELINE)

    def test_missing_known_gap_is_detected(self):
        result = valid_gaps()
        result["observations"].pop()
        result["assertions"] -= 1
        with self.assertRaisesRegex(ValueError, "KG06"):
            RUNNER.validate_known_gaps(result, BASELINE)

    def test_known_gaps_cannot_claim_fixed_status(self):
        result = valid_gaps()
        result["status"] = "fixed"
        with self.assertRaisesRegex(ValueError, "observed_unfixed"):
            RUNNER.validate_known_gaps(result, BASELINE)

    def test_duplicate_known_gap_is_detected(self):
        result = valid_gaps()
        result["observations"][-1] = copy.deepcopy(result["observations"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate check ID"):
            RUNNER.validate_known_gaps(result, BASELINE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
