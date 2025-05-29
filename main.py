from commons.configuration_reader import read_configuration
from configuration import create_config
from dependencies_comparator import compare
from dependencies_loader import loads_dependencies
from printer import print_dependencies
from properties_loader import loads_properties

if __name__ == '__main__':
    config = read_configuration("config", lambda x: create_config(x))

    reference_dependencies = loads_dependencies(loads_properties(config.references), config.references)
    compared_to_dependencies = loads_dependencies(loads_properties(config.compared_to), config.compared_to)

    compared_dependencies = compare(reference_dependencies, compared_to_dependencies)

    print_dependencies(compared_dependencies, config.printer)
