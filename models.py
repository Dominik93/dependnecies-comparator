class FilePathInfo:
    def __init__(self, path: str, provider: str, local_path: str):
        self.path = path
        self.provider = provider
        self.local_path = local_path

    def __str__(self):
        return f'Path: {self.path}, provider {self.provider}, local path: {self.local_path}'


class Dependency:
    def __init__(self, parent: str, group_id, artifact_id, version, scope):
        self.parent = parent
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.scope = scope

    def __str__(self):
        return f'{self.parent}:{self.group_id}:{self.artifact_id}:{self.version}:{self.scope}'

    def __eq__(self, other):
        if not isinstance(other, Dependency):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.parent == other.parent and self.group_id == other.group_id and self.artifact_id == other.artifact_id and self.version == other.version and self.scope == other.scope


class Provider:
    def __init__(self, name: str, path: str, strategy: str):
        self.name = name
        self.path = path
        self.strategy = strategy

    def __str__(self):
        return f'Name: {self.name}, path: {self.path}, strategy: {self.strategy}'


class Config:
    def __init__(self, printer: str, providers: list[Provider], references: list[FilePathInfo],
                 compared_to: list[FilePathInfo]):
        self.printer = printer
        self.providers = providers
        self.references = references
        self.compared_to = compared_to

    def find_provider(self, provider_name: str) -> Provider | None:
        for provider in self.providers:
            if provider.name == provider_name:
                return provider
        return None
