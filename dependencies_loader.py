import xmltodict

import file_loader
from properties_loader import loads_properties
from models import FilePathInfo, Dependency


def load_dependencies(file_path: FilePathInfo) -> list[Dependency]:
    return loads_dependencies([file_path])


def loads_dependencies(files: list[FilePathInfo]) -> list[Dependency]:
    properties = loads_properties(files)

    all_dependencies = []
    for file in files:
        all_dependencies = all_dependencies + _load_dependencies(file, properties)
    return all_dependencies


def _load_dependencies(info: FilePathInfo, properties: dict) -> list[Dependency]:
    with open(info.local_path, "rb") as file:
        pom = xmltodict.parse(file)
        return _prepare_dependencies(info, pom, properties)


def _prepare_dependencies(info: FilePathInfo, pom: dict, properties: dict) -> list[Dependency]:
    dependencies = []
    if 'dependencyManagement' not in pom['project']:
        return dependencies
    parent = pom['project']['artifactId']
    dependencies_source = pom['project']['dependencyManagement']['dependencies']
    for dependency in _get_dependencies(dependencies_source):
        version = dependency['version'].replace("{", "").replace("$", "").replace("}", "")
        version = properties[version] if version in properties else version
        group_id = dependency['groupId']
        artifact_id = dependency['artifactId']
        scope = dependency['scope'] if 'scope' in dependency else ""
        dependency = Dependency(parent, group_id, artifact_id, version, scope)
        if scope == 'import':
            dependencies.extend(_prepare_imported_dependencies(info.provider, dependency))
        else:
            dependencies.append(dependency)
    return dependencies


def _prepare_imported_dependencies(provider_name: str, dependency: Dependency) -> list[Dependency]:
    url = _prepare_url(dependency)
    file = file_loader.load_file(FilePathInfo(url, provider_name, ""))
    return load_dependencies(file)


def _prepare_url(d: Dependency):
    return f'{d.group_id.replace(".", "/")}/{d.artifact_id}/{d.version}/{d.artifact_id}-{d.version}.pom'


def _get_dependencies(dependencies_source: dict):
    dependency = dependencies_source['dependency']
    if isinstance(dependency, dict):
        return [dependency]
    return dependency
