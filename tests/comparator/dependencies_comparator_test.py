import unittest
from dependencies_comparator import compare


class MyTestCase(unittest.TestCase):
    def test_compare_dependencies(self):
        reference_dependencies = [
            {"parent": "reference", "groupId": "com.sample.two", "artifactId": "sample-two-one", "version": "4.3.2"},
            {"parent": "reference", "groupId": "com.sample.two", "artifactId": "sample-two-two", "version": "4.3.2"},
            {"parent": "reference", "groupId": "com.sample.two", "artifactId": "sample-two-three", "version": "4.3.2"},
            {"parent": "reference", "groupId": "com.sample.one", "artifactId": "sample-one-one", "version": "2.4.0"},
            {"parent": "reference", "groupId": "com.sample.one", "artifactId": "sample-one-two", "version": "2.0.0"}]

        dependencies = [{"parent": "compared_to", "groupId": "com.sample.two", "artifactId": "sample-two-one", "version": "4.0.2"},
                        {"parent": "compared_to", "groupId": "com.sample.two", "artifactId": "sample-two-two", "version": "4.3.2"},
                        {"parent": "compared_to", "groupId": "com.sample.one", "artifactId": "sample-one-one", "version": "2.4.1"},
                        {"parent": "compared_to", "groupId": "com.sample.one", "artifactId": "sample-one-two", "version": "2.0.0"}]
        actual = compare(reference_dependencies, dependencies)
        expected = [
            {"reference": "reference:com.sample.two:sample-two-one:4.3.2",
             "operator": "ne",
             "compared_to": "compared_to:com.sample.two:sample-two-one:4.0.2"},
            {"reference": "reference:com.sample.two:sample-two-two:4.3.2",
             "operator": "eq",
             "compared_to": "compared_to:com.sample.two:sample-two-two:4.3.2"},
            {"reference": "reference:com.sample.two:sample-two-three:4.3.2",
             "operator": "not found",
             "compared_to": ""},
            {"reference": "reference:com.sample.one:sample-one-one:2.4.0",
             "operator": "ne",
             "compared_to": "compared_to:com.sample.one:sample-one-one:2.4.1"},
            {"reference": "reference:com.sample.one:sample-one-two:2.0.0",
             "operator": "eq",
             "compared_to": "compared_to:com.sample.one:sample-one-two:2.0.0"}
        ]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
