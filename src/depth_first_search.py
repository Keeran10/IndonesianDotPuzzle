import os, sys
from graph import Graph, Pair
import copy, functools, time


def createGraphs(file_path):
    graphs = []
    with open(file_path, "r") as f:
        for line in f:
            data = line.split()
            n = data[0]
            max_d = data[1]
            max_l = data[2]
            values = data[3]
            graphs.append(Graph(n, max_d, max_l, values))
    return graphs


def depthFirstSearch(o, c, max_d, puzzle_count):

    success = False
    solution = []
    search = []
    start = time.perf_counter()
    ALLOCATED_TIME = 30  # how long while loop should last in seconds
    duration = 0

    while len(o) != 0:

        # Time counter set to avoid extensive search
        duration = time.perf_counter() - start
        if duration > ALLOCATED_TIME:
            break

        printStack(o, "opened")

        root = o.pop()

        if isTraversed(root, c):
            print("\nNode " + root.readableDots + " has already been traversed.\n")
            continue

        print("\ntouch", root.touched)

        solution.append(Pair(root.touched, root.readableDots))
        search.append(root.readableDots)
        c.append(root)

        printStack(c, "closed")
        root.print()

        # Exit DFS if root is goal state
        if root.isGoalState():
            success = True
            break

        # Backtrack by not expanding root's children
        if root.depth == max_d:
            print(
                "\nMaximum depth reached. Children of node "
                + root.readableDots
                + " will not be explored.\n"
            )
            continue

        # Add root's children to stack
        black_dots = root.getBlackDots()
        black_dots.reverse()
        children = []

        for black_dot in black_dots:
            child = copy.deepcopy(root)
            child.touch(black_dot)
            child.depth = root.depth + 1
            children.append(child)

        sorted(children, key=functools.cmp_to_key(compareChildren))
        print(
            "Exploring children of "
            + root.readableDots
            + " (depth level: "
            + str(root.depth)
            + ").\n"
        )
        o.extend(children)

    goal_message = "Goal state achieved."
    error_message = " "

    if duration > ALLOCATED_TIME:
        print("\nDFS ran past allocated time of " + str(ALLOCATED_TIME) + " seconds.\n")
    else:
        print(f"\nDFS completed in {duration:0.4f} seconds.\n")

    if not success:
        goal_message = "Goal state not found.\n"
        error_message = "No solution found."

    print(goal_message)

    output = []
    output.append(search)
    output.append(solution)
    output.append(error_message)

    return output


# Returns true if the state of the current node had already been traversed.
def isTraversed(root, c):
    for graph in c:
        # readableDots contains a stringified representation of the state
        if root.readableDots == graph.readableDots:
            return True
    return False


# Returns the positive if child1 has white dots at earlier positions than child2
def compareChildren(child1, child2):

    child1_white_dots = []
    child2_white_dots = []

    for key in child1.dots:
        if child1.dots.get(key).value == 0:
            child1_white_dots.append(child1.dots.get(key).index)

    for key in child2.dots:
        if child2.dots.get(key).value == 0:
            child2_white_dots.append(child2.dots.get(key).index)

    size = (
        len(child2_white_dots)
        if len(child1_white_dots) >= len(child2_white_dots)
        else len(child1_white_dots)
    )

    for x in range(size):
        if child1_white_dots[x] == child2_white_dots[x]:
            continue
        else:
            return child1_white_dots[x] - child2_white_dots[x]
    return 0


# prints stack with positions to be touched
def printStack(stack, stack_type):
    print(stack_type + ":", end=" ")
    for graph in stack:
        if graph.touched == None:
            continue
        print(graph.touched, end=" ")


def generateSolutionFile(solution, error, puzzle_count):

    with open(str(puzzle_count) + "_dfs_solution.txt", "a") as f:

        if error == "No solution found.":
            f.write(error + "\n")
            return False

        for line in solution:
            f.write(line.position + "\t" + line.state + "\n")


def generateSearchFile(search, puzzle_count):

    with open(str(puzzle_count) + "_dfs_search.txt", "a") as f:

        for line in search:
            f.write("0" + "\t" + "0" + "\t" + "0" + "\t" + line + "\n")


def main():
    file_path = input("File Path: ")
    # Toggle between the following two lines for (1) easy access to test case or (2) perform dfs on demo file
    graphs = createGraphs(os.path.join(sys.path[0], "test_sample.txt"))
    # graphs = createGraphs(file_path)
    puzzle_count = 0
    for graph in graphs:
        o = []  # open stack
        c = []  # closed stack
        o.append(graph)
        output = depthFirstSearch(o, c, graph.max_d, puzzle_count)
        generateSearchFile(output[0], puzzle_count)
        generateSolutionFile(output[1], output[2], puzzle_count)
        puzzle_count += 1


if __name__ == "__main__":
    main()
