import json

from models import Config, Provider, FilePathInfo

CONFIG_JSON = 'config.json'

__config = None


def load_configuration() -> Config:
    global __config
    return __config if __config is not None else _load()


def _load() -> Config:
    with open(CONFIG_JSON) as config_file:
        config = json.load(config_file)

    providers = []
    for provider in config['providers']:
        providers.append(Provider(provider['name'], provider['path'], provider['strategy']))
    references = []
    for reference in config['references']:
        references.append(FilePathInfo(reference['path'], reference['provider'], ""))
    compared_to = []
    for compared in config['compared_to']:
        compared_to.append(FilePathInfo(compared['path'], compared['provider'], ""))

    return Config(config['printer'], providers, references, compared_to)
