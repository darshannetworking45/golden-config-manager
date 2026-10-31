import unittest
from src.manager import GoldenConfigManager

CONFIG_A = """
hostname sw-acc-01
service password-encryption
service timestamps log datetime msec
no ip domain-lookup
spanning-tree mode rapid-pvst
"""

CONFIG_B = """
hostname sw-acc-02
service password-encryption
"""

class TestGoldenConfig(unittest.TestCase):
    def test_full_adherence(self):
        mgr = GoldenConfigManager()
        res = mgr.calculate_standardization_score("sw-acc-01", "access_switch", CONFIG_A)
        self.assertEqual(res["score_pct"], 100.0)
        self.assertEqual(len(res["missing_golden_lines"]), 0)

    def test_partial_adherence_with_exception(self):
        mgr = GoldenConfigManager()
        mgr.register_exception("sw-acc-02", "spanning-tree mode rapid-pvst")
        res = mgr.calculate_standardization_score("sw-acc-02", "access_switch", CONFIG_B)
        self.assertEqual(res["score_pct"], 50.0)

if __name__ == "__main__":
    unittest.main()
