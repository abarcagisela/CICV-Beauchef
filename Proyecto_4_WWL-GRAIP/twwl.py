import numpy as np
from collections import deque

class Node:
    def __init__(self, node_hash, depth, n_graphs):
        self.hash = node_hash
        self.depth = depth
        self.gamma = np.zeros(n_graphs)
        self.children = {}

class TWWL:
    def __init__(self, H):
        self.H = H
        self.root = None
        self.n_graphs = 0

    def fit(self, graphs, label_symb='label', measure_symb='measure'):
        self.n_graphs = len(graphs)
        self.root = Node(hash(None), -1, self.n_graphs)
        queue = deque()

        for i, G in enumerate(graphs):
            for u in G.nodes():
                l_val = G.nodes[u].get(label_symb, "dummy")
                l_hash = hash(l_val)
                if l_hash not in self.root.children:
                    self.root.children[l_hash] = (0.5, Node(l_hash, 0, self.n_graphs))
                child_node = self.root.children[l_hash][1]
                queue.append((child_node, i, u))

        while queue:
            node, g_idx, u_idx = queue.popleft()
            G = graphs[g_idx]
            masa = G.nodes[u_idx].get(measure_symb, 1.0 / len(G))
            node.gamma[g_idx] += masa
            if node.depth >= self.H: continue
            neighbors_labels = sorted([hash(G.nodes[v].get(label_symb, "dummy")) for v in G.neighbors(u_idx)])
            nxt_hash = hash((node.hash, tuple(neighbors_labels)))
            if nxt_hash not in node.children:
                node.children[nxt_hash] = (0.5, Node(nxt_hash, node.depth + 1, self.n_graphs))
            queue.append((node.children[nxt_hash][1], g_idx, u_idx))

    def compute_distance_matrix(self):
        dist_matrix = np.zeros((self.n_graphs, self.n_graphs))
        def _traverse(curr_node):
            nonlocal dist_matrix
            for weight, child in curr_node.children.values():
                _traverse(child)
                diff = np.abs(child.gamma[:, np.newaxis] - child.gamma[np.newaxis, :])
                dist_matrix += diff * weight
        _traverse(self.root)
        return dist_matrix

        