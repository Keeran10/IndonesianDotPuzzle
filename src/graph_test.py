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
        print(graph.dots)
        print()
        graph.print()
        self.assertTrue(graph is not None)

        to_be_touched = graph.dots.get("B2").value
        top = graph.dots.get("A2").value
        left = graph.dots.get("B1").value
        right = graph.dots.get("B3").value
        bottom = graph.dots.get("C2").value

        # verify initial values of target dot and its adjacents
        self.assertTrue(to_be_touched == 0)
        self.assertTrue(top == 1)
        self.assertTrue(left == 1)
        self.assertTrue(right == 0)
        self.assertTrue(bottom == 1)

        # Touch the dot at position 5
        graph.dots.get("B2").touch()

        graph.print()

        touched = graph.dots.get("B2").value
        top = graph.dots.get("A2").value
        left = graph.dots.get("B1").value
        right = graph.dots.get("B3").value
        bottom = graph.dots.get("C2").value

        # verify flipped values of target dot and its adjacents
        self.assertTrue(touched == 1)
        self.assertTrue(top == 0)
        self.assertTrue(left == 0)
        self.assertTrue(right == 1)
        self.assertTrue(bottom == 0)
