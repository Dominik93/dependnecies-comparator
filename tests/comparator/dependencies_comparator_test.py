import unittest
from dependencies_comparator import compare


class MyTestCase(unittest.TestCase):
    def test_read_dependencies_from_file(self):
        reference_dependencies = [
            {"groupId": "com.sample.two", "artifactId": "sample-two-one", "version": "4.3.2"},
            {"groupId": "com.sample.two", "artifactId": "sample-two-two", "version": "4.3.2"},
            {"groupId": "com.sample.two", "artifactId": "sample-two-three", "version": "4.3.2"},
            {"groupId": "com.sample.one", "artifactId": "sample-one-one", "version": "2.4.0"},
            {"groupId": "com.sample.one", "artifactId": "sample-one-two", "version": "2.0.0"}]

        dependencies = [{"groupId": "com.sample.two", "artifactId": "sample-two-one", "version": "4.0.2"},
                        {"groupId": "com.sample.two", "artifactId": "sample-two-two", "version": "4.3.2"},
                        {"groupId": "com.sample.one", "artifactId": "sample-one-one", "version": "2.4.1"},
                        {"groupId": "com.sample.one", "artifactId": "sample-one-two", "version": "2.0.0"}]
        actual = compare(reference_dependencies, dependencies)
        self.assertEqual(actual, 'com.sample.two:sample-two-one:4.3.2 != 4.0.2 \n'
                                 'com.sample.two:sample-two-two:4.3.2 == \n'
                                 'com.sample.two:sample-two-three:4.3.2 not found \n'
                                 'com.sample.one:sample-one-one:2.4.0 != 2.4.1 \n'
                                 'com.sample.one:sample-one-two:2.0.0 == \n')


if __name__ == '__main__':
    unittest.main()
