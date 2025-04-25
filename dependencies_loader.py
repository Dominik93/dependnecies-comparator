import xmltodict

from models import Dependency, File, DependencyFactory
from properties_loader import loads_properties


def load_dependencies(file: File) -> list[Dependency]:
    return loads_dependencies([file])


def loads_dependencies(files: list[File]) -> list[Dependency]:
    properties = loads_properties(files)

    all_dependencies = []
    for file in files:
        all_dependencies = all_dependencies + _load_dependencies(file, properties)
    return all_dependencies


def _load_dependencies(file: File, properties: dict) -> list[Dependency]:
    print(f'Load dependencies from {file}')
    with open(file.local_path(), "rb") as f:
        pom = xmltodict.parse(f)
        return _prepare_dependencies(file, pom, properties)


def _prepare_dependencies(file: File, pom: dict, properties: dict) -> list[Dependency]:
    dependencies = []
    if 'dependencyManagement' not in pom['project']:
        return dependencies
    source = pom['project']['artifactId']
    dependencies_source = pom['project']['dependencyManagement']['dependencies']
    for dependency in _get_dependencies(dependencies_source):
        dependency = DependencyFactory().create(source, dependency, properties)
        if dependency.scope == 'import':
            print(f'Load imported dependencies {dependency}')
            dependencies.extend(_prepare_imported_dependencies(file, dependency))
        else:
            print(f'Add dependency {dependency}')
            dependencies.append(dependency)
    return dependencies


def _prepare_imported_dependencies(file: File, dependency: Dependency) -> list[Dependency]:
    return load_dependencies(file.spawn(dependency.prepare_path()))


def _get_dependencies(dependencies_source: dict):
    dependency = dependencies_source['dependency']
    if isinstance(dependency, dict):
        return [dependency]
    return dependency
