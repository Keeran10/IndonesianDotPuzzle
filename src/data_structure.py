class Dot:
    def __init__(self, value, position, index):
        self.value = int(value)
        self.position = position
        self.index = index
        self.adjacents = list()

    def add_adjacent(self, adjacent):
        # accounts for bi-directionality between dots
        if adjacent not in self.adjacents:
            self.adjacents.append(adjacent)

        if self not in adjacent.adjacents:
            adjacent.add_adjacent(self)

    def touch(self):
        self.flip()
        for adjacent in self.adjacents:
            adjacent.flip()

    def flip(self):
        if self.value == 0:
            self.value = 1
        else:
            self.value = 0


class Graph:
    def __init__(self, n, max_d, max_l, values):
        self.n = int(n)  # the size of the graph
        self.max_d = int(max_d)  # the maximum depth search for DFS
        self.max_l = int(max_l)  # the maximum search path length for BFS and A*
        self.dots = self.process_dot_values(values)  # list of all ordered dots
        self.touched = "0"
        self.depth = 1
        self.state = values

    def process_dot_values(self, values):
        # transform dots values into dot objects

        dots = list()
        row = 65
        column = 1
        count = 0

        for value in values:

            position = chr(row) + str(column)
            dot = Dot(value, position, count)
            dots.append(dot)

            # only top-left need consideration because add_adjacent
            # bi-directionality will handle the bottom-right edges
            index = len(dots) - 1
            adjacent_top = index - self.n
            adjacent_left = index - 1

            if row == 65:
                # first row doesn't have top adjacent

                if column != 1:
                    # first row, first column doesn't have top or left adjacents
                    dot.add_adjacent(dots[adjacent_left])

            elif column == 1:
                # first columns don't have left adjacent
                dot.add_adjacent(dots[adjacent_top])

            else:
                dot.add_adjacent(dots[adjacent_top])
                dot.add_adjacent(dots[adjacent_left])

            column += 1
            count += 1

            if column > self.n:
                column = 1
                row += 1

        dot_dictionary = {}

        for dot in dots:
            dot_dictionary[dot.position] = dot

        return dot_dictionary

    def touch(self, position):
        self.dots.get(position).touch()
        self.touched = position
        self.set_state()

    def set_state(self):
        self.state = ""
        for key in self.dots:
            self.state += str(self.dots.get(key).value)

    def is_goal_state(self):
        goal_state = "0" * (self.n * self.n)
        return True if self.state == goal_state else False

    def print(self):

        format_counter = 0
        header_counter = 1
        print("\n")

        # top-left corner left blank
        print(" ", end=" ")

        while header_counter <= self.n:
            print(header_counter, end=" ")
            header_counter += 1

        for key in self.dots:
            dot = self.dots.get(key)
            if format_counter % self.n == 0:
                print()
                print(dot.position[0], end=" ")
                print(dot.value, end=" ")
                format_counter += 1
                continue

            print(dot.value, end=" ")
            format_counter += 1

        print("\n")

    @classmethod
    def create_graphs(cls, file_path):
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


# custom object pair used to generate lines in solution.txt
class Pair:
    def __init__(self, touched, state):
        self.touched = touched
        self.state = state
