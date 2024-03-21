from copy import deepcopy
import itertools

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
        self.network_nodes = dict()
        self.evidence_dict = dict()
        self._build_network()

    def _build_network(self):
        vertices = list()
        edges = list()

        season_node = Node(node_data=self.season)

        # Build evidence dict
        self.evidence_dict[season_node.node_data["identifier"]] = {
            "evidence": None,
            "ref": season_node
        }

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
            vertices.append(dummy_vertex_node)

            # Add connections between vertices and season node
            dummy_vertex_node.add_parent(season_node)
            season_node.add_child(dummy_vertex_node)

        # Add vertices to the network
        for vertex_data in self.special_vertices:
            vertex_node = Node(node_data=vertex_data)
            vertices.append(vertex_node)

            # Add connections between vertices and season node
            vertex_node.add_parent(season_node)
            season_node.add_child(vertex_node)

            # Build evidence dict
            self.evidence_dict[vertex_node.node_data["identifier"]] = {
                "evidence": None,
                "ref": vertex_node
            }

        # Add edges to the network
        for edge_data in self.special_edges:
            edge_data["leakage_probability"] = self.leakage_probability
            edge_node = Node(node_data=edge_data)
            edges.append(edge_node)

            # Build evidence dict
            self.evidence_dict[edge_node.node_data["identifier"]] = {
                "evidence": None,
                "ref": edge_node
            }

            # Add connections between edges and vertices
            for vertex_node in vertices:
                if edge_node.node_data["from"] == vertex_node.node_data["at"]:
                    vertex_node.add_child(edge_node)
                    edge_node.add_parent(vertex_node)
                elif edge_node.node_data["to"] == vertex_node.node_data["at"]:
                    vertex_node.add_child(edge_node)
                    edge_node.add_parent(vertex_node)
                else:
                    continue

        self.network_nodes["season"] = season_node
        self.network_nodes["vertices"] = vertices
        self.network_nodes["edges"] = edges

        # TODO: Remove this print before submission
        # print("Network Nodes Structure:")
        # print(season_node.network_tree_str())

    def bayes_network_structure(self):
        season_node = self.network_nodes["season"]

        # Add season node probs to the string
        network_structure_str = (
            "SEASON: \n"
            f"  P(low) = {season_node.probs['low']}\n"
            f"  P(medium) = {season_node.probs['medium']}\n"
            f"  P(high) = {season_node.probs['high']}\n"
            "\n"
        )

        for vertex_node in self.network_nodes["vertices"]:
            if vertex_node.sub_type() == "dummy":
                continue

            # Add vertex node probs to the string
            coords = vertex_node.node_data["identifier"]
            network_structure_str += (
                f"VERTEX {coords}: \n"
                f"  P(package|low) = {vertex_node.probs['package']['low']}\n"
                f"  P(package|medium) = {vertex_node.probs['package']['medium']}\n"
                f"  P(package|high) = {vertex_node.probs['package']['high']}\n"
                "\n"
            )

        for edge_node in self.network_nodes["edges"]:
            # Add edge node probs to the string
            coords1, coords2 = edge_node.node_data["identifier"].split(" ")
            network_structure_str += (
                f"EDGE {coords1} {coords2}: \n"
                f"  P(blocked|no package {coords1}, no package {coords2}) = {edge_node.probs['blocked']['no package']['no package']}\n"
                f"  P(blocked|no package {coords1}, package {coords2}) = {edge_node.probs['blocked']['no package']['package']}\n"
                f"  P(blocked|package {coords1}, no package {coords2}) = {edge_node.probs['blocked']['package']['no package']}\n"
                f"  P(blocked|package {coords1}, package {coords2}) = {edge_node.probs['blocked']['package']['package']}\n"
                "\n"
            )

        return network_structure_str

    def get_evidence_dict(self):
        return deepcopy(self.evidence_dict)

    def _update_nodes_given_probs(self):
        for evidence in self.evidence_dict.values():
            node = evidence["ref"]
            if node.type() == "season":
                node.node_data["low"] = 1.0 if evidence["evidence"] == "Low" else 0.0
                node.node_data["medium"] = 1.0 if evidence["evidence"] == "Medium" else 0.0
                node.node_data["high"] = 1.0 if evidence["evidence"] == "High" else 0.0
            elif node.type() == "vertex":
                node.node_data["p"] = 1.0 if evidence["evidence"] == "Package" else 0.0
                node.node_data["q"] = 1.0 if evidence["evidence"] == "No Package" else 0.0
            elif node.type() == "edge":
                node.node_data["p"] = 1.0 if evidence["evidence"] == "Blockage" else 0.0
                node.node_data["q"] = 1.0 if evidence["evidence"] == "No Blockage" else 0.0
            else:
                continue
            node.calculate_given_probs()

    def probabilistic_reasoning(self, evidence_dict: dict):
        self.evidence_dict = evidence_dict
        self._update_nodes_given_probs()

        season_node = self.network_nodes["season"]
        season_node.calculate_infers()
        network_infers_str = (
            "SEASON: \n"
            f"  P(low) = {season_node.infers['low']}\n"
            f"  P(medium) = {season_node.infers['medium']}\n"
            f"  P(high) = {season_node.infers['high']}\n"
            "\n"
        )

        for vertex_node in self.network_nodes["vertices"]:
            vertex_node.calculate_infers()
            if vertex_node.sub_type() == "dummy":
                continue

            coords = vertex_node.node_data["identifier"]
            network_infers_str += (
                f"VERTEX {coords}: \n"
                f"  P(package) = {vertex_node.infers['package']}\n"
                f"  P(no package) = {vertex_node.infers['no package']}\n"
                "\n"
            )

        for edge_node in self.network_nodes["edges"]:
            edge_node.calculate_infers()
            coords1, coords2 = edge_node.node_data["identifier"].split(" ")
            network_infers_str += (
                f"EDGE {coords1} {coords2}: \n"
                f"  P(blocked) = {edge_node.infers['blocked']}\n"
                f"  P(no blocked) = {edge_node.infers['unblocked']}\n"
                "\n"
            )

        return network_infers_str

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
