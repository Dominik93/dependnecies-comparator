def compare(reference_dependencies, dependencies):
    result = ""
    for reference_dependency in reference_dependencies:
        result = result + to_str(reference_dependency)
        dependency = _find_dependency(reference_dependency, dependencies)
        if dependency is not None:
            result = result + _compare_dependency(reference_dependency, dependency)
        else:
            result = result + " not found \n"
    return result


def _compare_dependency(reference_dependency, dependency):
    if reference_dependency['version'] == dependency['version']:
        return " == \n"
    else:
        return " != " + dependency['version'] + " \n"


def _find_dependency(reference_dependency, dependencies):
    for dependency in dependencies:
        if reference_dependency['groupId'] == dependency['groupId'] and reference_dependency['artifactId'] == \
                dependency['artifactId']:
            return dependency
    return None


def to_str(reference_dependency):
    return reference_dependency['groupId'] + ":" + reference_dependency['artifactId'] + ":" + reference_dependency['version']
