import json


class Row:

    def __init__(self, reference, operator, compared_to):
        self.reference = reference
        self.operator = operator
        self.compared_to = compared_to

    def csv(self):
        return self.reference + ";" + self.operator + ";" + self.compared_to

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
    f = open("result.csv", "w")
    header = Row("reference", "operator", "compared_to")
    dependencies.insert(0, header)
    for dependency in dependencies:
        f.write(dependency.csv() + "\n")
    f.close()
