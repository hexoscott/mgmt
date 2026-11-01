import copy
import unittest

from check_plan import validate


def example_plan():
    return {
        "baseline": {"existing-register": "register.py at abc123; API tests pass"},
        "requirements": ["R1", "R2"],
        "issues": [
            {
                "id": "CI",
                "owns": ["R1"],
                "provides": ["required-checks"],
                "requires": ["existing-register"],
                "protects": ["API", "FEATURE"],
            },
            {
                "id": "API",
                "blocked_by": ["CI"],
                "provides": ["export-stream"],
            },
            {
                "id": "FEATURE",
                "blocked_by": ["API"],
                "owns": ["R2"],
                "provides": ["feature"],
                "requires": ["export-stream", "required-checks", "feature"],
            },
        ],
    }


class PlanChecks(unittest.TestCase):
    def test_baseline_own_and_transitive_capabilities_are_available(self):
        self.assertEqual(validate(example_plan()), [])

    def test_acyclic_graph_can_still_lack_a_required_producer(self):
        plan = example_plan()
        plan["issues"][2]["blocked_by"] = ["CI"]
        errors = validate(plan)
        self.assertTrue(any("export-stream" in e and "API" in e for e in errors))

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
        self.assertTrue(any("R2" in e and "no owner" in e for e in validate(plan)))

    def test_requirement_cannot_have_overlapping_delivery_owners(self):
        plan = example_plan()
        plan["issues"][2]["owns"].append("R1")
        self.assertTrue(any("R1" in e and "multiple owners" in e for e in validate(plan)))

    def test_ticket_cannot_claim_an_unknown_requirement(self):
        plan = example_plan()
        plan["issues"][2]["owns"].append("R404")
        self.assertTrue(any("unknown requirement R404" in e for e in validate(plan)))

    def test_gate_cannot_follow_work_it_protects(self):
        plan = {
            "baseline": {},
            "requirements": ["R1"],
            "issues": [
                {"id": "FEATURE", "owns": ["R1"]},
                {"id": "CI", "blocked_by": ["FEATURE"], "protects": ["FEATURE"]},
            ],
        }
        self.assertTrue(any("must precede FEATURE" in e for e in validate(plan)))

    def test_dependency_cycle_is_rejected(self):
        plan = example_plan()
        plan["issues"][0]["blocked_by"] = ["FEATURE"]
        self.assertTrue(any("cycle" in e for e in validate(plan)))

    def test_unknown_blocker_is_rejected(self):
        plan = example_plan()
        plan["issues"][2]["blocked_by"] = ["MISSING"]
        self.assertTrue(any("unknown blocker MISSING" in e for e in validate(plan)))

    def test_unknown_protected_issue_is_rejected(self):
        plan = example_plan()
        plan["issues"][0]["protects"].append("MISSING")
        self.assertTrue(any("unknown protected issue MISSING" in e for e in validate(plan)))

    def test_duplicate_issue_identity_is_rejected(self):
        plan = example_plan()
        plan["issues"].append(copy.deepcopy(plan["issues"][0]))
        self.assertTrue(any("duplicate issue CI" in e for e in validate(plan)))

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
