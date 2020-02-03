class Dot:
    def __init__(self, value, position):
        self.value = int(value)
        self.position = position
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
        self.dots = self.processDotValues(values)  # list of all ordered dots

    def processDotValues(self, values):
        # transform dots values into dot objects

        dots = list()
        row = 65
        column = 1

        for value in values:

            position = chr(row) + str(column)
            dot = Dot(value, position)
            dots.append(dot)

            index = len(dots) - 1
            adjacent_top = index - self.n
            adjacent_left = index - 1

            if row == 65:
                # first row doesn't have top adjacent

                if column % self.n != 1:
                    # first row, first column doesn't have top or left adjacents
                    dot.add_adjacent(dots[adjacent_left])

            elif column % self.n == 1:
                # first columns don't have left adjacent
                dot.add_adjacent(dots[adjacent_top])

            else:
                dot.add_adjacent(dots[adjacent_top])
                dot.add_adjacent(dots[adjacent_left])

            column += 1

            if column % self.n == 0:
                row += 1

        return dots

    def print(self):

        format_counter = 0
        header_counter = 1

        print()

        # top-left corner left blank
        print(" ", end=" ")

        while header_counter <= self.n:
            print(header_counter, end=" ")
            header_counter += 1

        for dot in self.dots:

            if format_counter % self.n == 0:
                print()
                print(dot.position[0], end=" ")
                print(dot.value, end=" ")
                format_counter += 1
                continue

            print(dot.value, end=" ")
            format_counter += 1

        print()

