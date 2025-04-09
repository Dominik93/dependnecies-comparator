def compare(reference_dependencies, dependencies):
    result = []
    for reference_dependency in reference_dependencies:
        dependency = _find_dependency(reference_dependency, dependencies)
        result.append({"reference": _to_str(reference_dependency),
                       "operator": _compare_dependency(reference_dependency, dependency),
                       "compared_to": _to_str(dependency)})
    return result


def _compare_dependency(reference_dependency, dependency):
    if dependency is not None:
        if reference_dependency['version'] == dependency['version']:
            return "eq"
        else:
            return "ne"
    else:
        return "not found"


def _find_dependency(reference_dependency, dependencies):
    for dependency in dependencies:
        if reference_dependency['groupId'] == dependency['groupId'] \
                and reference_dependency['artifactId'] == dependency['artifactId']:
            return dependency
    return None


def _to_str(dependency):
    if dependency is None:
        return ""
    return dependency['parent'] + ":" + dependency['groupId'] + ":" + dependency['artifactId'] + \
        ":" + dependency['version']
