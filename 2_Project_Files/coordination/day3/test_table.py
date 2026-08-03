import unittest

from solution import render_table


class TestCases(unittest.TestCase):
    def test_basic_ints(self):
        self.assertEqual(render_table(['name', 'qty'], [['apple', 3], ['kiwi', 12]]), 'name  | qty\n-----------\napple |   3\nkiwi  |  12')

    def test_floats_two_dp(self):
        self.assertEqual(render_table(['item', 'price'], [['tea', 1.5], ['coffee', 12.25]]), 'item   | price\n--------------\ntea    |  1.50\ncoffee | 12.25')

    def test_bool_yes_no(self):
        self.assertEqual(render_table(['k', 'v'], [['ok', True], ['bad', False]]), 'k   | v\n---------\nok  | yes\nbad | no')

    def test_none_em_dash(self):
        self.assertEqual(render_table(['a', 'b'], [['x', None], [None, 7]]), 'a | b\n-----\nx | —\n— | 7')

    def test_empty_rows(self):
        self.assertEqual(render_table(['only', 'header'], []), 'only | header\n-------------')

    def test_single_col_rstrip(self):
        self.assertEqual(render_table(['n'], [[5], [100]]), 'n\n---\n  5\n100')

    def test_mixed_int_float_col(self):
        self.assertEqual(render_table(['v'], [[3], [4.5]]), 'v\n----\n   3\n4.50')

    def test_wide_header(self):
        self.assertEqual(render_table(['identifier', 'x'], [['a', 1]]), 'identifier | x\n--------------\na          | 1')

    def test_strings_left(self):
        self.assertEqual(render_table(['s'], [['hi'], ['longer str']]), 's\n----------\nhi\nlonger str')

    def test_bool_before_int_trap(self):
        self.assertEqual(render_table(['flag', 'count'], [[True, 1], [False, 0]]), 'flag | count\n------------\nyes  |     1\nno   |     0')
