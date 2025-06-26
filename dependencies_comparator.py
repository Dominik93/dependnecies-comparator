from commons.optional import empty, Optional, of
from models import Dependency
from version_comparator import compare_versions


class CompareResult:

    def __init__(self, reference, property, operator, compared_to):
        self.reference = reference if reference is not None else "-"
        self.property = property if property is not None else "-"
        self.operator = operator if operator is not None else "-"
        self.compared_to = compared_to if compared_to is not None else "-"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if not isinstance(other, CompareResult):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.reference == other.reference and self.property == other.property and self.operator == other.operator and self.compared_to == other.compared_to


sign_by_value = {
    0: "eq",
    -1: "gt",
    1: "lt",
}


def compare(reference_dependencies: list[Dependency], dependencies: list[Dependency]) -> list[CompareResult]:
    result = []
    for reference_dependency in reference_dependencies:
        reference = str(reference_dependency)
        property = reference_dependency.property
        dependency = _find_dependency(reference_dependency, dependencies)
        operator = dependency.map(lambda dep: _compare(reference_dependency, dep)).or_get("not found")
        compared_to = dependency.map(lambda dep: str(dep)).or_get(None)
        result.append(CompareResult(reference, property, operator, compared_to))
    return result


def _compare(reference_dependency: Dependency, dependency: Dependency) -> str:
    return sign_by_value[compare_versions(dependency.version, reference_dependency.version)]


def _find_dependency(reference_dependency: Dependency, dependencies: list[Dependency]) -> Optional:
    for dependency in dependencies:
        if reference_dependency.same(dependency):
            return of(dependency)
    return empty()
