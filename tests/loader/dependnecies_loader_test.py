import unittest

from dependencies_loader import load_dependencies, loads_dependencies
from models import FilePathInfo, Dependency


def _create(path: str):
    return FilePathInfo(None, None, path)


class DependenciesLoaderTestCase(unittest.TestCase):
    def test_read_dependencies_from_file(self):
        actual = load_dependencies(_create("resources/pom.xml"))
        expected = [
            Dependency("sample", "com.sample.one", "sample-one-one", "2.4.0", ""),
            Dependency("sample", "com.sample.one", "sample-one-two", "2.0.0", ""),
            Dependency("sample", "com.sample.two", "sample-two-one", "4.3.2", ""),
            Dependency("sample", "com.sample.two", "sample-two-two", "4.3.2", ""),
            Dependency("sample", "com.sample.two", "sample-two-three", "4.3.2", "")
        ]
        self.assertEqual(actual, expected)

    def test_read_dependencies_from_files(self):
        actual = loads_dependencies([_create("resources/pom_one.xml"), _create("resources/pom_two.xml")])
        expected = [
            Dependency("sample", "com.sample.one", "sample-one-one", "2.4.0", ""),
            Dependency("sample", "com.sample.one", "sample-one-two", "2.0.0", ""),
            Dependency("sample", "com.sample.two", "sample-two-one", "4.3.2", ""),
            Dependency("sample", "com.sample.two", "sample-two-two", "4.3.2", ""),
            Dependency("sample", "com.sample.two", "sample-two-three", "4.3.2", "")
        ]
        self.assertEqual(actual, expected)

    def test_read_dependencies_inherited(self):
        actual = loads_dependencies([_create("resources/pom_child.xml"), _create("resources/pom_parent.xml")])
        expected = [
            Dependency("sample", "com.sample.one", "sample-one-one", "2.4.0", ""),
            Dependency("sample", "com.sample.one", "sample-one-two", "2.0.0", "")
        ]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
