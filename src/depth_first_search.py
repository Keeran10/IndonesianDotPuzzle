import os, sys
from data_structure import Graph, Pair
from generate_file import generate_search_file, generate_solution_file
import copy, functools, time


def depth_first_search(o, c, max_d):

    print("Starting depth-first search...\n")

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

        print_stack(o, "opened")

        root = o.pop()

        if is_traversed(root, c):
            print("\nNode " + root.state + " has already been traversed.\n")
            continue

        print("\ntouch", root.touched)

        solution.append(Pair(root.touched, root.state))
        search.append(root.state)
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

        sorted(children, key=functools.cmp_to_key(compare_children))
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
    output.append(search)
    output.append(solution)
    output.append(error_message)

    return output


# Returns true if the state of the current node had already been traversed.
def is_traversed(root, c):
    for graph in c:
        # state contains a stringified representation of the state
        if root.state == graph.state:
            return True
    return False


# Returns the positive if child1 has white dots at earlier positions than child2
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

    for x in range(size):
        if child1_white_dots[x] == child2_white_dots[x]:
            continue
        else:
            return child1_white_dots[x] - child2_white_dots[x]
    return 0


# prints stack with positions to be touched
def print_stack(stack, stack_type):

    print(stack_type + ":")
    for x in range(len(stack) - 1, 0, -1):
        if stack[x].touched == None:
            continue
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
        generate_search_file(output[0], puzzle_count, "dfs")
        generate_solution_file(output[1], output[2], puzzle_count)
        puzzle_count += 1


if __name__ == "__main__":
    main()
