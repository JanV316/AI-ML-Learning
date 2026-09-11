"""
Unit tests for passforge.analyzer module using Python unittest framework.
"""

import unittest
from passforge.analyzer import (
    analyze_password,
    estimate_entropy,
    get_entropy_level,
    has_repeated_characters,
    has_repeated_pattern,
    has_sequential_characters,
    is_common_password,
)


class TestAnalyzer(unittest.TestCase):

    def test_common_password_detection(self):
        self.assertTrue(is_common_password("password123"))
        self.assertTrue(is_common_password("PASSWORD123"))

    def test_non_common_password_detection(self):
        self.assertFalse(is_common_password("XyZ_987#UniqueKey"))

    def test_repeated_character_detection(self):
        self.assertTrue(has_repeated_characters("aaa"))
        self.assertFalse(has_repeated_characters("aba"))
        self.assertFalse(has_repeated_characters("aa"))

    def test_sequential_pattern_detection(self):
        self.assertTrue(has_sequential_characters("abc"))
        self.assertTrue(has_sequential_characters("123"))

    def test_reverse_sequence_detection(self):
        self.assertTrue(has_sequential_characters("cba"))
        self.assertTrue(has_sequential_characters("321"))

    def test_repeated_pattern_detection(self):
        self.assertTrue(has_repeated_pattern("abcabc"))
        self.assertTrue(has_repeated_pattern("123123"))
        self.assertFalse(has_repeated_pattern("abcdef"))

    def test_entropy_calculation(self):
        entropy = estimate_entropy("Abc1!")
        self.assertGreater(entropy, 0.0)

    def test_entropy_classification(self):
        self.assertEqual(get_entropy_level(30), "Very Low")
        self.assertEqual(get_entropy_level(50), "Low")
        self.assertEqual(get_entropy_level(70), "Moderate")
        self.assertEqual(get_entropy_level(90), "High")
        self.assertEqual(get_entropy_level(110), "Very High")

    def test_analysis_result_structure(self):
        res = analyze_password("K#9xP$m2L!vQ8zW9")
        expected_keys = {
            "length",
            "uppercase",
            "lowercase",
            "digit",
            "special",
            "common",
            "repeated",
            "sequential",
            "repeated_pattern",
            "entropy",
            "strength",
            "score",
            "warnings",
            "suggestions",
        }
        self.assertTrue(expected_keys.issubset(res.keys()))

    def test_empty_password_handling(self):
        with self.assertRaises(ValueError):
            analyze_password("")

        with self.assertRaises(ValueError):
            is_common_password("")

        with self.assertRaises(ValueError):
            has_repeated_characters("")

        with self.assertRaises(ValueError):
            has_sequential_characters("")

        with self.assertRaises(ValueError):
            has_repeated_pattern("")

        with self.assertRaises(ValueError):
            estimate_entropy("")


if __name__ == "__main__":
    unittest.main()
