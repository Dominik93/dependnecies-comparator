import unittest
from dependencies_loader import load, loads


class MyTestCase(unittest.TestCase):
    def test_read_dependencies_from_file(self):
        actual = load("pom.xml")
        expected = [{"groupId": "com.sample.one", "artifactId": "sample-one-one", "version": "2.4.0"},
                    {"groupId": "com.sample.one", "artifactId": "sample-one-two", "version": "2.0.0"},
                    {"groupId": "com.sample.two", "artifactId": "sample-two-one", "version": "4.3.2"},
                    {"groupId": "com.sample.two", "artifactId": "sample-two-two", "version": "4.3.2"},
                    {"groupId": "com.sample.two", "artifactId": "sample-two-three", "version": "4.3.2"} ]
        self.assertEqual(actual, expected)

    def test_read_dependencies_from_files(self):
        actual = loads(["pom_one.xml", "pom_two.xml"])
        expected = [{"groupId": "com.sample.one", "artifactId": "sample-one-one", "version": "2.4.0"},
                    {"groupId": "com.sample.one", "artifactId": "sample-one-two", "version": "2.0.0"},
                    {"groupId": "com.sample.two", "artifactId": "sample-two-one", "version": "4.3.2"},
                    {"groupId": "com.sample.two", "artifactId": "sample-two-two", "version": "4.3.2"},
                    {"groupId": "com.sample.two", "artifactId": "sample-two-three", "version": "4.3.2"}]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
