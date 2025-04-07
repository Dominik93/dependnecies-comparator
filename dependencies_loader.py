import xmltodict


def loads(files):
    all_dependencies = []
    for file in files:
        all_dependencies = all_dependencies + load(file)
    return all_dependencies


def load(file_path):
    with open(file_path, "rb") as file:
        pom = xmltodict.parse(file)
        properties = prepare_properties(pom)
        return prepare_dependencies(pom, properties)


def prepare_dependencies(pom, properties):
    dependencies = []
    dependencies_source = pom['project']['dependencyManagement']['dependencies']
    for dependency in dependencies_source['dependency']:
        version = dependency['version'].replace("{", "").replace("$", "").replace("}", "")
        if version in properties:
            version = properties[version]
        group_id = dependency['groupId']
        artifact_id = dependency['artifactId']
        dependencies.append({"groupId": group_id, "artifactId": artifact_id, "version": version})
    return dependencies


def prepare_properties(pom):
    properties = {}
    if 'properties' in pom['project']:
        properties_source = pom['project']['properties']
        for property in properties_source:
            properties[property] = properties_source[property]
    return properties
