from models import Dependency


def compare(reference_dependencies: list[Dependency], dependencies: list[Dependency]):
    result = []
    for reference_dependency in reference_dependencies:
        dependency = _find_dependency(reference_dependency, dependencies)
        result.append({"reference": _to_str(reference_dependency),
                       "operator": _compare_dependency(reference_dependency, dependency),
                       "compared_to": _to_str(dependency)})
    return result


def _compare_dependency(reference_dependency: Dependency, dependency: Dependency):
    if dependency is not None:
        if reference_dependency.version == dependency.version:
            return "eq"
        else:
            return "ne"
    else:
        return "not found"


def _find_dependency(reference_dependency: Dependency, dependencies: list[Dependency]):
    for dependency in dependencies:
        if reference_dependency.group_id == dependency.group_id \
                and reference_dependency.artifact_id == dependency.artifact_id:
            return dependency
    return None


def _to_str(dependency: Dependency):
    if dependency is None:
        return ""
    return dependency.parent + ":" + dependency.group_id + ":" + dependency.artifact_id + \
        ":" + dependency.version
