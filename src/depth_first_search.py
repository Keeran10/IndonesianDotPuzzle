import os, sys
from graph import Graph
import copy


def createGraph(file_path):
    with open(file_path, "r") as f:
        for line in f:
            data = line.split()
            n = data[0]
            max_d = data[1]
            max_l = data[2]
            values = data[3]

            return Graph(n, max_d, max_l, values)


def depthFirstSearch(o, c, max_d, depth):

    success = False

    while len(o) != 0:

        if depth <= max_d:

            root = o.pop()

            if isTraversed(root, c):
                print(
                    "\n" + root.touched + " touched state has already been traversed."
                )
                continue

            c.append(root)

            printStack(o, "opened")
            printStack(c, "closed")
            root.print()

            if root.isGoalState():
                success = True
                break

            black_dots = root.getBlackDots()
            black_dots.reverse()

            for black_dot in black_dots:
                child = copy.deepcopy(root)
                child.touch(black_dot)
                o.append(child)

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


def printStack(stack, stack_type):
    print("\n" + stack_type + ":", end=" ")
    for graph in stack:
        if graph.touched == None:
            continue
        print(graph.touched, end=" ")


graph = createGraph(os.path.join(sys.path[0], "test_sample.txt"))
o = []  # open stack tracks position
c = []  # closed stack tracks position
o.append(graph)

print(depthFirstSearch(o, c, graph.max_d, 1))
