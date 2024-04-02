class Node:
    def __init__(self, node_data: dict):
        # Tree structure
        self.depth = 0
        self.parents = list()
        self.children = list()
        self.node_data = node_data

        # Node Probabilities
        self.probs_options_dict = {
            "season": self._season_probs,
            "vertex": self._vertex_probs,
            "edge": self._edge_probs,
        }
        self.probs = dict()
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
        return self.probs

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
        return self.probs

    def _edge_probs(self):
        if self.node_data["p"] == 1.0:
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
        return self.probs

    def calculate_given_probs(self):
        self.probs_options_dict[self.type()]()

    def node_values(self):
        return list(self.probs.keys())

    def probability(self, value, evidence):
        if self.type() == "season":
            # Calculate the probability
            return self.probs[value]
        elif self.type() == "vertex":
            season_node = self.parents[0]

            # Calculate the probability
            season_evidence = evidence[season_node.node_data["identifier"]]
            return self.probs[value][season_evidence]
        elif self.type() == "edge":
            from_vertex_node = self.parents[0]
            to_vertex_node = self.parents[1]

            # Calculate the probability
            from_vertex_evidence = evidence[from_vertex_node.node_data["identifier"]]
            to_vertex_evidence = evidence[to_vertex_node.node_data["identifier"]]
            return self.probs[value][from_vertex_evidence][to_vertex_evidence]
        else:
            raise ValueError("Invalid node type.")
