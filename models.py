import urllib.request


class FileProvider:

    def load(self):
        pass


class FileProviderFactory:

    def create(self, path: str, provider_name: str) -> FileProvider:
        pass


class File:

    def local_path(self):
        pass

    def spawn(self, path):
        pass


class DefaultFile(File):

    def __init__(self, loader_factory: FileProviderFactory, path: str, provider: str, local_path: str = None):
        self.path = path
        self.provider = provider
        self._local_path = local_path
        self.loader_factory = loader_factory

    def spawn(self, path):
        return DefaultFile(self.loader_factory, path, self.provider)

    def local_path(self):
        if self._local_path is not None:
            return self._local_path
        self._local_path = self.loader_factory.create(self.path, self.provider).load()
        return self._local_path

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)


class DependencyFactory:

    def create(self, source: str, dependency: dict, properties: dict):
        version = dependency['version'].replace("{", "").replace("$", "").replace("}", "")
        version = properties[version] if version in properties else version
        group_id = dependency['groupId']
        artifact_id = dependency['artifactId']
        scope = dependency['scope'] if 'scope' in dependency else "runtime"
        return Dependency(source, group_id, artifact_id, version, scope)


class Dependency:

    def __init__(self, source: str, group_id: str, artifact_id: str, version: str, scope: str):
        self.source = source
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.scope = scope

    def prepare_path(self):
        return f'{self.group_id.replace(".", "/")}/{self.artifact_id}/{self.version}/{self.artifact_id}-{self.version}.pom'

    def same(self, dependency):
        return self.group_id == dependency.group_id and self.artifact_id == dependency.artifact_id

    def __str__(self):
        return f'{self.source}:{self.group_id}:{self.artifact_id}:{self.version}'

    def __eq__(self, other):
        if not isinstance(other, Dependency):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.source == other.source and self.group_id == other.group_id and self.artifact_id == other.artifact_id and self.version == other.version and self.scope == other.scope


class Provider:
    def __init__(self, name: str, path: str, strategy: str):
        self.name = name
        self.path = path
        self.strategy = strategy

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)


class Providers:

    def __init__(self, providers: list[Provider]):
        self.providers = providers

    def find_provider(self, provider_name: str) -> Provider | None:
        for provider in self.providers:
            if provider.name == provider_name:
                return provider
        return None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)


class Config:
    def __init__(self, printer: str, providers: Providers, references: list[DefaultFile],
                 compared_to: list[DefaultFile]):
        self.printer = printer
        self.providers = providers
        self.references = references
        self.compared_to = compared_to

    def find_provider(self, provider_name: str) -> Provider | None:
        return self.providers.find_provider(provider_name)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)


class DefaultFileProviderFactory(FileProviderFactory):

    def __init__(self, providers: Providers):
        self.providers = providers

    def create(self, path: str, provider_name: str):
        provider = self.providers.find_provider(provider_name)

        full_path = provider.path + path
        print(f'Get {provider.strategy} {full_path}')
        if provider.strategy == 'HTTP':
            return HttpFileProvider(full_path)
        if provider.strategy == 'FILE':
            return FileFileProvider(full_path)


class FileFileProvider(FileProvider):

    def __init__(self, path: str):
        self.path = path

    def load(self):
        return self.path


class HttpFileProvider(FileProvider):

    def __init__(self, path: str):
        self.path = path

    def load(self):
        local_path = "runtime/" + self.path.split('/')[-1]
        urllib.request.urlretrieve(self.path, local_path)
        return local_path
