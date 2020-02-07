import os, sys
from data_structure import Graph
from generate_file import generate_search_file, generate_solution_file
import copy, functools, time


def depth_first_search(opened, closed, max_depth):
    print("\nStarting depth-first search...\n")
    success = False
    start = time.perf_counter()
    ALLOCATED_TIME = 100  # how long while loop should last in seconds
    duration = 0

    while len(opened) != 0:
        # Time counter set to avoid extensive search
        duration = time.perf_counter() - start
        if duration > ALLOCATED_TIME:
            break

        # Remove root from opened list and print it
        print_stack(opened, "opened")
        root = opened.pop()
        print("\ntouch", root.touched)

        # Exit DFS if root is goal state
        if root.is_goal_state():
            success = True
            closed.append(root)
            print_stack(closed, "closed")
            root.print()
            break

        print_stack(closed, "closed")
        root.print()

        # Backtrack by not expanding root's children
        if root.depth == max_depth:
            print(
                "\nMaximum depth reached. Children of node "
                + root.state
                + " will not be explored.\n"
            )
            continue

        # Generate root's children
        children = generate_children(root, opened, closed)

        # Add root to closed list
        closed.append(root)

        # Sort children by earliest occurence of white dots
        # Add them to opened list
        add_sorted_children_to_opened_list(root, children, opened)

    # print and extract required data for search/solution files into output list
    output = procress_dfs_results(closed, success, duration, ALLOCATED_TIME)

    return output


# Returns children filtered by known states in opened, closed lists
def generate_children(root, opened, closed):
    children = []
    for position in root.dots:
        root.touch(position, True)
        if is_in_open_closed_lists(root, opened, closed):
            root.touch(position, True)
        else:
            root.touch(position, True)
            child = copy.deepcopy(root)
            child.touch(position, False)
            child.depth = root.depth + 1
            child.parent = root
            children.append(child)
    return children


# Returns true if the state of the current node is found in open or closed lists
def is_in_open_closed_lists(root, o, c):
    is_known = False
    for graph in c:
        # state contains a stringified representation of the state
        if root.state == graph.state:
            is_known = True
    for graph in o:
        if root.state == graph.state:
            is_known = True

    if is_known:
        print_stack(o, "opened")
        print("\nChild " + root.state + " is a known state. Will not be traversed.\n")
    return is_known


# Sort and add children to opened list
def add_sorted_children_to_opened_list(root, children, opened):
    if len(children) == 0:
        print("\nNode " + root.state + " does not have children to explore.\n")
    else:
        children.sort(key=functools.cmp_to_key(compare_children))
        print(
            "\nExploring children of "
            + root.state
            + " (depth level: "
            + str(root.depth)
            + ").\n"
        )
        opened.extend(children)


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


def procress_dfs_results(closed, success, duration, ALLOCATED_TIME):
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
    output.append(closed)
    output.append(closed[-1])
    output.append(error_message)
    return output


def main():
    # Toggle between the following lines for (1) easy access to test case or (2) perform dfs on demo file
    graphs = Graph.create_graphs(os.path.join(sys.path[0], "sample.txt"))
    # file_path = input("File Path: ")
    # graphs = createGraphs(file_path)
    puzzle_count = 0
    for graph in graphs:
        o = []  # open stack
        c = []  # closed stack
        o.append(graph)
        output = depth_first_search(o, c, graph.max_d)
        # output[0] = search path, output[1] = solution path, output[2] = error message
        generate_search_file(output[0], puzzle_count, "dfs")
        generate_solution_file(output[1], output[2], puzzle_count)
        puzzle_count += 1


if __name__ == "__main__":
    main()
