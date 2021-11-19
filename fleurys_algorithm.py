import random
from collections import deque


class Graph:
    def __init__(self, nodes=None):
        self.nodes = set()
        self.add_nodes(nodes)

    def add_node(self, node) -> None:
        if isinstance(node, Node):
            self.nodes.add(node)

    def add_nodes(self, nodes) -> None:
        if isinstance(nodes, (list, set, tuple)):
            self.nodes = self.nodes.union(set(nodes))

    def print_nodes(self) -> None:
        for node in list(self.nodes):
            print(f"{node.label}: {node.get_edge_names()}")

    def has_eulerian_cycle(self) -> bool:
        for node in self.nodes:
            if not node.is_even_degree():
                return False
        return True

    def has_eulerian_path(self) -> bool:
        odd_count = 0
        for node in self.nodes:
            if not node.is_even_degree():
                odd_count += 1
                if odd_count > 2:
                    return False

        if odd_count in (0, 2):
            return True
        return False

    def has_edges(self) -> bool:
        for node in self.nodes:
            if len(node.edges) > 0:
                return True
        return False

    def is_connected(self, excluded=None) -> bool:
        if excluded is None:
            excluded = set()
        for node in self.nodes:
            node.visited = False

        queue = deque()
        first = random.choice(list(self.nodes))
        queue.append(first)

        while queue:
            current_node = queue.popleft()
            current_node.visited = True
            for edge in current_node.edges:
                if edge.visited is False:
                    queue.append(edge)

        for node in self.nodes:
            if not node.visited and node not in excluded:
                return False
        return True

    def get_fleury_path(self) -> list:
        has_cycle = self.has_eulerian_cycle()
        has_path = self.has_eulerian_path()
        print(f"Has cycle: {has_cycle}")
        print(f"Has path: {has_path}")
        if not has_path and not has_cycle:
            return

        path = []

        edgeless = set()

        if has_cycle:
            current = random.choice(list(self.nodes))
        elif has_path:
            for node in random.sample(self.nodes, len(self.nodes)):
                if not node.is_even_degree():
                    current = node
                    break

        path.append(current.label)
        while len(current.edges) > 0:
            for node in current.edges:
                current.remove_edge(node)
                if len(current.edges) == 0:
                    edgeless.add(current)
                    path.append(node.label)
                    current = node
                    break
                if self.is_connected(edgeless):
                    path.append(node.label)
                    current = node
                    break
                current.add_edge(node)

        return path


class Node:
    def __init__(self, label, edges=None):
        self.label = str(label)
        self.edges = set()
        if isinstance(edges, (list, set, tuple)):
            self.edges = self.edges.union(set(edges))

    def add_edge(self, node) -> None:
        if isinstance(node, Node):
            self.edges.add(node)
            node.edges.add(self)

    def remove_edge(self, node) -> None:
        if isinstance(node, Node):
            self.edges.remove(node)
            node.edges.remove(self)

    def add_edges(self, nodes) -> None:
        if isinstance(nodes, (list, set, tuple)):
            self.edges = self.edges.union(set(nodes))
            for node in nodes:
                node.add_edge(self)

    def get_edge_names(self) -> str:
        labels = list()
        for edge in list(self.edges):
            labels.append(str(edge.label))
        if self.edges:
            return ", ".join(labels)
        else:
            return ""

    def is_even_degree(self) -> bool:
        vert_count = len(self.edges)
        if vert_count % 2 == 0:
            return True
        return False


def node_dict_to_list(nodes: dict) -> list:
    # Node labels must have keys arranged in: 0, 1, 2, ..., n-1
    if isinstance(nodes, dict):
        dict_len = len(nodes.keys())
        result = [Node(i) for i in range(dict_len)]
        for label, neighbors in nodes.items():
            for neighbor in neighbors:
                result[label].add_edge(result[neighbor])
        return result


def example_one():
    nodes = {
        0: (1, 2),
        1: (0, 2, 3, 4),
        2: (0, 1, 3, 5),
        3: (1, 2, 4, 5),
        4: (1, 3, 5),
        5: (2, 3, 4)
    }
    nodes = node_dict_to_list(nodes)

    graph = Graph(nodes)
    print("Example One")
    path = graph.get_fleury_path()
    print(r"""
      0
     / \
    1 - 2
    |\ /|
    | 3 |
    |/ \|
    4 - 5
    """)
    print(" -> ".join(path))


def example_two():
    nodes = {
        0: (1, 2),
        1: (0, 3),
        2: (0, 3),
        3: (1, 2)
    }
    nodes = node_dict_to_list(nodes)

    graph = Graph(nodes)
    print("Example Two")
    path = graph.get_fleury_path()
    print(r"""
    0 -- 1
    |    |
    2 -- 3
    """)
    print(" -> ".join(path))


def example_three():
    nodes = {
        0: (1, 2, 3, 4),
        1: (0, 2),
        2: (0, 1),
        3: (0, 5),
        4: (0, 5, 11),
        5: (3, 4, 6, 8, 9, 10),
        6: (5, 7),
        7: (6, 8),
        8: (5, 7, 9, 15),
        9: (5, 8, 10, 14, 15),
        10: (5, 9, 11, 13),
        11: (4, 10, 12),
        12: (11, 13),
        13: (10, 11, 12, 14),
        14: (9, 13),
        15: (8, 9, 16, 19),
        16: (9, 15, 17, 18),
        17: (16, 18),
        18: (16, 17, 19, 20),
        19: (15, 18, 20),
        20: (18, 19)
    }
    nodes = node_dict_to_list(nodes)

    graph = Graph(nodes)
    print("Example Three (Game Puzzle 1)")
    print("https://git.io/J16OK")
    path = graph.get_fleury_path()
    print(" -> ".join(path))


def main():
    example_one()
    print()
    example_two()
    print()
    example_three()


if __name__ == "__main__":
    main()
