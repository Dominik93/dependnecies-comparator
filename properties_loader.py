import xmltodict

from commons.dictionary import Dictionary
from commons.logger import get_logger
from commons.optional import of
from models import File, DependencyFactory

logger = get_logger("PropertiesLoader")


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
            logger.debug("_resolve_placeholders", f'Resolve placeholder {key}:{value} as {new_value}')
            properties[key] = new_value
    return properties


def _load_properties(file: File) -> dict:
    with open(file.local_path(), "rb") as f:
        pom = xmltodict.parse(f)
        return _prepare_properties(file, Dictionary(pom))


def _prepare_properties(file: File, pom: Dictionary) -> dict:
    properties = {'project.version': pom.get_value("project.version", "")}
    if properties['project.version'] == '':
        properties = {'project.version': pom.get_value("project.parent.version", "")}
    properties.update(_prepare_parent_properties(file, pom))
    logger.debug("_prepare_properties", f"Prepared property project.version:{properties['project.version']}")
    pom.do_with("project.properties", lambda props: _add_properties(properties, props))
    return properties


def _add_properties(properties, properties_source):
    for property_source in properties_source:
        property_value = of(properties_source[property_source])
        properties[property_source] = property_value.map(lambda value: _parse(value)).or_get("")
        logger.debug("_add_properties", f"Added property {property_source}:{properties[property_source]}")


def _prepare_parent_properties(file: File, pom: Dictionary) -> dict:
    logger.debug("_prepare_parent_properties", f'Prepare parent properties')
    return pom.map("project.parent", lambda parent: _load_parent(file, pom, parent), {})


def _load_parent(file: File, pom: Dictionary, parent) -> dict:
    dependency = DependencyFactory().create(pom.get_value('project.artifactId'), parent, {})
    return _load_properties(file.spawn(dependency.prepare_path()))


def _parse(property_value: list | dict) -> dict:
    if isinstance(property_value, list):
        return property_value[0]
    else:
        return property_value
