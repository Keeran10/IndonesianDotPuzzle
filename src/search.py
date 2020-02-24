import os
import sys
from data_structure import Graph
from generate_file import generate_search_file, generate_solution_file
import copy
import functools
import time


def depth_first_search(opened, closed):
    print("\nStarting depth-first search...\n")
    success = False
    start = time.perf_counter()
    ALLOCATED_TIME = 300  # how long while loop should last in seconds
    duration = 0

    while len(opened) != 0:
        # Time counter set to avoid extensive search
        duration = time.perf_counter() - start
        if duration > ALLOCATED_TIME:
            break

        # Remove root from opened list and print it
        ## print_stack(opened, "opened")
        root = opened.popitem()[1]

        print("\ntouch", root.touched)

        # Exit DFS if root is goal state
        if root.is_goal_state():
            success = True
            closed[root.state + str(root.depth)] = root
            ## print_stack(closed, "closed")
            root.print()
            break

        ## print_stack(closed, "closed")
        root.print()

        # Backtrack by not expanding root's children
        if root.depth == root.max_d:
            print(
                "\nMaximum depth reached. Children of node "
                + root.state
                + " will not be explored.\n"
            )
            continue

        # Generate root's children
        children = generate_children(root, opened, closed)

        # Add root to closed list
        closed[root.state + str(root.depth)] = root

        # Sort children by earliest occurence of white dots
        # Add them to opened list
        add_sorted_children_to_opened_list(root, children, opened)

    # print and extract required data for search/solution files into output list
    output = procress_dfs_results(closed, success, duration, ALLOCATED_TIME)

    return output


def best_first_search(opened, closed):
    print("\nStarting best-first search...\n")
    success = False
    start = time.perf_counter()
    ALLOCATED_TIME = 3000  # how long while loop should last in seconds
    duration = 0

    while len(opened) != 0:
        # Time counter set to avoid extensive search
        duration = time.perf_counter() - start
        if duration > ALLOCATED_TIME:
            break

        # Remove root from opened list and print it
        ## print_stack(opened, "opened")
        root = opened.pop()
        print("\ntouch", root.touched)
        root.get_heuristic()
        # Exit BFS if root is goal state
        if root.is_goal_state():
            success = True
            closed.append(root)
            ## print_stack(closed, "closed")
            root.print()
            break

        ## print_stack(closed, "closed")
        root.print()

        # Backtrack by not expanding root's children
        if root.depth == root.max_l:
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
        # Add them to opened list and then sort by heuristic
        add_children_to_opened_list_then_sort(root, children, opened)

    # print and extract required data for search/solution files into output list
    output = procress_dfs_results(closed, success, duration, ALLOCATED_TIME)

    return output


# Returns children filtered by known states in opened, closed lists


def generate_children(root, opened, closed):
    children = []
    for position in root.dots:
        # touching same position twice is redundant as it gives the same state
        if position == root.touched:
            continue
        child = copy.deepcopy(root)
        child.touch(position)
        if not is_in_opened_closed_lists(child, opened, closed):
            child.depth = root.depth + 1
            child.parent = root
            children.append(child)
    return children


# Returns true if the state of the current node is found in open or closed lists
def is_in_opened_closed_lists(child, opened, closed):
    is_known = False
    if opened.get(child.state + str(child.depth)) != None:
        is_known = True
    if closed.get(child.state + str(child.depth)) != None:
        is_known = True
    if is_known:
        print("\nChild " + child.state + " is a known state. Will not be traversed.\n")
    return is_known


# Sort and add children to opened list by heuristic
def add_children_to_opened_list_sort_by_heuristic(root, children, opened):
    if len(children) == 0:
        print("\nNode " + root.state + " does not have children to explore.\n")
    else:
        opened.extend(children)
        opened.sort(key=functools.cmp_to_key(sort_children_by_heuristic))
        print(
            "\nExploring children of "
            + root.state
            + " (depth level: "
            + str(root.depth)
            + ").\n"
        )


# Sort and add children to opened list
def add_sorted_children_to_opened_list(root, children, opened):
    if len(children) == 0:
        print("\nNode " + root.state + " does not have children to explore.\n")
    else:
        children.sort(key=functools.cmp_to_key(sort_children_by_leading_zeros))
        print(
            "\nExploring children of "
            + root.state
            + " (depth level: "
            + str(root.depth)
            + ").\n"
        )

        for child in children:
            opened[child.state + str(child.depth)] = child


# Returns +1 if child1 has white dots at earlier positions than child2
def sort_children_by_leading_zeros(child1, child2):
    for x in range(len(child1.state) - 1):
        character1 = child1.state[x]
        character2 = child2.state[x]
        if int(character1) == int(character2):
            continue
        elif int(character1) < int(character2):
            return 1
        else:
            return -1
    return 0


# Sort and add children to opened list
def add_children_to_opened_list_then_sort(root, children, opened):
    if len(children) == 0:
        print("\nNode " + root.state + " does not have children to explore.\n")
    else:
        opened.extend(children)
        opened.sort(key=functools.cmp_to_key(sort_children_by_heuristic))
        print(
            "\nExploring children of "
            + root.state
            + " (depth level: "
            + str(root.depth)
            + ").\n"
        )


# Returns +1 if child1 has white dots at less positions than child2
def sort_children_by_heuristic(child1, child2):
    character1 = child1.get_heuristic()
    character2 = child2.get_heuristic()
    if int(character1) == int(character2):
        # if equals, sort by leading zero
        sort_children_by_leading_zeros(child1, child2)
    if int(character1) < int(character2):
        return 1
    else:
        return -1
    return 0


# prints stack with positions to be touched
def print_stack(stack, stack_type):

    print(stack_type + ":")

    if len(stack) == 1:
        print(stack[0].state, end=" ")
    else:
        for x in range(len(stack) - 1, -1, -1):
            print(stack[x].state, end=" ")


def procress_bfs_results(closed, success, duration, ALLOCATED_TIME):
    goal_message = "Goal state achieved."
    error_message = " "

    if duration > ALLOCATED_TIME:
        print("\nBFS ran past allocated time of " + str(ALLOCATED_TIME) + " seconds.\n")
    else:
        print(f"\nBFS completed in {duration:0.4f} seconds.\n")

    if not success:
        goal_message = "Goal state not found.\n"
        error_message = "No solution found."

    print(goal_message)

    output = []
    output.append(closed)
    output.append(closed[-1])
    output.append(error_message)
    return output


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
    output.append(list(closed.values())[-1])
    output.append(error_message)
    return output


def main():
    # Toggle between the following lines for (1) easy access to test case or (2) perform dfs on demo file
    graphs = Graph.create_graphs(os.path.join(sys.path[0], "sample.txt"))
    # file_path = input("File Path: ")
    # graphs = createGraphs(file_path)
    puzzle_count = 0
    for graph in graphs:
        o = {}  # open stack
        c = {}  # closed stack
        o[graph.state + str(graph.depth)] = graph
        output = depth_first_search(o, c)
        # output = best_first_search(o, c)
        # output[0] = search path, output[1] = solution path, output[2] = error message
        generate_search_file(output[0], puzzle_count, "dfs")
        generate_solution_file(output[1], output[2], puzzle_count, "dfs")
        puzzle_count += 1


if __name__ == "__main__":
    main()
