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


def depthFirstSearch(graph, o, c, depth):

    success = False

    while len(o) != 0:

        printStack(o, "open stack")
        printStack(c, "closed stack")

        if depth <= graph.max_d:
            root = o.pop()

            traversed = False
            for dot in c:
                if dot.position == root.position:
                    traversed = True
            if traversed:
                continue

            graph.dots.get(root.position).touch()

            if graph.isGoalState():
                printStack(o, "open stack")
                printStack(c, "closed stack")
                success = True
                break

            else:
                c.append(root)
                o.extend(graph.dots.get(root.position).adjacents)
                # depth += 1
                continue
        else:
            print("Maximum depth reached ... \n")
            break

    if not success:
        print("No solution found.")

    return success


def printStack(stack, stack_type):
    print("\n", stack_type, ": ", end=" ")
    for dot in stack:
        print(dot.position, end=" ")


graph = createGraph(os.path.join(sys.path[0], "test_sample.txt"))
o = []  # open stack tracks position
c = []  # closed stack tracks position
o.append(graph.dots.get("A1"))

print(depthFirstSearch(graph, o, c, 1))

