import xmltodict

from models import File, DependencyFactory


def loads_properties(files: list[File]) -> dict:
    properties = {}
    for file in files:
        properties.update(load_properties(file))
    return _resolve_placeholders(properties)


def load_properties(file: File) -> dict:
    properties = _load_properties(file)
    return _resolve_placeholders(properties)


def _resolve_placeholders(properties: dict) -> dict:
    for key in properties:
        value = properties[key]
        if "$" in value:
            raw_value = value.replace("{", "").replace("$", "").replace("}", "")
            new_value = properties[raw_value] if raw_value in properties else value
            print(f'Resolve placeholder {key}:{value} as {new_value}')
            properties[key] = new_value
    return properties


def _load_properties(file: File) -> dict:
    with open(file.local_path(), "rb") as f:
        pom = xmltodict.parse(f)
        return _prepare_properties(file, pom)


def _prepare_properties(file: File, pom: dict) -> dict:
    properties = {'project.version': pom['project']['version'] if 'version' in pom['project'] else ""}
    if properties['project.version'] == '':
        properties['project.version'] = pom['project']['parent']['version'] if 'parent' in pom['project'] else ""
    properties.update(_prepare_parent_properties(file, pom))
    print(f"Prepared property project.version:{properties['project.version']}")
    if 'properties' in pom['project']:
        properties_source = pom['project']['properties']
        for property_source in properties_source:
            property_value = properties_source[property_source]
            properties[property_source] = _parse(property_value) if property_value is not None else ""
            print(f"Prepared property {property_source}:{properties[property_source]}")
    return properties


def _prepare_parent_properties(file: File, pom: dict) -> dict:
    print(f'Prepare parent properties')
    source = pom['project']['artifactId']
    if 'parent' in pom['project']:
        dependency = DependencyFactory().create(source, pom['project']['parent'], {})
        return _load_properties(file.spawn(dependency.prepare_path()))
    return {}


def _parse(property_value: list | dict) -> dict:
    if isinstance(property_value, list):
        return property_value[0]
    else:
        return property_value
