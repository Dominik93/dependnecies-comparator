import re


def compare_versions(reference_dependency: str, dependency: str) -> int:
    reference_parts = re.split('\.|-', reference_dependency)
    dependency_parts = re.split('\.|-', dependency)

    max_length = max(len(reference_parts), len(dependency_parts))
    for i in range(max_length):
        reference_part = "0" if i >= len(reference_parts) else reference_parts[i]
        dependency_part = "0" if i >= len(dependency_parts) else dependency_parts[i]
        value = _compare(int(reference_part) if reference_part.isdigit() else reference_part,
                         int(dependency_part) if dependency_part.isdigit() else dependency_part)
        if value != 0:
            return value
    return 0


def _compare(first: str | int, second: str | int):
    if first == second:
        return 0
    return 1 if first > second else -1
