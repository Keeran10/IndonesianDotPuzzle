def generate_search_file(closed, puzzle_count, algorithm):

    # with open(str(puzzle_count) + "_dfs_search.txt", "w") as f:
    #     if algorithm == "dfs":
    #         for line in closed:
    #             f.write("0" + "\t" + "0" + "\t" + "0" + "\t" + line.state + "\n")

    with open(str(puzzle_count) + "_bfs_search.txt", "w") as f:
        if algorithm == "bfs":
            for line in closed:
                f.write("0" + "\t" + "0" + "\t" +
                        "0" + "\t" + line.state + "\n")


def generate_solution_file(goal_state, error, puzzle_count):

    # with open(str(puzzle_count) + "_dfs_solution.txt", "w") as f:

    #     if error == "No solution found.":
    #         f.write(error + "\n")
    #         return False

    #     solution = []

    #     get_solution_path(goal_state, solution)

    #     for line in solution:
    #         f.write(line.touched + "\t" + line.state + "\n")

    with open(str(puzzle_count) + "_bfs_solution.txt", "w") as f:

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
