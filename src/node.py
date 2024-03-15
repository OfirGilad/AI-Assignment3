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

    def _vertex_probabs(self):
        season_node = self.parents[0]
        self.probabs = {
            "package": {
                "low": self.node_data["p"] * season_node.probabs["low"],
                "medium": self.node_data["p"] * season_node.probabs["medium"],
                "high": self.node_data["p"] * season_node.probabs["high"]
            },
            "no package": {
                "low": self.node_data["q"] * season_node.probabs["low"],
                "medium": self.node_data["q"] * season_node.probabs["medium"],
                "high": self.node_data["q"] * season_node.probabs["high"]
            }
        }

    def _edge_probabs(self):
        v0 = self.parents[0]
        v1 = self.parents[1]
        self.probabs = {
            "blocked": {
                "package": {
                    "package": {
                        "low": self.node_data["p"] * (v0.probabs["package"]["low"] + v1.probabs["package"]["low"]),
                        "medium": self.node_data["p"] * (v0.probabs["package"]["medium"] + v1.probabs["package"]["medium"]),
                        "high": self.node_data["p"] * (v0.probabs["package"]["high"] + v1.probabs["package"]["high"]),
                    },
                    "no package": {
                        "low": self.node_data["p"] * (v0.probabs["package"]["low"] + v1.probabs["no package"]["low"]),
                        "medium": self.node_data["p"] * (v0.probabs["package"]["medium"] + v1.probabs["no package"]["medium"]),
                        "high": self.node_data["p"] * (v0.probabs["package"]["high"] + v1.probabs["no package"]["high"]),
                    }
                },
                "no package": {
                    "package": {
                        "low": self.node_data["p"] * (v0.probabs["no package"]["low"] + v1.probabs["package"]["low"]),
                        "medium": self.node_data["p"] * (v0.probabs["no package"]["medium"] + v1.probabs["package"]["medium"]),
                        "high": self.node_data["p"] * (v0.probabs["no package"]["high"] + v1.probabs["package"]["high"]),
                    },
                    "no package": {
                        "low": self.node_data["p"] * (v0.probabs["no package"]["low"] + v1.probabs["no package"]["low"]),
                        "medium": self.node_data["p"] * (v0.probabs["no package"]["medium"] + v1.probabs["no package"]["medium"]),
                        "high": self.node_data["p"] * (v0.probabs["no package"]["high"] + v1.probabs["no package"]["high"]),
                    }
                }
            },
            "unblocked": {
                "package": {
                    "package": {
                        "low": self.node_data["q"] * (v0.probabs["package"]["low"] + v1.probabs["package"]["low"]),
                        "medium": self.node_data["q"] * (v0.probabs["package"]["medium"] + v1.probabs["package"]["medium"]),
                        "high": self.node_data["q"] * (v0.probabs["package"]["high"] + v1.probabs["package"]["high"]),
                    },
                    "no package": {
                        "low": self.node_data["q"] * (v0.probabs["package"]["low"] + v1.probabs["no package"]["low"]),
                        "medium": self.node_data["q"] * (v0.probabs["package"]["medium"] + v1.probabs["no package"]["medium"]),
                        "high": self.node_data["q"] * (v0.probabs["package"]["high"] + v1.probabs["no package"]["high"]),
                    }
                },
                "no package": {
                    "package": {
                        "low": self.node_data["q"] * (v0.probabs["no package"]["low"] + v1.probabs["package"]["low"]),
                        "medium": self.node_data["q"] * (v0.probabs["no package"]["medium"] + v1.probabs["package"]["medium"]),
                        "high": self.node_data["q"] * (v0.probabs["no package"]["high"] + v1.probabs["package"]["high"]),
                    },
                    "no package": {
                        "low": self.node_data["q"] * (v0.probabs["no package"]["low"] + v1.probabs["no package"]["low"]),
                        "medium": self.node_data["q"] * (v0.probabs["no package"]["medium"] + v1.probabs["no package"]["medium"]),
                        "high": self.node_data["q"] * (v0.probabs["no package"]["high"] + v1.probabs["no package"]["high"]),
                    }
                }
            },
        }

    def calculate_probs(self):
        self.options_dict[self.type()]()
        return self.probabs
