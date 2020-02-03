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

        graph.dots[5].touch()
        print("-------------------")
        graph.print()

        # Touch the dot at position 5
        touched = graph.dots[5].value
        top = graph.dots[1].value
        left = graph.dots[4].value
        right = graph.dots[6].value
        bottom = graph.dots[9].value

        self.assertTrue(touched == 1)
        self.assertTrue(top == 0)
        self.assertTrue(left == 0)
        self.assertTrue(right == 1)
        self.assertTrue(bottom == 0)
