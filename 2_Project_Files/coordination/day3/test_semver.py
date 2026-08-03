import unittest

from solution import satisfies


class TestCases(unittest.TestCase):
    # --- basics ---
    def test_exact(self):
        self.assertTrue(satisfies("1.2.3", "1.2.3"))

    def test_exact_mismatch(self):
        self.assertFalse(satisfies("1.2.4", "1.2.3"))

    def test_eq_prefix(self):
        self.assertTrue(satisfies("1.2.3", "=1.2.3"))

    def test_gte(self):
        self.assertTrue(satisfies("2.0.0", ">=1.0.0"))

    def test_gte_below(self):
        self.assertFalse(satisfies("0.9.9", ">=1.0.0"))

    def test_gt_not_equal(self):
        self.assertFalse(satisfies("1.0.0", ">1.0.0"))

    # --- caret ---
    def test_caret_within(self):
        self.assertTrue(satisfies("1.4.9", "^1.2.3"))

    def test_caret_major_bump(self):
        self.assertFalse(satisfies("2.0.0", "^1.2.3"))

    def test_caret_below_floor(self):
        self.assertFalse(satisfies("1.2.0", "^1.2.3"))

    def test_caret_zero_minor(self):
        self.assertTrue(satisfies("0.2.9", "^0.2.3"))
        self.assertFalse(satisfies("0.3.0", "^0.2.3"))

    def test_caret_zero_zero(self):
        self.assertTrue(satisfies("0.0.3", "^0.0.3"))
        self.assertFalse(satisfies("0.0.4", "^0.0.3"))

    # --- tilde ---
    def test_tilde(self):
        self.assertTrue(satisfies("1.2.9", "~1.2.3"))
        self.assertFalse(satisfies("1.3.0", "~1.2.3"))

    # --- AND / OR ---
    def test_and(self):
        self.assertTrue(satisfies("1.5.0", ">=1.0.0 <2.0.0"))
        self.assertFalse(satisfies("2.5.0", ">=1.0.0 <2.0.0"))

    def test_or(self):
        self.assertTrue(satisfies("0.5.3", "^0.5.0 || >=1.0.0"))
        self.assertTrue(satisfies("2.0.0", "^0.5.0 || >=1.0.0"))
        self.assertFalse(satisfies("0.6.0", "^0.5.0 || >=1.0.0"))

    # --- prerelease precedence ---
    def test_prerelease_lt_release(self):
        self.assertTrue(satisfies("1.0.0-alpha", "<1.0.0-beta"))

    def test_prerelease_numeric_compare(self):
        self.assertTrue(satisfies("1.0.0-beta.11", ">1.0.0-beta.2"))

    def test_prerelease_numeric_vs_alpha(self):
        self.assertTrue(satisfies("1.0.0-alpha.beta", ">1.0.0-alpha.1"))

    def test_prerelease_shorter_set_lower(self):
        self.assertTrue(satisfies("1.0.0-alpha.1", ">1.0.0-alpha"))

    # --- the prerelease gate ---
    def test_gate_blocks_different_tuple(self):
        self.assertFalse(satisfies("1.0.1-alpha", ">=1.0.0"))

    def test_gate_allows_same_tuple(self):
        self.assertTrue(satisfies("1.0.0-alpha", ">=1.0.0-0"))

    def test_gate_blocks_plain_range(self):
        self.assertFalse(satisfies("2.0.0-rc.1", "^1.0.0 || >=2.0.0"))

    # --- build metadata ---
    def test_build_metadata_ignored(self):
        self.assertTrue(satisfies("1.2.3+build.5", "1.2.3"))

    def test_build_metadata_ignored_in_compare(self):
        self.assertTrue(satisfies("1.2.4+x", ">1.2.3+y"))
