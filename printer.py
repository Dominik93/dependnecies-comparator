def print_dependencies(dependencies, strategy):
    if strategy == 'CONSOLE':
        print(str(dependencies))
    if strategy == "CSV":
        f = open("result.csv", "w")
        f.write('reference;operator;compared_to\n')
        for dependency in dependencies:
            f.write(dependency['reference'] + ";" + dependency['operator'] + ";" + dependency['compared_to'] + "\n")
        f.close()
