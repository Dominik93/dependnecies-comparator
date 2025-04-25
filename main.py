from configuration import load_configuration
from dependencies_comparator import compare
from dependencies_loader import loads_dependencies
from printer import print_dependencies

if __name__ == '__main__':
    config = load_configuration()

    reference_dependencies = loads_dependencies(config.references)
    compared_to_dependencies = loads_dependencies(config.compared_to)

    compared_dependencies = compare(reference_dependencies, compared_to_dependencies)

    print_dependencies(compared_dependencies, config.printer)
