from copy import deepcopy
from pathlib import Path
import unittest

from health_lab.core import evaluate_health
from health_lab.fixture_check import check


class HealthTests(unittest.TestCase):
    def test_readiness_uses_consecutive_failure_hysteresis(self):
        result = evaluate_health({"probes": [True, False, False, False], "failure_threshold": 3})
        self.assertEqual(result, {"states": ["ready", "ready", "ready", "unready"], "ready": False, "success_streak": 0, "failure_streak": 3})

    def test_success_threshold_resets_after_failure(self):
        result = evaluate_health({"probes": [True, False, True, True], "success_threshold": 2, "failure_threshold": 1})
        self.assertEqual(result["states"], ["unready", "unready", "unready", "ready"])
        self.assertEqual(result["success_streak"], 2)

    def test_empty_input_preserves_initial_readiness(self):
        self.assertEqual(evaluate_health({"probes": [], "initial_ready": True}), {"states": [], "ready": True, "success_streak": 0, "failure_streak": 0})
        self.assertFalse(evaluate_health({"probes": []})["ready"])

    def test_invalid_policies_and_nonboolean_probes_are_rejected(self):
        cases = [{"probes": [1]}, {"probes": [], "failure_threshold": True}, {"probes": [], "success_threshold": 11},
                 {"probes": [], "initial_ready": 0}, {"probes": [], "extra": True}, {"probes": [True] * 1001}]
        for data in cases:
            with self.subTest(data=data), self.assertRaises(ValueError):
                evaluate_health(data)

    def test_input_is_not_modified(self):
        data = {"probes": [True, False, True], "success_threshold": 2}
        original = deepcopy(data)
        evaluate_health(data)
        self.assertEqual(data, original)

    def test_complete_fixture_corpus(self):
        self.assertGreaterEqual(check(Path(__file__).resolve().parents[1] / "fixtures/cases.jsonl", evaluate_health), 350)


if __name__ == "__main__":
    unittest.main()
