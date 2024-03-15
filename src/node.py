class Node:
    def __init__(self, node_data: dict):
        # Tree structure
        self.depth = 0
        self.parent = list()
        self.children = list()
        self.node_data = node_data

    def type(self):
        return self.node_data["type"]

    def sub_type(self):
        return self.node_data.get("sub_type", None)

    def add_parent(self, parent_node):
        self.parent.append(parent_node)

    def add_child(self, child_node):
        self.children.append(child_node)

    def network_tree_str(self, level=1):
        network_structure = "|" + "--" * level + f" Node Info: {self.node_data}\n"
        for child in self.children:
            network_structure += child.network_tree_str(level + 1)
        return network_structure
