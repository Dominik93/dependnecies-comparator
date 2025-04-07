import urllib.request


def get_pom(path, strategy):
    if strategy == 'HTTP':
        urllib.request.urlretrieve(path, path.split('/')[-1])
        return path.split('/')[-1]
    if strategy == 'FILE':
        return path
