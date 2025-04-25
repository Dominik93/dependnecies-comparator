from models import Dependency
from printer import Row


def compare(reference_dependencies: list[Dependency], dependencies: list[Dependency]) -> list[Row]:
    result = []
    for reference_dependency in reference_dependencies:
        dependency = _find_dependency(reference_dependency, dependencies)
        result.append(Row(_to_str(reference_dependency), _compare_dependency(reference_dependency, dependency),
                          _to_str(dependency)))
    return result


def _compare_dependency(reference_dependency: Dependency, dependency: Dependency) -> str:
    return _compare(reference_dependency, dependency) if dependency is not None else "not found"


def _compare(reference_dependency: Dependency, dependency: Dependency) -> str:
    if reference_dependency.version == dependency.version:
        return "eq"
    if reference_dependency.version > dependency.version:
        return "ge"
    else:
        return "lt"


def _find_dependency(reference_dependency: Dependency, dependencies: list[Dependency]) -> Dependency | None:
    for dependency in dependencies:
        if reference_dependency.same(dependency):
            return dependency
    return None


def _to_str(dependency: Dependency) -> str:
    return str(dependency) if dependency is not None else ""
