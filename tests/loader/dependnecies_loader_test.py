import unittest
from dependencies_loader import load, loads


class MyTestCase(unittest.TestCase):
    def test_read_dependencies_from_file(self):
        actual = load("pom.xml")
        expected = [{"parent": "sample", "groupId": "com.sample.one", "artifactId": "sample-one-one", "version": "2.4.0"},
                    {"parent": "sample", "groupId": "com.sample.one", "artifactId": "sample-one-two", "version": "2.0.0"},
                    {"parent": "sample", "groupId": "com.sample.two", "artifactId": "sample-two-one", "version": "4.3.2"},
                    {"parent": "sample", "groupId": "com.sample.two", "artifactId": "sample-two-two", "version": "4.3.2"},
                    {"parent": "sample", "groupId": "com.sample.two", "artifactId": "sample-two-three", "version": "4.3.2"} ]
        self.assertEqual(actual, expected)

    def test_read_dependencies_from_files(self):
        actual = loads(["pom_one.xml", "pom_two.xml"])
        expected = [{"parent": "sample", "groupId": "com.sample.one", "artifactId": "sample-one-one", "version": "2.4.0"},
                    {"parent": "sample", "groupId": "com.sample.one", "artifactId": "sample-one-two", "version": "2.0.0"},
                    {"parent": "sample", "groupId": "com.sample.two", "artifactId": "sample-two-one", "version": "4.3.2"},
                    {"parent": "sample", "groupId": "com.sample.two", "artifactId": "sample-two-two", "version": "4.3.2"},
                    {"parent": "sample", "groupId": "com.sample.two", "artifactId": "sample-two-three", "version": "4.3.2"}]
        self.assertEqual(actual, expected)

    def test_read_dependencies_inherited(self):
        actual = loads(["pom_child.xml", "pom_parent.xml"])
        expected = [{"parent": "sample", "groupId": "com.sample.one", "artifactId": "sample-one-one", "version": "2.4.0"},
                    {"parent": "sample", "groupId": "com.sample.one", "artifactId": "sample-one-two", "version": "2.0.0"}]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
