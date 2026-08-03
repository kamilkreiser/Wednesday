import unittest

from solution import parse_duration


class TestCases(unittest.TestCase):
    def test_hours(self):
        self.assertEqual(parse_duration("2h"), 7200)

    def test_minutes_over_sixty(self):
        self.assertEqual(parse_duration("90m"), 5400)

    def test_combo(self):
        self.assertEqual(parse_duration("1h30m"), 5400)

    def test_full_combo(self):
        self.assertEqual(parse_duration("1d2h3m4s"), 93784)

    def test_zero(self):
        self.assertEqual(parse_duration("0s"), 0)

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("")

    def test_unknown_unit_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("5x")

    def test_duplicate_unit_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("1h2h")

    def test_wrong_order_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("30m1h")

    def test_bare_number_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("42")

    def test_whitespace_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("1h 30m")

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("-5m")
