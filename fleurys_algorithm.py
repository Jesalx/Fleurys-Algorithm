import random
from collections import deque


class Graph:
    def __init__(self, nodes=None):
        self.nodes = set()
        if nodes is set or nodes is list:
            self.nodes = self.nodes.union(set(nodes))

    def add_node(self, node) -> None:
        self.nodes.add(node)

    def add_nodes(self, nodes) -> None:
        nodes = set(nodes)
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
        self.label = label
        self.edges = set()
        if edges is set or edges is list:
            self.edges = self.edges.union(set(edges))

    def add_edge(self, node) -> None:
        self.edges.add(node)
        node.edges.add(self)

    def remove_edge(self, node) -> None:
        self.edges.remove(node)
        node.edges.remove(self)

    def add_edges(self, nodes) -> None:
        self.edges = self.edges.union(set(nodes))
        for node in nodes:
            node.add_edge(self)

    def get_edge_names(self) -> str:
        labels = list()
        for edge in list(self.edges):
            labels.append(edge.label)
        if self.edges:
            return ", ".join(labels)
        else:
            return ""

    def is_even_degree(self) -> bool:
        vert_count = len(self.edges)
        if vert_count % 2 == 0:
            return True
        return False


def example_one():
    graph = Graph()
    nodes = [Node('0'), Node('1'), Node('2'), Node('3'), Node('4'), Node('5')]

    nodes[0].add_edges({nodes[1], nodes[2]})
    nodes[1].add_edges({nodes[0], nodes[2], nodes[3], nodes[4]})
    nodes[2].add_edges({nodes[0], nodes[1], nodes[3], nodes[5]})
    nodes[3].add_edges({nodes[1], nodes[2], nodes[4], nodes[5]})
    nodes[4].add_edges({nodes[1], nodes[3], nodes[5]})
    nodes[5].add_edges({nodes[2], nodes[3], nodes[4]})

    graph.add_nodes(nodes)
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
    graph = Graph()
    nodes = [Node('0'), Node('1'), Node('2'), Node('3')]
    nodes[0].add_edges({nodes[1], nodes[2]})
    nodes[1].add_edges({nodes[0], nodes[3]})
    nodes[2].add_edges({nodes[0], nodes[3]})
    nodes[3].add_edges({nodes[1], nodes[2]})
    graph.add_nodes(nodes)
    print("Example Two")
    path = graph.get_fleury_path()
    print(r"""
    0 -- 1
    |    |
    2 -- 3
    """)
    print(" -> ".join(path))


def example_three():
    graph = Graph()
    nodes = [Node(str(i)) for i in range(21)]
    nodes[0].add_edges({nodes[1], nodes[2], nodes[3], nodes[4]})
    nodes[1].add_edges({nodes[0], nodes[2]})
    nodes[2].add_edges({nodes[0], nodes[1]})
    nodes[3].add_edges({nodes[0], nodes[5]})
    nodes[4].add_edges({nodes[0], nodes[5], nodes[11]})
    nodes[5].add_edges({nodes[3], nodes[6], nodes[4],
                       nodes[8], nodes[9], nodes[10]})
    nodes[6].add_edges({nodes[5], nodes[7]})
    nodes[7].add_edges({nodes[6], nodes[8]})
    nodes[8].add_edges({nodes[5], nodes[7], nodes[9], nodes[15]})
    nodes[9].add_edges({nodes[5], nodes[8], nodes[10], nodes[14], nodes[15]})
    nodes[10].add_edges({nodes[5], nodes[9], nodes[11], nodes[13]})
    nodes[11].add_edges({nodes[4], nodes[10], nodes[12]})
    nodes[12].add_edges({nodes[11], nodes[13]})
    nodes[13].add_edges({nodes[10], nodes[11], nodes[12], nodes[14]})
    nodes[14].add_edges({nodes[9], nodes[13]})
    nodes[15].add_edges({nodes[8], nodes[9], nodes[16], nodes[19]})
    nodes[16].add_edges({nodes[9], nodes[15], nodes[17], nodes[18]})
    nodes[17].add_edges({nodes[16], nodes[18]})
    nodes[18].add_edges({nodes[16], nodes[17], nodes[19], nodes[20]})
    nodes[19].add_edges({nodes[15], nodes[18], nodes[20]})
    nodes[20].add_edges({nodes[18], nodes[19]})
    graph.add_nodes(nodes)
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
