import json

condition_by_name = {
    "result": (lambda x: True),
    "eq": (lambda x: x.operator == 'eq'),
    "lt": (lambda x: x.operator == 'lt'),
    "gt": (lambda x: x.operator == 'gt'),
    "not_found": (lambda x: x.operator == 'not found')
}


class Row:

    def __init__(self, reference, operator, compared_to):
        self.reference = reference
        self.operator = operator
        self.compared_to = compared_to

    def csv(self):
        return self.reference + ";" + self.operator + ";" + self.compared_to

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if not isinstance(other, Row):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.reference == other.reference and self.operator == other.operator and self.compared_to == other.compared_to


def print_dependencies(dependencies: list[Row], strategy: str):
    if strategy == 'CONSOLE':
        _print_console(dependencies)
    if strategy == "CSV":
        _print_csv(dependencies)


def _print_console(dependencies: list[Row]):
    print(json.dumps([ob.__dict__ for ob in dependencies]))


def _print_csv(dependencies: list[Row]):
    for key in condition_by_name:
        _print_only_when(key, dependencies, condition_by_name[key])


def _print_only_when(name, dependencies, condition):
    f = open(f"resources/{name}.csv", "w")
    header = Row("reference", "operator", "compared_to")
    f.write(header.csv() + "\n")
    for dependency in list(filter(lambda x: condition(x), dependencies)):
        f.write(dependency.csv() + "\n")
    f.close()
