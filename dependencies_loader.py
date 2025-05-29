import xmltodict

from commons.logger import get_logger
from models import Dependency, File, DependencyFactory
from properties_loader import load_properties

logger = get_logger("DependenciesLoader")


def loads_dependencies(properties: dict, files: list[File]) -> list[Dependency]:
    all_dependencies = []
    for file in files:
        all_dependencies.extend(load_dependencies(properties, file))
    return all_dependencies


def load_dependencies(properties: dict, file: File) -> list[Dependency]:
    return _load_dependencies(file, properties)


def _load_dependencies(file: File, properties: dict) -> list[Dependency]:
    logger.debug("_load_dependencies", f'Load dependencies from {file}')
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
            logger.debug("_prepare_dependencies", f'Load imported dependencies {dependency}')
            dependencies.extend(_prepare_imported_dependencies(file, dependency))
        else:
            logger.debug("_prepare_dependencies", f'Add dependency {dependency}')
            dependencies.append(dependency)
    return dependencies


def _prepare_imported_dependencies(file: File, dependency: Dependency) -> list[Dependency]:
    file_spawn = file.spawn(dependency.prepare_path())
    properties = load_properties(file_spawn)
    return load_dependencies(properties, file_spawn)


def _get_dependencies(dependencies_source: dict):
    dependency = dependencies_source['dependency']
    if isinstance(dependency, dict):
        return [dependency]
    return dependency
