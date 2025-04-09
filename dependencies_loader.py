import xmltodict
from properties_loader import loads as loads_properties


def load(file_path):
    return loads([file_path])


def loads(files):
    properties = loads_properties(files)

    all_dependencies = []
    for file in files:
        all_dependencies = all_dependencies + _load_dependencies(file, properties)
    return all_dependencies


def _load_dependencies(file_path, properties):
    with open(file_path, "rb") as file:
        pom = xmltodict.parse(file)
        return _prepare_dependencies(pom, properties)


def _prepare_dependencies(pom, properties):
    dependencies = []
    if 'dependencyManagement' not in pom['project']:
        return dependencies
    parent = pom['project']['artifactId']
    dependencies_source = pom['project']['dependencyManagement']['dependencies']
    for dependency in dependencies_source['dependency']:
        version = dependency['version'].replace("{", "").replace("$", "").replace("}", "")
        if version in properties:
            version = properties[version]
        group_id = dependency['groupId']
        artifact_id = dependency['artifactId']
        dependencies.append({"parent": parent, "groupId": group_id, "artifactId": artifact_id, "version": version})
    return dependencies

