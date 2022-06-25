import os.path
from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, node_name: str, info: dict):
        self.name = node_name
        self.info = info

    def __str__(self):
        return f"{self.name}: {str(self.info)}"

    def update_info(self, new_info):
        self.info.update(new_info)


class Graph:
    def __init__(self, nodes: List[Node], connections: List[Tuple[str, str]]):
        self._graph = {}
        self._adj_matrix = {}
        # add nodes
        for node in nodes:
            assert node.name not in self._graph.keys(), f"Node with name: {node.name} is already exists"
            self._graph[node.name] = Node
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

    def add_node(self, node: Node, node_cons: List[Tuple[str, str]]):

        assert node.name not in self._graph.keys(), f"Node with name: {node.name} is already exists"
        self._node_names.append(node.name)

        self._adj_matrix[node.name] = {}
        for exist_name in self._graph.keys():
            self._adj_matrix[exist_name][node.name] = 0
            self._adj_matrix[node.name][exist_name] = 0
        self._adj_matrix[node.name][node.name] = 1

        self._update_cons(node_cons)

    def add_cons(self, new_cons: List[Tuple[str, str]]):
        self._update_cons(new_cons)

    def plot_graph(self):
        pl_graph = nx.Graph()
        for i in range(len(self._node_names)):
            for j in range(i+1, len(self._node_names)):
                if self._adj_matrix[self._node_names[i]][self._node_names[j]]:
                    pl_graph.add_edge(self._node_names[i], self._node_names[j])
        nx.draw_networkx(pl_graph, with_labels=True, node_size=800)
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plots/graph.png')
        plt.savefig(img_path)


if __name__ == "__main__":
    nodes_1 = [Node("a", {'val': 1}), Node("b", {'val': 2}), Node("c", {'val': 3}), Node("d", {'val': 4}),
             Node("e", {'val': 5}), Node("f", {'val': 6})]
    connections_1 = [('a', 'c'), ('b', 'd'), ('c', 'f'), ('c', 'e'), ('c', 'd'), ('d', 'f')]
    gr = Graph(nodes_1, connections_1)
    gr.plot_graph()
