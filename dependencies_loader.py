import xmltodict

from commons.logger import get_logger
from models import Dependency, File, DependencyFactory
from properties_loader import load_properties

logger = get_logger("DependenciesLoader")


def loads_dependencies(properties: dict, files: list[File]) -> list[Dependency]:
    return Loader().loads_dependencies(properties, files)


class Loader:

    def __init__(self, ):
        self._loaded_files = []

    def loads_dependencies(self, properties: dict, files: list[File]) -> list[Dependency]:
        all_dependencies = []
        for file in files:
            all_dependencies.extend(self.load_dependencies(properties, file))
        return all_dependencies

    def load_dependencies(self, properties: dict, file: File) -> list[Dependency]:
        return self._load_dependencies(file, properties)

    def _load_dependencies(self, file: File, properties: dict) -> list[Dependency]:
        logger.debug("_load_dependencies", f'Load dependencies from {file}')
        if file.local_path() not in self._loaded_files:
            self._loaded_files.append(file.local_path())
            with open(file.local_path(), "rb") as f:
                pom = xmltodict.parse(f)
                return self._prepare_dependencies(file, pom, properties)
        return []

    def _prepare_dependencies(self, file: File, pom: dict, properties: dict) -> list[Dependency]:
        dependencies = []
        if 'dependencyManagement' not in pom['project']:
            return dependencies
        source = pom['project']['artifactId']
        dependencies_source = pom['project']['dependencyManagement']['dependencies']
        for dependency in self._get_dependencies(dependencies_source):
            dependency = DependencyFactory().create(source, dependency, properties)
            if dependency.scope == 'import':
                logger.debug("_prepare_dependencies", f'Load imported dependencies {dependency}')
                dependencies.extend(self._prepare_imported_dependencies(file, dependency))
            else:
                logger.debug("_prepare_dependencies", f'Add dependency {dependency}')
                dependencies.append(dependency)
        return dependencies

    def _prepare_imported_dependencies(self, file: File, dependency: Dependency) -> list[Dependency]:
        file_spawn = file.spawn(dependency.prepare_path())
        properties = load_properties(file_spawn)
        return self.load_dependencies(properties, file_spawn)

    def _get_dependencies(self, dependencies_source: dict):
        dependency = dependencies_source['dependency']
        if isinstance(dependency, dict):
            return [dependency]
        return dependency
