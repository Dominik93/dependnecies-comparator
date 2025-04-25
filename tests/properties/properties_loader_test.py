import unittest

from models import File
from properties_loader import load_properties, loads_properties


class LocalFile(File):
    def __init__(self, local_path):
        self._local_path = local_path

    def spawn(self, path):
        return LocalFile(path)

    def local_path(self):
        return self._local_path


def _create(path: str):
    return LocalFile(path)


class PropertiesLoaderTestCase(unittest.TestCase):

    def test_read_properties_from_file_empty_property(self):
        actual = load_properties(_create("com/sample/empty/1.0.0/empty-1.0.0.pom"))
        expected = {"empty.version": "", "project.version": "1.0.0"}
        self.assertEqual(actual, expected)

    def test_read_properties_from_file_duplicate_properties(self):
        actual = load_properties(_create("com/sample/duplicate/1.0.0/duplicate-1.0.0.pom"))
        expected = {"duplicate.version": "1.0.0", "project.version": "1.0.0"}
        self.assertEqual(actual, expected)

    def test_read_properties_from_file(self):
        actual = load_properties(_create("com/sample/pom/1.0.0/pom-1.0.0.pom"))
        expected = {"sample.one.version": "2.4.0", "sample.two.version": "4.3.2", "project.version": "1.0.0"}
        self.assertEqual(actual, expected)

    def test_read_properties_from_files(self):
        actual = loads_properties([_create("com/sample/one/1.0.0/one-1.0.0.pom"),
                                   _create("com/sample/two/1.0.0/two-1.0.0.pom")])
        expected = {"sample.one.version": "2.4.0", "sample.two.version": "4.3.2", "project.version": "1.0.0"}
        self.assertEqual(actual, expected)

    def test_read_inherited_properties(self):
        actual = loads_properties([_create("com/sample/child/1.0.0/child-1.0.0.pom"),
                                   _create("com/sample/parent/1.0.0/parent-1.0.0.pom")])
        expected = {"sample.one.version": "2.4.0", "project.version": "1.0.0"}
        self.assertEqual(actual, expected)

    def test_read_parent_properties(self):
        actual = loads_properties([_create("com/sample/child/1.0.0/child-1.0.0.pom")])
        expected = {"sample.one.version": "2.4.0", "project.version": "1.0.0"}
        self.assertEqual(actual, expected)

    def test_read_nested_properties(self):
        actual = loads_properties([_create("com/sample/nested/1.0.0/nested-1.0.0.pom")])
        expected = {"sample.one.version": "2.4.0", "sample.two.version": "2.4.0", "sample.version": "2.4.0",
                    "project.version": "1.0.0"}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
