import os.path
from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
from optparse import OptionParser


class Node:
    def __init__(self, node_name: str, info: dict):
        self.name = node_name
        self.info = info

    def __str__(self):
        return f"{self.name}: {str(self.info)}"

    def update_info(self, new_info):
        self.info.update(new_info)


class Graph:
    def __init__(self, nodes: List[Node] = [], connections: List[Tuple[str, str]] = []):
        self._graph = {}
        self._adj_matrix = {}
        # add nodes
        for node in nodes:
            assert node.name not in self._graph.keys(), f"Node with name: {node.name} is already exists"
            self._graph[node.name] = node
        self._node_names = list(self._graph.keys())

        # init adj matrix
        node_names = list(self._graph.keys())
        for i in range(len(node_names)):
            self._adj_matrix[node_names[i]] = {}
            for j in range(len(node_names)):
                val = 0
                if i == j:
                    val = 1
                self._adj_matrix[node_names[i]][node_names[j]] = val

        # add connections
        self._update_cons(connections)

    def _update_cons(self, cons):
        for con in cons:
            assert con[0] in self._node_names and con[1] in self._node_names, f"{con[0]} or {con[1]} not in node names"
            self._adj_matrix[con[0]][con[1]] = 1
            self._adj_matrix[con[1]][con[0]] = 1

    def add_node(self, node: Node, node_cons: List[Tuple[str, str]] = []):

        assert node.name not in self._graph.keys(), f"Node with name: {node.name} is already exists"
        self._node_names.append(node.name)
        self._graph[node.name] = node

        self._adj_matrix[node.name] = {}
        for exist_name in self._graph.keys():
            self._adj_matrix[exist_name][node.name] = 0
            self._adj_matrix[node.name][exist_name] = 0
        self._adj_matrix[node.name][node.name] = 1

        self._update_cons(node_cons)

    def add_cons(self, new_cons: List[Tuple[str, str]]):
        self._update_cons(new_cons)

    def plot_graph(self, file_name='plots/graph.png'):
        pl_graph = nx.Graph()
        for i in range(len(self._node_names)):
            pl_graph.add_node(self._node_names[i])
            for j in range(i+1, len(self._node_names)):
                if self._adj_matrix[self._node_names[i]][self._node_names[j]]:
                    pl_graph.add_edge(self._node_names[i], self._node_names[j])
        nx.draw_networkx(pl_graph, with_labels=True, node_size=200)
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        if not os.path.exists(os.path.dirname(img_path)):
            os.mkdir(os.path.dirname(img_path))
        plt.savefig(img_path)
        plt.clf()

    @property
    def node_names(self):
        return self._node_names

    @property
    def adj_matrix(self):
        return self._adj_matrix


def gen_random_graph(num_nodes: int, num_edges: int) -> Graph:
    max_edges = num_nodes*(num_nodes-1)//2
    assert num_edges <= max_edges, f"num edges: {num_edges} more than max_edges: {max_edges}"

    node_list = [Node(str(i), {'val': 0}) for i in range(num_nodes)]

    # randomly select edges
    adj_matr_half = [0]*max_edges
    rand_pos = np.random.choice(list(range(max_edges)), size=num_edges, replace=False)
    for i in rand_pos:
        adj_matr_half[i] = 1

    # create connections
    adj_matr_ind = 0
    con_list = []
    for i in range(num_nodes - 1):
        for j in range(i+1, num_nodes):
            if adj_matr_half[adj_matr_ind]:
                con_list.append((node_list[i].name, node_list[j].name))
            adj_matr_ind += 1

    gr = Graph(node_list, con_list)
    return gr


def inv_friends_dummy(gr: Graph):
    def isDiagMatrix(matr):
        if np.sum(matr) == matr.shape[0]:
            return True
        else:
            return False

    node_names = gr.node_names
    adj_matr = np.zeros((len(node_names), len(node_names)), dtype=int)
    np.fill_diagonal(adj_matr, 1)

    for i in range(len(node_names)):
        for j in range(i + 1, len(node_names)):
            if gr.adj_matrix[node_names[i]][node_names[j]]:
                adj_matr[i][j], adj_matr[j][i] = 1, 1

    comb_degree = len(node_names)
    names_idxs = list(range(len(node_names)))
    final_comb = []
    while comb_degree != 1 and not final_comb:
        combs = combinations(names_idxs, comb_degree)
        for comb in combs:
            if isDiagMatrix(adj_matr[np.ix_(comb, comb)]):
                final_comb = comb
                break
        comb_degree -= 1

    final_friend_names = [node_names[i] for i in final_comb]
    if not final_comb:
        print(f"You can select an arbitary 1 friend: {node_names}")
        final_friend_names = ['0']
    else:
        print(f"Maximum you can invite: {comb_degree + 1} friends: {final_friend_names}")
    return final_friend_names


if __name__ == "__main__":
    """
    Generates random graph and solve task
    """

    parser = OptionParser()
    parser.add_option("--num_nodes", dest="num_nodes", type=int, default=5)
    parser.add_option("--num_edges", dest="num_edges", type=int, default=7)
    (options, args) = parser.parse_args()

    gr = gen_random_graph(options.num_nodes, options.num_edges)
    inv_friends_dummy(gr)
    gr.plot_graph()
