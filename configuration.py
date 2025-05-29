from models import Config, Provider, DefaultFile, DefaultFileProviderFactory, Providers, FileProviderFactory


def create_config(config) -> Config:
    providers = Providers(_load_providers(config))
    factory = DefaultFileProviderFactory(providers)

    references = _load_dependencies(config['references'], factory)
    compared_to = _load_dependencies(config['compared_to'], factory)

    return Config(config['printer'], providers, references, compared_to)


def _load_dependencies(dependencies: list, factory: FileProviderFactory):
    references = []
    for reference in dependencies:
        references.append(DefaultFile(factory, reference['path'], reference['provider']))
    return references


def _load_providers(config: dict):
    providers = []
    for provider in config['providers']:
        providers.append(Provider(provider['name'], provider['path'], provider['strategy']))
    return providers
