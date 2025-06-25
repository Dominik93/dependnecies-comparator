import unittest

from dependencies_comparator import compare
from models import Dependency
from printer import Row


class DependenciesComparatorTestCase(unittest.TestCase):
    def test_compare_dependencies(self):
        reference_dependencies = [
            Dependency("reference", "{sample}", "com.sample.two", "sample-two-one", "4.3.2", ""),
            Dependency("reference", "{sample}", "com.sample.two", "sample-two-two", "4.3.2", ""),
            Dependency("reference", "{sample}", "com.sample.two", "sample-two-three", "4.3.2", ""),

            Dependency("reference", "2.4.0", "com.sample.one", "sample-one-one", "2.4.0", ""),
            Dependency("reference", "2.0.0", "com.sample.one", "sample-one-two", "2.0.0", "")]

        dependencies = [
            Dependency("compared_to", "4.0.2", "com.sample.two", "sample-two-one", "4.0.2", ""),
            Dependency("compared_to", "4.3.2", "com.sample.two", "sample-two-two", "4.3.2", ""),
            Dependency("compared_to", "2.4.1", "com.sample.one", "sample-one-one", "2.4.1", ""),
            Dependency("compared_to", "2.0.0", "com.sample.one", "sample-one-two", "2.0.0", "")]

        actual = compare(reference_dependencies, dependencies)

        expected = [
            Row("reference:com.sample.two:sample-two-one:4.3.2", "{sample}", "gt",
                "compared_to:com.sample.two:sample-two-one:4.0.2"),
            Row("reference:com.sample.two:sample-two-two:4.3.2", "{sample}", "eq",
                "compared_to:com.sample.two:sample-two-two:4.3.2"),
            Row("reference:com.sample.two:sample-two-three:4.3.2", "{sample}", "not found", None),
            Row("reference:com.sample.one:sample-one-one:2.4.0", "2.4.0", "lt",
                "compared_to:com.sample.one:sample-one-one:2.4.1"),
            Row("reference:com.sample.one:sample-one-two:2.0.0", "2.0.0", "eq",
                "compared_to:com.sample.one:sample-one-two:2.0.0")
        ]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
