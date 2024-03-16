class Node:
    def __init__(self, node_data: dict):
        # Tree structure
        self.depth = 0
        self.parents = list()
        self.children = list()
        self.node_data = node_data

        self.options_dict = {
            "season": self._season_probs,
            "vertex": self._vertex_probs,
            "edge": self._edge_probs,
        }
        self.probs = dict()
        self.infers = dict()

        self.calculate_given_probs()

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

    def _season_probs(self):
        self.probs = {
            "low": self.node_data["low"],
            "medium": self.node_data["medium"],
            "high": self.node_data["high"]
        }

        # self.infers = self.probs

    def _vertex_probs(self):
        self.probs["package"] = {
            "low": self.node_data["p"],
            "medium":  min(2.0 * self.node_data["p"], 1.0),
            "high": min(3.0 * self.node_data["p"], 1.0)
        }
        self.probs["no package"] = {
            "low": self.node_data["q"],
            "medium": 1 - self.probs["package"]["medium"],
            "high": 1 - self.probs["package"]["high"]
        }

        # season_node = self.parents[0]
        # self.infers["package"] = (
        #     (self.probs["package"]["low"] * season_node.infers["low"]) +
        #     (self.probs["package"]["medium"] * season_node.infers["medium"]) +
        #     (self.probs["package"]["high"] * season_node.infers["high"])
        # )
        # self.infers["no package"] = 1 - self.infers["package"]

    def _edge_probs(self):
        if self.sub_type() == "always blocked":
            leakage_value = 1.0
        else:
            leakage_value = self.node_data["leakage_probability"]

        self.probs["blocked"] = {
            "package": {
                "package": 1 - (self.node_data["q"] * self.node_data["q"]),
                "no package": 1 - self.node_data["q"]
            },
            "no package": {
                "package": 1 - self.node_data["q"],
                "no package": leakage_value,
            }
        }
        self.probs["unblocked"] = {
            "package": {
                "package": 1 - self.probs["blocked"]["package"]["package"],
                "no package": 1 - self.probs["blocked"]["package"]["no package"]
            },
            "no package": {
                "package": 1 - self.probs["blocked"]["no package"]["package"],
                "no package": 1 - self.probs["blocked"]["no package"]["no package"]
            }
        }

    def calculate_given_probs(self):
        self.options_dict[self.type()]()
