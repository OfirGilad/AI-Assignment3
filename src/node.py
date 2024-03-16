class Node:
    def __init__(self, node_data: dict):
        # Tree structure
        self.depth = 0
        self.parents = list()
        self.children = list()
        self.node_data = node_data

        self.options_dict = {
            "season": self._season_probabs,
            "vertex": self._vertex_probabs,
            "edge": self._edge_probabs,
        }
        self.probabs = dict()
        self.infers = dict()

    def type(self):
        return self.node_data["type"]

    def sub_type(self):
        return self.node_data.get("sub_type", None)

    def add_parent(self, parent_node):
        self.parents.append(parent_node)

    def add_child(self, child_node):
        self.children.append(child_node)

    def network_tree_str(self, level=1):
        network_structure = "|" + "--" * level + f" Node Info: {self.node_data}\n"
        for child in self.children:
            if child.sub_type() == "dummy":
                continue
            network_structure += child.network_tree_str(level + 1)
        return network_structure

    def _season_probabs(self):
        self.probabs = {
            "low": self.node_data["low"],
            "medium": self.node_data["medium"],
            "high": self.node_data["high"]
        }
        self.infers = self.probabs

    def _vertex_probabs(self):
        season_node = self.parents[0]

        self.probabs["package"] = {
            "low": self.node_data["p"],
            "medium":  min(2.0 * self.node_data["p"], 1.0),
            "high": min(3.0 * self.node_data["p"], 1.0)
        }
        self.probabs["no package"] = {
            "low": self.node_data["q"],
            "medium": 1 - self.probabs["package"]["medium"],
            "high": 1 - self.probabs["package"]["high"]
        }

        self.infers["package"] = (
            (self.probabs["package"]["low"] * season_node.infers["low"]) +
            (self.probabs["package"]["medium"] * season_node.infers["medium"]) +
            (self.probabs["package"]["high"] * season_node.infers["high"])
        )
        self.infers["no package"] = 1 - self.infers["package"]

    def _edge_probabs(self):
        v0 = self.parents[0]
        v1 = self.parents[1]

        # TODO: Calculate the probabilities (need to find the problem)
        self.probabs["blocked"] = {
            "package": {
                "package": 1 - (self.node_data["q"] * v0.infers["no package"] * v1.infers["no package"]),
                "no package": 1 - (self.node_data["q"] * v0.infers["no package"] * v1.infers["package"])
            },
            "no package": {
                "package": 1 - (self.node_data["p"] * v0.infers["package"] * v1.infers["no package"]),
                "no package": 1 - (self.node_data["p"] * v0.infers["package"] * v1.infers["package"]),
            }
        }
        self.probabs["unblocked"] = {
            "package": {
                "package": 1 - self.probabs["blocked"]["package"]["package"],
                "no package": 1 - self.probabs["blocked"]["package"]["no package"]
            },
            "no package": {
                "package": 1 - self.probabs["blocked"]["no package"]["package"],
                "no package": 1 - self.probabs["blocked"]["no package"]["no package"]
            }
        }

        # TODO: Calculate the inferences
        self.infers["blocked"] = {}


    def calculate_node_probabs(self):
        self.options_dict[self.type()]()
