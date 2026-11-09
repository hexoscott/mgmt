import copy
import unittest

from check_plan import validate


def example_plan():
    return {
        "baseline": {"existing-register": "register.py at abc123; API tests pass"},
        "requirements": ["R1", "R2", "R3"],
        "issues": [
            {
                "id": "CI",
                "wave": 1,
                "owns": ["R1"],
                "provides": ["required-checks"],
                "requires": ["existing-register"],
                "protects": ["FEATURE"],
            },
            {
                "id": "EXPORT",
                "wave": 1,
                "owns": ["R2"],
                "provides": ["export-stream"],
                "requires": ["existing-register"],
            },
            {
                "id": "FEATURE",
                "wave": 2,
                "owns": ["R3"],
                "provides": ["feature"],
                "requires": ["export-stream", "required-checks", "feature"],
            },
        ],
    }


class PlanChecks(unittest.TestCase):
    def test_baseline_own_and_earlier_wave_capabilities_are_available(self):
        self.assertEqual(validate(example_plan()), [])

    def test_issue_cannot_consume_a_capability_from_its_own_wave(self):
        plan = example_plan()
        plan["issues"][2]["wave"] = 1
        plan["issues"][2]["protects"] = []
        plan["issues"][0]["protects"] = []
        errors = validate(plan)
        self.assertTrue(any("FEATURE" in e and "export-stream" in e and "EXPORT" in e for e in errors))

    def test_issue_cannot_consume_a_capability_from_a_later_wave(self):
        plan = example_plan()
        plan["issues"][1]["wave"] = 3
        errors = validate(plan)
        self.assertTrue(any("FEATURE" in e and "export-stream" in e and "EXPORT" in e for e in errors))

    def test_required_capability_needs_a_provider(self):
        plan = example_plan()
        plan["issues"][2]["requires"].append("closed-site-history")
        self.assertTrue(any("closed-site-history" in e for e in validate(plan)))

    def test_capability_cannot_have_two_producers(self):
        plan = example_plan()
        plan["issues"][2]["provides"].append("export-stream")
        self.assertTrue(any("multiple providers" in e for e in validate(plan)))

    def test_changed_contract_cannot_silently_reuse_baseline_identity(self):
        plan = example_plan()
        plan["issues"][1]["provides"].append("existing-register")
        self.assertTrue(any("multiple providers" in e for e in validate(plan)))

    def test_requirement_cannot_be_unowned(self):
        plan = example_plan()
        plan["issues"][2]["owns"] = []
        self.assertTrue(any("R3" in e and "no owner" in e for e in validate(plan)))

    def test_requirement_cannot_have_overlapping_delivery_owners(self):
        plan = example_plan()
        plan["issues"][2]["owns"].append("R1")
        self.assertTrue(any("R1" in e and "multiple owners" in e for e in validate(plan)))

    def test_ticket_cannot_claim_an_unknown_requirement(self):
        plan = example_plan()
        plan["issues"][2]["owns"].append("R404")
        self.assertTrue(any("unknown requirement R404" in e for e in validate(plan)))

    def test_gate_must_be_in_an_earlier_wave_than_the_work_it_protects(self):
        for gate_wave in (2, 3):
            with self.subTest(gate_wave=gate_wave):
                plan = example_plan()
                plan["issues"][0]["wave"] = gate_wave
                plan["issues"][2]["requires"].remove("required-checks")
                self.assertTrue(any("CI" in e and "FEATURE" in e for e in validate(plan)))

    def test_unknown_protected_issue_is_rejected(self):
        plan = example_plan()
        plan["issues"][0]["protects"].append("MISSING")
        self.assertTrue(any("unknown protected issue MISSING" in e for e in validate(plan)))

    def test_duplicate_issue_identity_is_rejected(self):
        plan = example_plan()
        plan["issues"].append(copy.deepcopy(plan["issues"][0]))
        self.assertTrue(any("duplicate issue CI" in e for e in validate(plan)))

    def test_blocked_by_edges_are_rejected_in_favour_of_waves(self):
        plan = example_plan()
        plan["issues"][2]["blocked_by"] = ["EXPORT"]
        with self.assertRaisesRegex(ValueError, "wave"):
            validate(plan)

    def test_wave_must_be_a_positive_integer(self):
        for wave in (None, 0, -1, "1", 1.0, True):
            with self.subTest(wave=wave):
                plan = example_plan()
                plan["issues"][1]["wave"] = wave
                with self.assertRaisesRegex(ValueError, "EXPORT.wave"):
                    validate(plan)

    def test_malformed_lists_and_missing_evidence_fail_clearly(self):
        for field, value in [("requires", "export-stream"), ("owns", [None]), ("provides", [""])]:
            with self.subTest(field=field):
                plan = example_plan()
                plan["issues"][1][field] = value
                with self.assertRaises(ValueError):
                    validate(plan)
        plan = example_plan()
        plan["baseline"]["existing-register"] = ""
        with self.assertRaises(ValueError):
            validate(plan)


if __name__ == "__main__":
    unittest.main()
