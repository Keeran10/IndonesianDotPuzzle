import os, sys
from graph import Graph, Pair
import copy, functools
import multiprocessing
import time


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
    backtrack_index = 0
    backtracked_node_count = 0
    depth = 1
    solution = []
    search = []

    while len(o) != 0:

        printStack(o, "opened")

        if depth <= max_d:

            root = o.pop()

            if isTraversed(root, c):
                print(
                    "\n" + root.touched + " touched state has already been traversed.\n"
                )
                continue

            print("\ntouch", root.touched, "(depth level: " + str(depth) + ").")

            solution.append(Pair(root.touched, root.readableDots))

            c.append(root)

            printStack(c, "closed")
            root.print()

            if root.isGoalState():
                success = True
                break

            black_dots = root.getBlackDots()
            black_dots.reverse()
            children = []

            for black_dot in black_dots:
                child = copy.deepcopy(root)
                child.touch(black_dot)
                children.append(child)

            # store backtrack index
            if depth == 1:
                backtrack_index = len(children) - 1 - backtracked_node_count
                backtracked_node_count += 1
                search.append(root.readableDots)

            # sort children by their white dots at earlier positions
            sorted(children, key=functools.cmp_to_key(compareChild))
            o.extend(children)
            depth += 1

        else:
            print(
                "\nMaximum depth reached (backtracking nodes: "
                + str(backtracked_node_count)
                + ")... \n"
            )
            # add to search path then change node to explore
            o = o[:backtrack_index]
            depth = 1
            continue

    if not success:
        printStack(c, "closed")
        print("\n\nNo solution found.")
        generateSolutionFile([], "no solution", puzzle_count)
        generateSearchFile(search, puzzle_count)
        return False

    generateSolutionFile(solution, " ", puzzle_count)
    generateSearchFile(search, puzzle_count)
    print("Goal state achieved.")
    return True


def isTraversed(root, c):
    for graph in c:
        if root.readableDots == graph.readableDots:
            return True
    return False


def compareChild(graph1, graph2):

    graph1_white_dots = []
    graph2_white_dots = []

    for key in graph1.dots:
        if graph1.dots.get(key).value == 0:
            graph1_white_dots.append(graph1.dots.get(key).index)

    for key in graph2.dots:
        if graph2.dots.get(key).value == 0:
            graph2_white_dots.append(graph2.dots.get(key).index)

    size = (
        len(graph2_white_dots)
        if len(graph1_white_dots) >= len(graph2_white_dots)
        else len(graph1_white_dots)
    )

    for x in range(size):
        if graph1_white_dots[x] == graph2_white_dots[x]:
            continue
        else:
            return graph1_white_dots[x] - graph2_white_dots[x]
    return 0


def printStack(stack, stack_type):
    print(stack_type + ":", end=" ")
    for graph in stack:
        if graph.touched == None:
            continue
        print(graph.touched, end=" ")


def generateSolutionFile(solution, error, puzzle_count):

    with open(str(puzzle_count) + "_dfs_solution.txt", "a") as f:

        if error == "no solution":
            f.write(error + "\n")
            return False

        for line in solution:
            f.write(line.position + "\t" + line.state + "\n")


def generateSearchFile(search, puzzle_count):

    with open(str(puzzle_count) + "_dfs_search.txt", "a") as f:

        for line in search:
            f.write("0" + "\t" + "0" + "\t" + "0" + "\t" + line + "\n")


def main():
    graphs = createGraphs(os.path.join(sys.path[0], "test_sample.txt"))
    puzzle_count = 0
    for graph in graphs:
        o = []  # open stack tracks position
        c = []  # closed stack tracks position
        o.append(graph)
        depthFirstSearch(o, c, graph.max_d, puzzle_count)
        puzzle_count += 1


if __name__ == "__main__":
    # Code to kill depth search function taken from stackoverflow at:
    # https://stackoverflow.com/questions/14920384/stop-code-after-time-period
    # Start main as a process
    p = multiprocessing.Process(target=main, name="main")
    p.start()

    # Wait x seconds for main
    time.sleep(10)

    # If thread is active
    if p.is_alive():
        print("\n\nDFS is running for more than 10 seconds. Terminating...")
        # Terminate main
        p.terminate()
        p.join()
