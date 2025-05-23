import re


def compare_versions(reference_dependency: str, dependency: str) -> int:
    reference_parts = re.split('\.|-', reference_dependency)
    dependency_parts = re.split('\.|-', dependency)

    max_length = len(reference_parts) if len(reference_parts) > len(dependency_parts) else len(dependency_parts)
    for i in range(max_length):
        reference_part = "" if i >= len(reference_parts) else reference_parts[i]
        dependency_part = "" if i >= len(dependency_parts) else dependency_parts[i]
        value = _compare(reference_part, dependency_part)
        if value != 0:
            return value
    return 0


def _compare(first: str, second: str):
    if first == second:
        return 0
    return -1 if first > second else 1
