import unittest

from dependencies_comparator import compare
from models import Dependency


class MyTestCase(unittest.TestCase):
    def test_compare_dependencies(self):
        reference_dependencies = [
            Dependency("reference", "com.sample.two", "sample-two-one", "4.3.2", ""),
            Dependency("reference", "com.sample.two", "sample-two-two", "4.3.2", ""),
            Dependency("reference", "com.sample.two", "sample-two-three", "4.3.2", ""),

            Dependency("reference", "com.sample.one", "sample-one-one", "2.4.0", ""),
            Dependency("reference", "com.sample.one", "sample-one-two", "2.0.0", "")]

        dependencies = [
            Dependency("compared_to", "com.sample.two", "sample-two-one", "4.0.2", ""),
            Dependency("compared_to", "com.sample.two", "sample-two-two", "4.3.2", ""),
            Dependency("compared_to", "com.sample.one", "sample-one-one", "2.4.1", ""),
            Dependency("compared_to", "com.sample.one", "sample-one-two", "2.0.0", "")]
        actual = compare(reference_dependencies, dependencies)
        expected = [
            {"reference": "reference:com.sample.two:sample-two-one:4.3.2",
             "operator": "ge",
             "compared_to": "compared_to:com.sample.two:sample-two-one:4.0.2"},
            {"reference": "reference:com.sample.two:sample-two-two:4.3.2",
             "operator": "eq",
             "compared_to": "compared_to:com.sample.two:sample-two-two:4.3.2"},
            {"reference": "reference:com.sample.two:sample-two-three:4.3.2",
             "operator": "not found",
             "compared_to": ""},
            {"reference": "reference:com.sample.one:sample-one-one:2.4.0",
             "operator": "lt",
             "compared_to": "compared_to:com.sample.one:sample-one-one:2.4.1"},
            {"reference": "reference:com.sample.one:sample-one-two:2.0.0",
             "operator": "eq",
             "compared_to": "compared_to:com.sample.one:sample-one-two:2.0.0"}
        ]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
