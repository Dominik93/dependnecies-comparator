import urllib.request

from configuration import load_configuration
from models import FilePathInfo


def load_files(file_paths: list[FilePathInfo]) -> list[FilePathInfo]:
    for file_path in file_paths:
        load_file(file_path)
    return file_paths


def load_file(file_path: FilePathInfo) -> FilePathInfo:
    file_path.local_path = _load_file(file_path.path, file_path.provider)
    print(f'Loaded file: {file_path}')
    return file_path


def _load_file(path: str, provider_name: str) -> str:
    config = load_configuration()
    provider = config.find_provider(provider_name)
    full_path = provider.path + path
    print(f'Get {provider.strategy} {full_path}')
    if provider.strategy == 'HTTP':
        return _load_http(full_path)
    if provider.strategy == 'FILE':
        return _load_local_file(full_path)


def _load_http(full_path):
    path = "runtime/" + full_path.split('/')[-1]
    urllib.request.urlretrieve(full_path, path)
    return path


def _load_local_file(full_path):
    return full_path
