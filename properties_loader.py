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
        for property in properties_source:
            properties[property] = properties_source[property]
    return properties
