from copy import deepcopy
import itertools
from tqdm import tqdm

from node import Node


class BayesNetwork:
    def __init__(self, environment_data: dict):
        # Parse state initial parameters
        self.X = environment_data["x"] + 1
        self.Y = environment_data["y"] + 1
        self.special_edges = environment_data.get("special_edges", list())
        self.special_vertices = environment_data.get("special_vertices", list())
        self.leakage_probability = environment_data.get("leakage_probability", 0.0)
        self.season = environment_data.get("season", dict())

        # Build bayes network
        self.ordered_variables = list()
        self.season_node = None
        self.vertex_nodes = None
        self.edge_nodes = None

        self.network_nodes = dict()
        self.evidence_dict = dict()
        self._build_network()

    def _build_network(self):
        self.season_node = Node(node_data=self.season)

        # Build evidence dict / ordered variables
        season_id = self.season_node.node_data["identifier"]
        self.ordered_variables.append(season_id)
        self.evidence_dict[season_id] = None

        self.vertex_nodes = list()

        # Add dummy vertices to the network
        all_vertices = list(list(vertex) for vertex in itertools.product(range(self.X), range(self.Y)))
        packages_vertices = [vertex["at"] for vertex in self.special_vertices]
        dummy_vertices = [vertex for vertex in all_vertices if vertex not in packages_vertices]
        for vertex_coords in dummy_vertices:
            dummy_vertex_data = {
                "type": "vertex",
                "sub_type": "dummy",
                "at": vertex_coords,
                "p": 0.0,
                "q": 1.0,
                "identifier": f"({vertex_coords[0]},{vertex_coords[1]})"
            }
            dummy_vertex_node = Node(node_data=dummy_vertex_data)
            self.vertex_nodes.append(dummy_vertex_node)

            # Add connections between vertices and season node
            dummy_vertex_node.add_parent(self.season_node)
            self.season_node.add_child(dummy_vertex_node)

            # Build evidence dict / ordered variables
            vertex_id = dummy_vertex_node.node_data["identifier"]
            self.ordered_variables.append(vertex_id)

        # Add vertices to the network
        for vertex_data in self.special_vertices:
            vertex_node = Node(node_data=vertex_data)
            self.vertex_nodes.append(vertex_node)

            # Add connections between vertices and season node
            vertex_node.add_parent(self.season_node)
            self.season_node.add_child(vertex_node)

            # Build evidence dict / ordered variables
            vertex_id = vertex_node.node_data["identifier"]
            self.ordered_variables.append(vertex_id)
            self.evidence_dict[vertex_id] = None

        self.edge_nodes = list()

        # Add edges to the network
        for edge_data in self.special_edges:
            edge_data["leakage_probability"] = self.leakage_probability
            edge_node = Node(node_data=edge_data)
            self.edge_nodes.append(edge_node)

            # Add connections between edges and vertices
            for vertex_node in self.vertex_nodes:
                if edge_node.node_data["from"] == vertex_node.node_data["at"]:
                    vertex_node.add_child(edge_node)
                    edge_node.add_parent(vertex_node)
                elif edge_node.node_data["to"] == vertex_node.node_data["at"]:
                    vertex_node.add_child(edge_node)
                    edge_node.add_parent(vertex_node)
                else:
                    continue

            # Build evidence dict / ordered variables
            edge_id = edge_node.node_data["identifier"]
            self.ordered_variables.append(edge_id)
            self.evidence_dict[edge_id] = None

        self.network_nodes["season"] = self.season_node
        for vertex_node in self.vertex_nodes:
            self.network_nodes[vertex_node.node_data["identifier"]] = vertex_node
        for edge_node in self.edge_nodes:
            self.network_nodes[edge_node.node_data["identifier"]] = edge_node

        # TODO: Remove this print before submission
        # print("Network Nodes Structure:")
        # print(season_node.network_tree_str())

    def _update_nodes_given_probs(self):
        # Set evidence to season node
        season_node = self.season_node
        season_id = season_node.node_data["identifier"]
        evidence = self.evidence_dict[season_id]
        if evidence is not None:
            season_node.node_data["low"] = 1.0 if evidence == "low" else 0.0
            season_node.node_data["medium"] = 1.0 if evidence == "medium" else 0.0
            season_node.node_data["high"] = 1.0 if evidence == "high" else 0.0
            season_node.calculate_given_probs()

        # Set evidence to vertex node
        for vertex_node in self.vertex_nodes:
            if vertex_node.sub_type() == "dummy":
                continue

            vertex_id = vertex_node.node_data["identifier"]
            evidence = self.evidence_dict[vertex_id]
            if evidence is not None:
                vertex_node.node_data["p"] = 1.0 if evidence == "package" else 0.0
                vertex_node.node_data["q"] = 1.0 if evidence == "no package" else 0.0
                vertex_node.calculate_given_probs()

        for edge_node in self.edge_nodes:
            edge_id = edge_node.node_data["identifier"]
            evidence = self.evidence_dict[edge_id]
            if evidence is not None:
                edge_node.node_data["p"] = 1.0 if evidence == "blocked" else 0.0
                edge_node.node_data["q"] = 1.0 if evidence == "unblocked" else 0.0
                edge_node.calculate_given_probs()

    def bayes_network_structure(self):
        self._update_nodes_given_probs()
        network_structure_str = "Printing network structure...\n"

        # Add season node probs to the string
        season_node = self.season_node
        network_structure_str += "\n"
        network_structure_str += (
            "SEASON: \n"
            f"  P(low) = {season_node.probs['low']}\n"
            f"  P(medium) = {season_node.probs['medium']}\n"
            f"  P(high) = {season_node.probs['high']}\n"
        )

        # Add vertex nodes probs to the string
        for vertex_node in self.vertex_nodes:
            if vertex_node.sub_type() == "dummy":
                continue

            vertex_id = vertex_node.node_data["identifier"]
            network_structure_str += "\n"
            network_structure_str += (
                f"VERTEX {vertex_id}: \n"
                f"  P(package|low) = {vertex_node.probs['package']['low']}\n"
                f"  P(package|medium) = {vertex_node.probs['package']['medium']}\n"
                f"  P(package|high) = {vertex_node.probs['package']['high']}\n"
            )

        # Add edge nodes probs to the string
        for edge_node in self.edge_nodes:
            edge_id = edge_node.node_data["identifier"]
            coords1, coords2 = edge_id.split(" ")
            network_structure_str += "\n"
            network_structure_str += (
                f"EDGE {edge_id}: \n"
                f"  P(blocked|no package {coords1}, no package {coords2}) = {edge_node.probs['blocked']['no package']['no package']}\n"
                f"  P(blocked|no package {coords1}, package {coords2}) = {edge_node.probs['blocked']['no package']['package']}\n"
                f"  P(blocked|package {coords1}, no package {coords2}) = {edge_node.probs['blocked']['package']['no package']}\n"
                f"  P(blocked|package {coords1}, package {coords2}) = {edge_node.probs['blocked']['package']['package']}\n"
            )

        return network_structure_str

    def get_evidence_dict(self):
        return deepcopy(self.evidence_dict)

    def probabilistic_reasoning(self, evidence_dict: dict):
        enumeration_ask_all_results = self.enumeration_ask_all(evidence_dict=evidence_dict)
        network_infers_str = "Printing probabilistic reasoning results...\n"

        # Add season node infers to the string
        season_id = self.season_node.node_data["identifier"]
        network_infers_str += "\n"
        network_infers_str += (
            "SEASON:\n"
            f"  P(low) = {enumeration_ask_all_results[season_id]['low']}\n"
            f"  P(medium) = {enumeration_ask_all_results[season_id]['medium']}\n"
            f"  P(high) = {enumeration_ask_all_results[season_id]['high']}\n"
        )

        # Add vertex nodes infers to the string
        for vertex_node in self.vertex_nodes:
            if vertex_node.sub_type() == "dummy":
                continue

            vertex_id = vertex_node.node_data["identifier"]
            network_infers_str += "\n"
            network_infers_str += (
                f"VERTEX {vertex_id}:\n"
                f"  P(package) = {enumeration_ask_all_results[vertex_id]['package']}\n"
                f"  P(no package) = {enumeration_ask_all_results[vertex_id]['no package']}\n"
            )

        # Add edge nodes infers to the string
        for edge_node in self.edge_nodes:
            edge_id = edge_node.node_data["identifier"]
            network_infers_str += "\n"
            network_infers_str += (
                f"EDGE {edge_id}:\n"
                f"  P(blocked) = {enumeration_ask_all_results[edge_id]['blocked']}\n"
                f"  P(unblocked) = {enumeration_ask_all_results[edge_id]['unblocked']}\n"
            )

        return network_infers_str

    def enumeration_ask_all(self, evidence_dict: dict):
        results = dict()

        e = deepcopy(evidence_dict)
        for key in evidence_dict.keys():
            if e[key] is None:
                e.pop(key)

        bn = {"variables": list(self.ordered_variables)}
        for X in tqdm(self.network_nodes.values()):
            node_id = X.node_data["identifier"]

            # Node is not part of the evidence
            if node_id not in list(e.keys()):
                result = self.enumeration_ask(X=X, e=e, bn=bn)
                results[node_id] = result

            # Node is part of the evidence
            else:
                result = dict()
                evidence_value = evidence_dict[node_id]
                for node_value in X.node_values():
                    if node_value == evidence_value:
                        result[node_value] = 1.0
                    else:
                        result[node_value] = 0.0
                results[node_id] = result

        return results

    @staticmethod
    def normalize(Q: dict):
        sum = 0
        for key in Q:
            sum += Q[key]

        for key in Q:
            Q[key] /= sum

        return Q

    def enumeration_ask(self, X: Node, e: dict, bn: dict):
        Q = {xi: 0 for xi in X.node_values()}
        for xi in X.node_values():
            cloned_e = deepcopy(e)
            cloned_e[X.node_data["identifier"]] = xi
            Q[xi] = self.enumerate_all(variables=bn["variables"], e=cloned_e)

        return self.normalize(Q)

    def enumerate_all(self, variables: list, e: dict):
        if len(variables) == 0:
            return 1.0

        Y, rest = variables[0], variables[1:]
        Y_node = self.network_nodes[Y]
        if Y in list(e.keys()):
            return Y_node.probability(value=e[Y], evidence=e) * self.enumerate_all(variables=rest, e=e)
        else:
            sum = 0
            for i, y in enumerate(Y_node.node_values()):
                cloned_e = deepcopy(e)
                cloned_e[Y] = y
                y_probability = Y_node.probability(value=cloned_e[Y], evidence=cloned_e)
                recursive_result = self.enumerate_all(variables=rest, e=cloned_e)
                final_result = y_probability * recursive_result
                sum += final_result

            return sum

    def clone_bayes_network(self):
        environment_data = {
            "x": self.X - 1,
            "y": self.Y - 1,
            "special_edges": deepcopy(self.special_edges),
            "special_vertices": deepcopy(self.special_vertices),
            "leakage_probability": self.leakage_probability,
            "season": deepcopy(self.season),
        }
        return BayesNetwork(environment_data=environment_data)
