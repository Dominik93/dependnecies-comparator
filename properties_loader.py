import xmltodict


def load(file_path):
    return loads([file_path])


def loads(files):
    properties = {}
    for file in files:
        properties.update(_load_properties(file))
    for key in properties:
        value = properties[key]
        if "$" in value:
            properties[key] = properties[value.replace("{", "").replace("$", "").replace("}", "")]
    return properties


def _load_properties(file_path):
    with open(file_path, "rb") as file:
        pom = xmltodict.parse(file)
        return _prepare_properties(pom)


def _prepare_properties(pom):
    properties = {}
    if 'properties' in pom['project']:
        properties_source = pom['project']['properties']
        for property_source in properties_source:
            property_value = properties_source[property_source]
            properties[property_source] = _parse(property_value) if property_value is not None else ""
    return properties


def _parse(property_value):
    if isinstance(property_value, list):
        return property_value[0]
    else:
        return property_value
