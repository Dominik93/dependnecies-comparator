from models import File


class LocalFile(File):
    def __init__(self, local_path):
        self._local_path = local_path

    def spawn(self, path):
        return LocalFile(path)

    def local_path(self):
        return self._local_path


def create_local_file(path: str):
    return LocalFile(path)
