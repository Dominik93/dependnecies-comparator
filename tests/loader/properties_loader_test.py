import unittest

from models import FilePathInfo
from properties_loader import load_properties, loads_properties


def _create(path: str):
    return FilePathInfo(None, None, path)


class PropertiesLoaderTestCase(unittest.TestCase):

    def test_read_properties_from_file_empty_property(self):
        actual = load_properties(_create("./resources/empty.xml"))
        expected = {"empty.version": "", "project.version": ""}
        self.assertEqual(actual, expected)

    def test_read_properties_from_file_duplicate_properties(self):
        actual = load_properties(_create("./resources/duplicate.xml"))
        expected = {"duplicate.version": "1.0.0", "project.version": ""}
        self.assertEqual(actual, expected)

    def test_read_properties_from_file(self):
        actual = load_properties(_create("./resources/pom.xml"))
        expected = {"sample.one.version": "2.4.0", "sample.two.version": "4.3.2", "project.version": ""}
        self.assertEqual(actual, expected)

    def test_read_properties_from_files(self):
        actual = loads_properties([_create("./resources/pom_one.xml"), _create("./resources/pom_two.xml")])
        expected = {"sample.one.version": "2.4.0", "sample.two.version": "4.3.2", "project.version": ""}
        self.assertEqual(actual, expected)

    def test_read_inherited_properties(self):
        actual = loads_properties([_create("./resources/pom_child.xml"), _create("./resources/pom_parent.xml")])
        expected = {"sample.one.version": "2.4.0", "project.version": ""}
        self.assertEqual(actual, expected)

    def test_read_nested_properties(self):
        actual = loads_properties([_create("resources/pom_nested.xml")])
        expected = {"sample.one.version": "2.4.0", "sample.two.version": "2.4.0", "sample.version": "2.4.0",
                    "project.version": ""}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
