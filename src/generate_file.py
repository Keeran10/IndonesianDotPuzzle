def generate_search_file(closed, puzzle_count, algorithm):
    if algorithm == "dfs":
        with open(str(puzzle_count) + "_dfs_search.txt", "w") as f:
            for line in closed.values():
                f.write("0" + "\t" + "0" + "\t" + "0" + "\t" + line.state + "\n")
    else:
        with open(str(puzzle_count) + "_bfs_search.txt", "w") as f:
            for line in closed:
                f.write(
                    str(line.heuristic)
                    + "\t"
                    + "g(n)"
                    + "\t"
                    + str(line.heuristic)
                    + "\t"
                    + line.state
                    + "\n"
                )


def generate_solution_file(goal_state, error, puzzle_count, algorithm):
    if algorithm == "dfs":
        filename = "_dfs_solution.txt"
    elif algorithm == "bfs":
        filename = "_bfs_solution.txt"

    with open(str(puzzle_count) + filename, "w") as f:

        if error == "No solution found.":
            f.write(error + "\n")
            return False

        solution = []

        get_solution_path(goal_state, solution)

        for line in solution:
            f.write(line.touched + "\t" + line.state + "\n")


def get_solution_path(root, solution):

    if root.parent == None:
        solution.reverse()
        return solution

    if len(solution) == 0:
        solution.append(root)

    solution.append(root.parent)
    get_solution_path(root.parent, solution)
