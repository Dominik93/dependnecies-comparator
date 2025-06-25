from models import Dependency
from printer import Row
from version_comparator import compare_versions

sign_by_value = {
    0: "eq",
    -1: "gt",
    1: "lt",
}


def compare(reference_dependencies: list[Dependency], dependencies: list[Dependency]) -> list[Row]:
    result = []
    for reference_dependency in reference_dependencies:
        reference = _to_str(reference_dependency)
        property = reference_dependency.property if reference_dependency is not None else None
        dependency = _find_dependency(reference_dependency, dependencies)
        operator = _compare_dependency(reference_dependency, dependency)
        compared_to = _to_str(dependency)
        result.append(Row(reference, property, operator, compared_to))
    return result


def _compare_dependency(reference_dependency: Dependency, dependency: Dependency) -> str:
    return _compare(reference_dependency, dependency) if dependency is not None else "not found"


def _compare(reference_dependency: Dependency, dependency: Dependency) -> str:
    value = compare_versions(dependency.version, reference_dependency.version)
    return sign_by_value[value]


def _find_dependency(reference_dependency: Dependency, dependencies: list[Dependency]) -> Dependency | None:
    for dependency in dependencies:
        if reference_dependency.same(dependency):
            return dependency
    return None


def _to_str(dependency: Dependency) -> str:
    return str(dependency) if dependency is not None else None
