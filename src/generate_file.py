def generate_search_file(search, puzzle_count, algorithm):

    with open(str(puzzle_count) + "_dfs_search.txt", "a") as f:
        if algorithm == "dfs":
            for line in search:
                f.write("0" + "\t" + "0" + "\t" + "0" + "\t" + line + "\n")


def generate_solution_file(solution, error, puzzle_count):

    with open(str(puzzle_count) + "_dfs_solution.txt", "a") as f:

        if error == "No solution found.":
            f.write(error + "\n")
            return False

        for line in solution:
            f.write(line.touched + "\t" + line.state + "\n")

