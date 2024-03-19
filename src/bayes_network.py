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
        node_type = season_node.node_data["type"]
        self.evidence_dict[node_type] = None

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
                "q": 1.0
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
            coords = str(tuple(vertex_node.node_data["at"])).replace(" ", "")
            self.evidence_dict[coords] = None

        # Add edges to the network
        for edge_data in self.special_edges:
            edge_data["leakage_probability"] = self.leakage_probability
            edge_node = Node(node_data=edge_data)
            edges.append(edge_node)

            # Build evidence dict
            coords1 = str(tuple(edge_node.node_data["from"])).replace(" ", "")
            coords2 = str(tuple(edge_node.node_data["to"])).replace(" ", "")
            edge_coords = f"{coords1} {coords2}"
            self.evidence_dict[edge_coords] = None

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
        print("Network Nodes Structure:")
        print(season_node.network_tree_str())

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
            coords = f"({vertex_node.node_data['at'][0]},{vertex_node.node_data['at'][1]})"
            network_structure_str += (
                f"VERTEX {coords}: \n"
                f"  P(package|low) = {vertex_node.probs['package']['low']}\n"
                f"  P(package|medium) = {vertex_node.probs['package']['medium']}\n"
                f"  P(package|high) = {vertex_node.probs['package']['high']}\n"
                "\n"
            )

        for edge_node in self.network_nodes["edges"]:
            coords1 = f"({edge_node.node_data['from'][0]},{edge_node.node_data['from'][1]})"
            coords2 = f"({edge_node.node_data['to'][0]},{edge_node.node_data['to'][1]})"

            # Add edge node probs to the string
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
