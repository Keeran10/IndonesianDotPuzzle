import os, sys
import unittest
from graph import Graph


class GraphTest(unittest.TestCase):
    def test_graph_functionality(self):
        with open(os.path.join(sys.path[0], "test_sample.txt"), "r") as f:
            for line in f:
                data = line.split()
                n = data[0]
                max_d = data[1]
                max_l = data[2]
                values = data[3]

                graph = Graph(n, max_d, max_l, values)

        print()
        graph.print()
        self.assertTrue(graph is not None)

        to_be_touched = graph.dots[5].value
        top = graph.dots[1].value
        left = graph.dots[4].value
        right = graph.dots[6].value
        bottom = graph.dots[9].value

        # verify initial values of target dot and its adjacents
        self.assertTrue(to_be_touched == 0)
        self.assertTrue(top == 1)
        self.assertTrue(left == 1)
        self.assertTrue(right == 0)
        self.assertTrue(bottom == 1)

        # Touch the dot at position 5
        graph.dots[5].touch()

        graph.print()

        touched = graph.dots[5].value
        top = graph.dots[1].value
        left = graph.dots[4].value
        right = graph.dots[6].value
        bottom = graph.dots[9].value

        # verify flipped values of target dot and its adjacents
        self.assertTrue(touched == 1)
        self.assertTrue(top == 0)
        self.assertTrue(left == 0)
        self.assertTrue(right == 1)
        self.assertTrue(bottom == 0)
