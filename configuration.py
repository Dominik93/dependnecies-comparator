import json

from models import Config, Provider, DefaultFile, DefaultFileProviderFactory, Providers, FileProviderFactory

CONFIG_JSON = 'config.json'

__config = None


def load_configuration() -> Config:
    global __config
    return __config if __config is not None else _load()


def _load() -> Config:
    with open(CONFIG_JSON) as config_file:
        config = json.load(config_file)

    providers = Providers(_load_providers(config))
    factory = DefaultFileProviderFactory(providers)

    references = _load_dependencies(config['references'], factory)
    compared_to = _load_dependencies(config['compared_to'], factory)

    return Config(config['printer'], providers, references, compared_to)


def _load_dependencies(dependencies: list, factory: FileProviderFactory):
    references = []
    for reference in dependencies:
        references.append(
            DefaultFile(factory, reference['path'], reference['provider']))
    return references


def _load_providers(config: dict):
    providers = []
    for provider in config['providers']:
        providers.append(Provider(provider['name'], provider['path'], provider['strategy']))
    return providers
