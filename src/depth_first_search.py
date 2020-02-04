import os, sys
from graph import Graph


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

            root.print()

            if isTraversed(root, c):
                continue

            c.append(root)

            if root.isGoalState():
                success = True
                break

            black_dots = root.getBlackDots()
            black_dots.reverse()

            for black_dot in black_dots:
                child = root
                child.dots.get(black_dot).touch()
                o.append(child)

            break
            # depth += 1

        else:
            print("Maximum depth reached ... \n")
            break

    printStack(o, "open stack")
    printStack(c, "closed stack")

    if not success:
        print("\nNo solution found.")

    return success


def isTraversed(root, c):
    traversed = False
    for dots in c:
        if root.dots == dots:
            traversed = True
    return traversed


def printStack(stack, stack_type):
    print("\n", stack_type, ": ", end=" ")
    for graph in stack:
        print(graph.print(), end=" ")


graph = createGraph(os.path.join(sys.path[0], "test_sample.txt"))
o = []  # open stack tracks position
c = []  # closed stack tracks position
o.append(graph)

print(depthFirstSearch(o, c, graph.max_d, 1))

