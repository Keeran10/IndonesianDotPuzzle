def generate_search_file(closed, puzzle_count, algorithm):

    with open(str(puzzle_count) + "_dfs_search.txt", "w") as f:
        if algorithm == "dfs":
            for line in closed:
                f.write("0" + "\t" + "0" + "\t" + "0" + "\t" + line.state + "\n")


def generate_solution_file(closed, error, puzzle_count):

    with open(str(puzzle_count) + "_dfs_solution.txt", "w") as f:

        if error == "No solution found.":
            f.write(error + "\n")
            return False

        for line in closed:
            f.write(line.touched + "\t" + line.state + "\n")

