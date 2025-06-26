import json

from commons.csv_writer import write
from dependencies_comparator import CompareResult

condition_by_name = {
    "result": (lambda x: True),
    "eq": (lambda x: x.operator == 'eq'),
    "lt": (lambda x: x.operator == 'lt'),
    "gt": (lambda x: x.operator == 'gt'),
    "not_found": (lambda x: x.operator == 'not found')
}


def print_dependencies(dependencies: list[CompareResult], strategy: str):
    if strategy == 'CONSOLE':
        _print_console(dependencies)
    if strategy == "CSV":
        _print_csv(dependencies)


def _print_console(dependencies: list[CompareResult]):
    print(json.dumps([ob.__dict__ for ob in dependencies]))


def _print_csv(dependencies: list[CompareResult]):
    for key in condition_by_name:
        _print_only_when(key, dependencies, condition_by_name[key])


def _print_only_when(name, dependencies, condition):
    content = list(map(lambda d: d.__dict__, list(filter(lambda d: condition(d), dependencies))))
    write(f"resources/{name}.csv", content)
