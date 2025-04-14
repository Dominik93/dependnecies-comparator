import unittest
from properties_loader import load, loads


class MyTestCase(unittest.TestCase):

    def test_read_properties_from_file_empty_property(self):
        actual = load("empty.xml")
        expected = {"empty.version": ""}
        self.assertEqual(actual, expected)

    def test_read_properties_from_file_duplicate_properties(self):
        actual = load("duplicate.xml")
        expected = {"duplicate.version": "1.0.0"}
        self.assertEqual(actual, expected)

    def test_read_properties_from_file(self):
        actual = load("pom.xml")
        expected = {"sample.one.version": "2.4.0", "sample.two.version": "4.3.2"}
        self.assertEqual(actual, expected)

    def test_read_properties_from_files(self):
        actual = loads(["pom_one.xml", "pom_two.xml"])
        expected = {"sample.one.version": "2.4.0", "sample.two.version": "4.3.2"}
        self.assertEqual(actual, expected)

    def test_read_inherited_properties(self):
        actual = loads(["pom_child.xml", "pom_parent.xml"])
        expected = {"sample.one.version": "2.4.0"}
        self.assertEqual(actual, expected)

    def test_read_nested_properties(self):
        actual = loads(["pom_nested.xml"])
        expected = {"sample.one.version": "2.4.0", "sample.two.version": "2.4.0", "sample.version": "2.4.0"}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
