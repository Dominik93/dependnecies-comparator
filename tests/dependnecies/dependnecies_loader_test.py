import unittest

from dependencies_loader import load_dependencies, loads_dependencies
from models import Dependency
from tests.file import create_local_file


class DependenciesLoaderTestCase(unittest.TestCase):
    def test_read_dependencies_from_file(self):
        properties = {"sample.one.version": "2.4.0", "sample.two.version": "4.3.2"}
        actual = load_dependencies(properties, create_local_file("resources/pom.xml"))
        expected = [
            Dependency("sample", "${sample.one.version}", "com.sample.one", "sample-one-one", "2.4.0", "runtime"),
            Dependency("sample", "2.0.0", "com.sample.one", "sample-one-two", "2.0.0", "runtime"),
            Dependency("sample", "${sample.two.version}", "com.sample.two", "sample-two-one", "4.3.2", "runtime"),
            Dependency("sample", "${sample.two.version}", "com.sample.two", "sample-two-two", "4.3.2", "runtime"),
            Dependency("sample", "${sample.two.version}", "com.sample.two", "sample-two-three", "4.3.2", "runtime")
        ]
        self.assertEqual(actual, expected)

    def test_read_dependencies_from_files(self):
        properties = {"sample.one.version": "2.4.0", "sample.two.version": "4.3.2"}
        actual = loads_dependencies(properties, [create_local_file("resources/pom_one.xml"),
                                                 create_local_file("resources/pom_two.xml")])
        expected = [
            Dependency("sample-one", "${sample.one.version}", "com.sample.one", "sample-one-one", "2.4.0", "runtime"),
            Dependency("sample-one", "2.0.0", "com.sample.one", "sample-one-two", "2.0.0", "runtime"),
            Dependency("sample-two", "${sample.two.version}", "com.sample.two", "sample-two-one", "4.3.2", "runtime"),
            Dependency("sample-two", "${sample.two.version}", "com.sample.two", "sample-two-two", "4.3.2", "runtime"),
            Dependency("sample-two", "${sample.two.version}", "com.sample.two", "sample-two-three", "4.3.2", "runtime")
        ]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
