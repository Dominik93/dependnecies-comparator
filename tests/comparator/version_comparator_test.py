import unittest

from version_comparator import compare_versions


class VersionComparatorTestCase(unittest.TestCase):
    def test_should_return_plus_when_second_version_is_lower(self):
        actual = compare_versions("10.0.0", "9.0.0")
        self.assertEqual(actual, 1)

    def test_should_return_plus_when_second_version_is_lower_four_digits(self):
        actual = compare_versions("1.0.0.1", "1.0.0")
        self.assertEqual(actual, 1)

    def test_should_return_minus_when_second_version_is_bigger_four_digits(self):
        actual = compare_versions("1.0.0", "1.0.0.1")
        self.assertEqual(actual, -1)

    def test_should_return_zero_when_compare_same_versions(self):
        actual = compare_versions("1.0.0", "1.0.0")
        self.assertEqual(actual, 0)

    def test_should_return_plus_when_second_version_is_lower(self):
        actual = compare_versions("1.1.0", "1.0.0")
        self.assertEqual(actual, 1)

    def test_should_return_minus_when_second_version_is_bigger(self):
        actual = compare_versions("1.1.0", "1.11.0")
        self.assertEqual(actual, -1)

    def test_should_return_zero_when_compare_same_versions_with_text(self):
        actual = compare_versions("1.0.0-RELEASE", "1.0.0-RELEASE")
        self.assertEqual(actual, 0)

    def test_should_return_plus_when_second_version_is_lower_with_text(self):
        actual = compare_versions("1.0.0.RELEASE-1", "1.0.0.RELEASE-0")
        self.assertEqual(actual, 1)

    def test_should_return_minus_when_second_version_is_bigger_with_text(self):
        actual = compare_versions("1.0.0.RELEASE-0", "1.0.0.RELEASE-1")
        self.assertEqual(actual, -1)


if __name__ == '__main__':
    unittest.main()
