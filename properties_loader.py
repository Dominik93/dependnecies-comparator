import xmltodict

from models import FilePathInfo


def load_properties(file_path: FilePathInfo):
    return loads_properties([file_path])


def loads_properties(files: list[FilePathInfo]):
    properties = {}
    for file in files:
        properties.update(_load_properties(file))
    for key in properties:
        value = properties[key]
        if "$" in value:
            raw_value = value.replace("{", "").replace("$", "").replace("}", "")
            new_value = properties[raw_value] if raw_value in properties else value
            print(f'Resolve placeholder {key}:{value} as {new_value}')
            properties[key] = new_value
    return properties


def _load_properties(file_path: FilePathInfo):
    with open(file_path.local_path, "rb") as file:
        pom = xmltodict.parse(file)
        return _prepare_properties(pom)


def _prepare_properties(pom: dict):
    properties = {'project.version': pom['project']['version'] if 'version' in pom['project'] else ""}
    if properties['project.version'] != '':
        properties['project.version'] = pom['project']['parent']['version'] if 'parent' in pom['project'] else ""
    if 'properties' in pom['project']:
        properties_source = pom['project']['properties']
        for property_source in properties_source:
            property_value = properties_source[property_source]
            properties[property_source] = _parse(property_value) if property_value is not None else ""
            print(f"Prepared property {property_source}:{properties[property_source]}")
    return properties


def _parse(property_value: list | dict):
    if isinstance(property_value, list):
        return property_value[0]
    else:
        return property_value
