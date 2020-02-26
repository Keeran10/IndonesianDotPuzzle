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
    ALLOCATED_TIME = 3000  # how long while loop should last in seconds
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
        children = generate_children(root, opened, closed, "DFS")

        # Add root to closed list
        closed[root.state + str(root.depth)] = root

        # Sort children by earliest occurence of white dots
        # Add them to opened list
        add_sorted_children_to_opened_list(root, children, opened)

    # print and extract required data for search/solution files into output list
    output = process_results(closed, success, duration, ALLOCATED_TIME, "DFS")

    return output


def best_first_search(opened, closed, max_length):
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
        root = opened.popitem()[1]
        print("\ntouch", root.touched)
        root.get_heuristic()
        # Exit BFS if root is goal state
        if root.is_goal_state():
            success = True
            closed[root.state + str(root.depth)] = root
            ## print_stack(closed, "closed")
            root.print()
            break

        ## print_stack(closed, "closed")
        root.print()

        # Generate root's children
        children = generate_children(root, opened, closed, "BFS")

        # Add root to closed list
        closed[root.state + str(root.depth)] = root

        if len(closed) == max_length:
            print("Max search length reached of " + str(max_length) + ". Aborting...")
            break

        # Sort children by earliest occurence of white dots
        # Add them to opened list and then sort by heuristic
        add_children_to_opened_list_then_sort(root, children, opened, "BFS")

    # print and extract required data for search/solution files into output list
    output = process_results(closed, success, duration, ALLOCATED_TIME, "BFS")

    return output


def algorithm_a_star(opened, closed, max_length):
    print("\nStarting algorithm a star...\n")
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
        # print_stack(opened, "opened")
        root = opened.popitem()[1]
        print("\ntouch", root.touched)
        root.get_fn()
        # Exit BFS if root is goal state
        if root.is_goal_state():
            success = True
            closed[root.state + str(root.depth)] = root
            # print_stack(closed, "closed")
            root.print()
            break

        # print_stack(closed, "closed")
        root.print()

        # Generate root's children
        children = generate_children(root, opened, closed, "a-star")

        # Add root to closed list
        closed[root.state + str(root.depth)] = root

        if len(closed) == max_length:
            print("Max search length reached of " + str(max_length) + ". Aborting...")
            break

        # Sort children by earliest occurence of white dots
        # Add them to opened list and then sort by heuristic
        add_children_to_opened_list_then_sort(root, children, opened, "a_star")

    # print and extract required data for search/solution files into output list
    output = process_results(closed, success, duration, ALLOCATED_TIME, "A star")

    return output


# Returns children filtered by known states in opened, closed lists


def generate_children(root, opened, closed, algorithm):
    children = []
    for position in root.dots:
        # touching same position twice is redundant as it gives the same state
        if position == root.touched:
            continue
        child = Graph(root.n, root.max_d, root.max_l, root.state)
        child.touch(position)

        if not is_in_opened_closed_lists(child, opened, closed, algorithm, root):
            child.depth = root.depth + 1
            child.parent = root
            children.append(child)
    return children


# Returns true if the state of the current node is found in open or closed lists
def is_in_opened_closed_lists(child, opened, closed, algorithm, root):

    is_known = False

    if algorithm == "DFS":
        if opened.get(child.state + str(child.depth)) != None:
            is_known = True
        if closed.get(child.state + str(child.depth)) != None:
            is_known = True

    elif algorithm == "BFS":
        if opened.get(child.state) != None:
            is_known = True
        if closed.get(child.state) != None:
            is_known = True
    else:
        if opened.get(child.state) != None:
            child.depth = root.depth + 1
            if child.get_fn() < opened.get(child.state).get_fn():
                opened.pop(child.state)
                is_known = False;       # the graph having the same state with the child will be replaced by child that has lower f(n)
            else:
                is_known = True;

        if closed.get(child.state) != None:
            is_known = True
    if is_known:
        print("\nChild " + child.state + " is a known state. Will not be traversed.\n")
    return is_known


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


def add_children_to_opened_list_then_sort(root, children, opened, algorithm):
    if len(children) == 0:
        print("\nNode " + root.state + " does not have children to explore.\n")
    else:
        for child in children:
            if algorithm == "DFS":
                opened[child.state + str(child.depth)] = child
            else:
                opened[child.state] = child
        # Sorting dictionary is not feasible; therefore, dictionary is transferred into list then sorted and transferred back to dictionary
        opened_list = []
        for node in opened.values():
            opened_list.append(node)

        if algorithm == "BFS":
            opened_list.sort(key=functools.cmp_to_key(sort_children_by_fn))
        elif algorithm == "a_star":
            opened_list.sort(key=functools.cmp_to_key(sort_children_by_heuristic))

        opened.clear()
        for node in opened_list:
            if algorithm == "DFS":
                opened[node.state + str(node.depth)] = node
            else:
                opened[node.state] = node

        print(
            "\nExploring children of "
            + root.state
            + " (depth level: "
            + str(root.depth)
            + ").\n"
        )


def sort_children_by_fn(child1, child2):
    character1 = child1.get_fn()
    character2 = child2.get_fn()
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


def process_results(closed, success, duration, ALLOCATED_TIME, algorithm):
    goal_message = "Goal state achieved."
    error_message = " "

    if duration > ALLOCATED_TIME:
        print(
            "\n"
            + algorithm
            + " ran past allocated time of "
            + str(ALLOCATED_TIME)
            + " seconds.\n"
        )
    else:
        print("\n" + algorithm + f" completed in {duration:0.4f} seconds.\n")

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
        o_dfs = {}  # open stack
        c_dfs = {}  # closed stack
        o_dfs[graph.state + str(graph.depth)] = graph

        # What is output? output[0] = search path, output[1] = solution path, output[2] = error message
        output_dfs = depth_first_search(o_dfs, c_dfs)
        generate_search_file(output_dfs[0], puzzle_count, "dfs")
        generate_solution_file(output_dfs[1], output_dfs[2], puzzle_count, "dfs")

        o_bfs = {}  # open stack
        c_bfs = {}  # closed stack
        o_bfs[graph.state] = graph

        output_bfs = best_first_search(o_bfs, c_bfs, graph.max_l)
        generate_search_file(output_bfs[0], puzzle_count, "bfs")
        generate_solution_file(output_bfs[1], output_bfs[2], puzzle_count, "bfs")

        o_a_star = {}  # open stack
        c_a_star = {}  # closed stack
        o_a_star[graph.state] = graph

        output_a_star = algorithm_a_star(o_a_star, c_a_star, graph.max_l)
        generate_search_file(output_a_star[0], puzzle_count, "a_star")
        generate_solution_file(
            output_a_star[1], output_a_star[2], puzzle_count, "a_star"
        )

        puzzle_count += 1


if __name__ == "__main__":
    main()
