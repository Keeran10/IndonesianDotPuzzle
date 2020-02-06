import os, sys
from data_structure import Graph
from generate_file import generate_search_file, generate_solution_file
import copy, functools, time


def depth_first_search(o, c, max_d):

    print("Starting depth-first search...\n")

    success = False
    start = time.perf_counter()
    ALLOCATED_TIME = 10  # how long while loop should last in seconds
    duration = 0

    while len(o) != 0:

        # Time counter set to avoid extensive search
        duration = time.perf_counter() - start
        if duration > ALLOCATED_TIME:
            break

        print_stack(o, "opened")
        root = o.pop()

        if is_traversed(root, c):
            print("\nNode " + root.state + " has already been traversed.\n")
            continue

        print("\ntouch", root.touched)

        c.append(root)

        print_stack(c, "closed")
        root.print()

        # Exit DFS if root is goal state
        if root.is_goal_state():
            success = True
            break

        # Backtrack by not expanding root's children
        if root.depth == max_d:
            print(
                "\nMaximum depth reached. Children of node "
                + root.state
                + " will not be explored.\n"
            )
            continue

        # Add root's children to stack
        children = []
        for position in root.dots:
            child = copy.deepcopy(root)
            child.touch(position)
            child.depth = root.depth + 1
            children.append(child)

        # search priority given to states with earlier position of white dots
        children.sort(key=functools.cmp_to_key(compare_children))

        print(
            "Exploring children of "
            + root.state
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
    output.append(c)
    output.append(error_message)

    return output


# Returns true if the state of the current node had already been traversed.
def is_traversed(root, c):
    for graph in c:
        # state contains a stringified representation of the state
        if root.state == graph.state:
            return True
    return False


# Returns +1 if child1 has white dots at earlier positions than child2
def compare_children(child1, child2):

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

    for x in range(size - 1):
        if child1_white_dots[x] == child2_white_dots[x]:
            continue
        elif child1_white_dots[x] > child2_white_dots[x]:
            return -1
        elif child1_white_dots[x] < child2_white_dots[x]:
            return 1

    return 1


# prints stack with positions to be touched
def print_stack(stack, stack_type):

    print(stack_type + ":")

    if len(stack) == 1:
        print(stack[0].state, end=" ")
    else:
        for x in range(len(stack) - 1, -1, -1):
            print(stack[x].state, end=" ")


def main():
    # Toggle between the following lines for (1) easy access to test case or (2) perform dfs on demo file
    graphs = Graph.create_graphs(os.path.join(sys.path[0], "test_sample.txt"))
    # file_path = input("File Path: ")
    # graphs = createGraphs(file_path)
    puzzle_count = 0
    for graph in graphs:
        o = []  # open stack
        c = []  # closed stack
        o.append(graph)
        output = depth_first_search(o, c, graph.max_d)
        # output[0] = closed list, output[1] = error message
        generate_search_file(output[0], puzzle_count, "dfs")
        generate_solution_file(output[0], output[1], puzzle_count)
        puzzle_count += 1


if __name__ == "__main__":
    main()
