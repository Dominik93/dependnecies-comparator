
from pom_provider import get_pom
from dependencies_loader import loads
from dependencies_comparator import compare
from printer import print_dependencies
import json


def _get_files(poms):
    files = []
    for pom in poms:
        files.append(get_pom(pom['path'], pom['strategy']))
    return files


if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)
        reference_dependencies = loads(_get_files(config['reference_poms']))
        dependencies = loads(_get_files(config['poms']))
        compared_dependencies = compare(reference_dependencies, dependencies)
        print_dependencies(compared_dependencies, "CSV")
