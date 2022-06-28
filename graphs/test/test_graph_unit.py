import unittest
from graph import Node, Graph, gen_random_graph, inv_friends_dummy


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

    def test_graph_gen(self):
        gr = gen_random_graph(10, 15)
        self.assertEqual(len(gr._node_names), 10)
        edg_count = 0
        for i in range(len(gr._node_names)):
            for j in range(i+1, len(gr._node_names)):
                if gr._adj_matrix[gr._node_names[i]][gr._node_names[j]]:
                    edg_count += 1
        self.assertEqual(edg_count, 15)
        self.assertRaises(Exception, gen_random_graph, 0, 15)
        self.assertRaises(Exception, gen_random_graph, 10, 150)

    def test_inv_friend(self):
        nodes_1 = [Node("a", {'val': 1}), Node("b", {'val': 2}), Node("c", {'val': 3}), Node("d", {'val': 4}),
                   Node("e", {'val': 5}), Node("f", {'val': 6})]
        connections_1 = [('a', 'c'), ('b', 'd'), ('c', 'f'), ('c', 'e'), ('c', 'd'), ('d', 'f')]
        gr = Graph(nodes_1, connections_1)
        res_friends = inv_friends_dummy(gr)
        self.assertListEqual(['a', 'b', 'e', 'f'], res_friends)
        gr.plot_graph("plots/test_gr_1.png")

        # all nodes connected with each other
        gr = gen_random_graph(5, 10)
        res_friends = inv_friends_dummy(gr)
        self.assertListEqual(['0'], res_friends)
        gr.plot_graph("plots/test_gr_2.png")

        # with 0 edges
        gr = gen_random_graph(5, 0)
        res_friends = inv_friends_dummy(gr)
        self.assertListEqual(['0', '1', '2', '3', '4'], res_friends)
        gr.plot_graph("plots/test_gr_3.png")

        # another tests
        nodes_1 = [Node("0", {'val': 1}), Node("1", {'val': 2}), Node("2", {'val': 3}), Node("3", {'val': 4}),
                   Node("4", {'val': 5}), Node("5", {'val': 6})]
        connections_1 = [('0', '2'), ('0', '3'), ('0', '4'), ('0', '5'), ('1', '2'), ('2', '4'),
                         ('3', '5'), ('4', '5')]
        gr = Graph(nodes_1, connections_1)
        res_friends = inv_friends_dummy(gr)
        self.assertListEqual(['1', '3', '4'], res_friends)
        gr.plot_graph("plots/test_gr_4.png")


if __name__ == '__main__':
    unittest.main()
