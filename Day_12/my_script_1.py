from pathlib import Path
import copy
from typing import _SpecialForm

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_12" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_12" / "example_input.txt"


def get_input(filepath: Path) -> list[list[str]]:
    grid = []
    with open(filepath, "r") as f:
        for grid_line in f.readlines():
            grid.append([i.strip() for i in grid_line.split("-")])

    return grid


class Network():
    def __init__(self, grid: list[list[str]]) -> None:
        # 1. parse network
        self.network = self.parse_network(grid)

    def parse_network(self, grid: list[list[str]]) -> dict:
        network = {}
        for start_node, end_node in grid:
            # append end_node to start_node key
            if start_node in network:
                network[start_node].append(end_node)
            else:
                network[start_node] = [end_node]
            
            if end_node in network:
                network[end_node].append(start_node)
            else:
                network[end_node] = [start_node]
        
        network['end'] = []
        return network

    def print_network(self) -> None:
        for key, value in self.network.items():
            print(f"{key}: {value}")


class Tree():
    def __init__(self, network: 'Network') -> None:
        self.network = network
        # 1. init tree
        self.tree = TreeNode('start')

        # 2. recursively build tree
        self.build_tree(self.tree)

        # 3. get tree paths
        self.paths = []
        self.parse_tree_paths()

        
    def build_tree(self, node: 'TreeNode') -> None:
        # recursively build tree: visit lowercase nodes only once
        for neighbor_node in self.network.network[node.name]:
            if neighbor_node not in node.get_parent_nodes_lowercase():
                node.add_leaf(neighbor_node)
                self.build_tree(node.leafs[-1])
    
    def parse_tree_paths(self) -> None:
        self._parse_tree_paths(self.tree)
    
    def _parse_tree_paths(self, node: 'TreeNode') -> None:
        if node.leafs:
            for leaf in node.leafs:
                self._parse_tree_paths(leaf)
        elif node.name == 'end':
            self.paths.append([node.name] + node.get_parent_nodes())
    
    def print_tree_paths(self) -> None:
        self._print_tree_paths(self.tree)

    def _print_tree_paths(self, node: 'TreeNode') -> None:
        if node.leafs:
            for leaf in node.leafs:
                self._print_tree_paths(leaf)
        elif node.name == 'end':
            print([node.name] + node.get_parent_nodes())
    
    def __repr__(self) -> str:
        return self.tree.__repr__()

class TreeNode():
    def __init__(self, name: str, parent: 'TreeNode' = None) -> None:
        self.name   = name
        self.parent = parent  # subnode?
        self.leafs  = []      # list of node
    
    def add_leaf(self, name: str) -> None:
        self.leafs.append(TreeNode(name, parent=self))
    
    def get_parent_nodes(self) -> list[str]:
        parent_nodes = []
        node = self
        while node.parent is not None:
            parent_nodes.append(node.parent.name)
            node = node.parent
        return parent_nodes
    
    def get_parent_nodes_lowercase(self) -> list[str]:
        parent_nodes = []
        node = self
        while node.parent is not None:
            if(node.parent.name.islower()):
                parent_nodes.append(node.parent.name)
            node = node.parent
        return parent_nodes
    
    def __repr__(self) -> str:
        return f"{self.name} -> {self.leafs}"


        
def part_1(grid: list[list[int]]) -> int:
    # 1. parse network
    network = Network(grid)
    # network.print_network()

    # 2. build tree from network
    tree = Tree(network)
        
    # 3. find all paths
    # tree.print_tree_paths()
    return len(tree.paths)


if __name__ == '__main__':
    # horizontal position of each crab
    # -> make all of their horizontal positions match while requiring them to spend as little fuel as possible
    print(INPUT_FILE)

    # parse input 
    example_grid = get_input(EXAMPLE_INPUT_FILE)
    print(example_grid)

    grid = get_input(INPUT_FILE)
    print(len(grid))

    # Part 1
    print(part_1(example_grid)) 
    print(part_1(grid))
    