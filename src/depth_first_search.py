import os, sys
from graph import Graph
import copy, functools


def createGraph(file_path):
    with open(file_path, "r") as f:
        line = f.readline()
        data = line.split()
        n = data[0]
        max_d = data[1]
        max_l = data[2]
        values = data[3]
        return Graph(n, max_d, max_l, values)
    return None


def depthFirstSearch(o, c, max_d):

    success = False
    depth = 1

    while len(o) != 0:

        printStack(o, "opened")

        if depth <= max_d:

            root = o.pop()
            print("\ntouch", root.touched)

            if isTraversed(root, c):
                print(root.touched + " touched state has already been traversed.\n")
                continue

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

            # print("\n", children)
            # sort children by their white dots at earlier positions
            sorted(children, key=functools.cmp_to_key(compareChild))
            # print("\n", children)
            # children.reverse()
            o.extend(children)

            depth += 1

        else:
            print("\nMaximum depth reached ... \n")
            break

    if not success:
        print("\nNo solution found.")

    return success


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


graph = createGraph(os.path.join(sys.path[0], "test_sample.txt"))

if graph is not None:
    o = []  # open stack tracks position
    c = []  # closed stack tracks position
    o.append(graph)

    print(depthFirstSearch(o, c, graph.max_d))
