def print_dependencies(dependencies, strategy):
    if strategy == 'CONSOLE':
        _print_console(dependencies)
    if strategy == "CSV":
        _print_csv(dependencies)


def _print_console(dependencies):
    print(str(dependencies))


def _print_csv(dependencies):
    f = open("result.csv", "w")
    f.write('reference;operator;compared to\n')
    for dependency in dependencies:
        f.write(dependency['reference'] + ";" + dependency['operator'] + ";" + dependency['compared_to'] + "\n")
    f.close()
