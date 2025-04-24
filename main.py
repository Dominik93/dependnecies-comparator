from configuration import load_configuration
from dependencies_comparator import compare
from dependencies_loader import loads_dependencies
from file_loader import load_files
from models import FilePathInfo
from printer import print_dependencies


def load(poms: list[FilePathInfo]):
    pom_files = load_files(poms)
    return loads_dependencies(pom_files)


if __name__ == '__main__':
    config = load_configuration()

    reference_dependencies = load(config.references)
    compared_to_dependencies = load(config.compared_to)

    compared_dependencies = compare(reference_dependencies, compared_to_dependencies)

    print_dependencies(compared_dependencies, config.printer)
