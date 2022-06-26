import unittest
from graph import Node, Graph


class TestGraphFunc(unittest.TestCase):
    def test_graph_main_funcs(self):
        nodes_1 = [Node("a", {'val': 1}), Node("b", {'val': 2}), Node("c", {'val': 3}), Node("d", {'val': 4}),
                   Node("e", {'val': 5}), Node("f", {'val': 6})]
        connections_1 = [('a', 'c'), ('b', 'd'), ('c', 'f'), ('c', 'e'), ('c', 'd'), ('d', 'f')]
        gr = Graph(nodes_1, connections_1)
        gold_adj_matr = {'a': {'a': 1, 'b': 0, 'c': 1, 'd': 0, 'e': 0, 'f': 0}, 'b': {'a': 0, 'b': 1, 'c': 0, 'd': 1, 'e': 0, 'f': 0},
                         'c': {'a': 1, 'b': 0, 'c': 1, 'd': 1, 'e': 1, 'f': 1}, 'd': {'a': 0, 'b': 1, 'c': 1, 'd': 1, 'e': 0, 'f': 1},
                         'e': {'a': 0, 'b': 0, 'c': 1, 'd': 0, 'e': 1, 'f': 0}, 'f': {'a': 0, 'b': 0, 'c': 1, 'd': 1, 'e': 0, 'f': 1}}
        self.assertListEqual(['a', 'b', 'c', 'd', 'e', 'f'], gr._node_names)
        self.assertDictEqual(gold_adj_matr, gr._adj_matrix, "Adj matrix isn't equal for gr_1")
        self.assertRaises(Exception, gr.add_node, Node("a", {'val': 1}), "exception didn't raise, existed node added")

        nodes_2 = []
        connections_2 = []
        gr = Graph(nodes_2, connections_2)
        gold_adj_matr = {}
        self.assertDictEqual(gold_adj_matr, gr._adj_matrix, "Adj matrix isn't equal for gr_2")

        gr.add_node(Node("a", {'val': 1}))
        gold_adj_matr = {'a': {'a': 1}}
        self.assertDictEqual(gold_adj_matr, gr._adj_matrix, "Adj matrix isn't equal for gr_2")
        self.assertListEqual(['a'], gr._node_names)
        self.assertTrue(gr._graph['a'].info['val'] == 1)

        gr.add_node(Node("b", {'val': 2}))
        gr.add_node(Node("c", {'val': 3}))
        connections_2 = [('a', 'c'), ('a', 'b'), ('c', 'b')]
        gr.add_cons(connections_2)
        gold_adj_matr = {'a': {'a': 1, 'b': 1, 'c': 1}, 'b': {'a': 1, 'b': 1, 'c': 1}, 'c': {'a': 1, 'b': 1, 'c': 1}}
        self.assertDictEqual(gold_adj_matr, gr._adj_matrix, "Adj matrix isn't equal for new cons")

        connections_3 = [('a', 'd')]
        self.assertRaises(Exception, gr.add_cons, connections_3, "exception didn't raise, existed node added")


if __name__ == '__main__':
    unittest.main()
