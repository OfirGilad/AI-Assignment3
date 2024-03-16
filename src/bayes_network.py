import numpy as np
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

        # Build state graph
        self.total_vertices = self.X * self.Y
        self.adjacency_matrix = None
        self._build_adjacency_matrix()

        self.network_nodes = dict()
        self._build_network()

    def coordinates_to_vertex_index(self, coords: list) -> int:
        row, col = coords
        if row < 0 or row >= self.X or col < 0 or col >= self.Y:
            raise ValueError("Coordinates out of bounds")

        return row * self.Y + col

    def vertex_index_to_coordinates(self, idx: int) -> list:
        if idx < 0 or idx > self.total_vertices:
            raise ValueError("Vertex index out of bounds")

        row = idx // self.Y
        col = idx % self.Y
        coords = [row, col]
        return coords

    def _apply_special_edges(self):
        for special_edge in self.special_edges:
            if special_edge["type"] == "always blocked":
                first_node = self.coordinates_to_vertex_index(coords=special_edge["from"])
                second_node = self.coordinates_to_vertex_index(coords=special_edge["to"])

                self.adjacency_matrix[first_node, second_node] = 0
                self.adjacency_matrix[second_node, first_node] = 0

    def _build_adjacency_matrix(self):
        self.adjacency_matrix = np.zeros(shape=(self.total_vertices, self.total_vertices), dtype=int)

        for i in range(self.X):
            for j in range(self.Y):
                current_node = self.coordinates_to_vertex_index(coords=[i, j])

                # Connect with the right neighbor (if exists)
                if j + 1 < self.Y:
                    right_neighbor = self.coordinates_to_vertex_index(coords=[i, j + 1])
                    self.adjacency_matrix[current_node, right_neighbor] = 1
                    self.adjacency_matrix[right_neighbor, current_node] = 1

                # Connect with the bottom neighbor (if exists)
                if i + 1 < self.X:
                    bottom_neighbor = self.coordinates_to_vertex_index(coords=[i + 1, j])
                    self.adjacency_matrix[current_node, bottom_neighbor] = 1
                    self.adjacency_matrix[bottom_neighbor, current_node] = 1

        self._apply_special_edges()

    def _build_network(self):
        vertices = list()
        edges = list()

        season_node = Node(node_data=self.season)

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

        # Add edges to the network
        for edge_data in self.special_edges:
            edge_node = Node(node_data=edge_data)
            edges.append(edge_node)

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

        print("Network Nodes Structure:")
        print(season_node.network_tree_str())

    def calculate_network_probabs(self):
        network_probabs_str = ""

        season_node = self.network_nodes["season"]
        season_node.calculate_node_probabs()

        # Add season node probabs to the string
        network_probabs_str += (
            "SEASON: \n"
            f"  P(low) = {season_node.probabs['low']}\n"
            f"  P(medium) = {season_node.probabs['medium']}\n"
            f"  P(high) = {season_node.probabs['high']}\n"
            "\n"
        )

        for vertex_node in self.network_nodes["vertices"]:
            vertex_node.calculate_node_probabs()
            if vertex_node.sub_type() == "dummy":
                continue

            # Add vertex node probabs to the string
            coords = f"({vertex_node.node_data['at'][0]},{vertex_node.node_data['at'][1]})"
            network_probabs_str += (
                f"VERTEX {coords}: \n"
                f"  P(package|low) = {vertex_node.probabs['package']['low']}\n"
                f"  P(package|medium) = {vertex_node.probabs['package']['medium']}\n"
                f"  P(package|high) = {vertex_node.probabs['package']['high']}\n"
                "\n"
            )

        for edge_node in self.network_nodes["edges"]:
            edge_node.calculate_node_probabs()
            coords1 = f"({edge_node.node_data['from'][0]},{edge_node.node_data['from'][1]})"
            coords2 = f"({edge_node.node_data['to'][0]},{edge_node.node_data['to'][1]})"

            # Add edge node probabs to the string
            network_probabs_str += (
                f"EDGE {coords1} {coords2}: \n"
                f"  P(blocked|no package {coords1}, no package {coords2}) = {edge_node.probabs['blocked']['no package']['no package']}\n"
                f"  P(blocked|no package {coords1}, package {coords2}) = {edge_node.probabs['blocked']['no package']['package']}\n"
                f"  P(blocked|package {coords1}, no package {coords2}) = {edge_node.probabs['blocked']['package']['no package']}\n"
                f"  P(blocked|package {coords1}, package {coords2}) = {edge_node.probabs['blocked']['package']['package']}\n"
                "\n"
            )

        return network_probabs_str

    def convert_to_node_indices(self, current_vertex, next_vertex, mode: str):
        # The input vertices are list of coordinates
        if mode == "Coords":
            current_vertex_index = self.coordinates_to_vertex_index(coords=current_vertex)
            next_vertex_index = self.coordinates_to_vertex_index(coords=next_vertex)

        # The input vertices are indices of the vertices on the graph
        elif mode == "Indices":
            current_vertex_index = current_vertex
            next_vertex_index = next_vertex
        # Encountered invalid mode
        else:
            raise ValueError(f"Invalid mode: {mode}. Current available modes are: Coords, Indices")

        return current_vertex_index, next_vertex_index

    def convert_to_node_coords(self, current_vertex, next_vertex, mode: str):
        # The input vertices are list of coordinates
        if mode == "Coords":
            current_vertex_coords = current_vertex
            next_vertex_coords = next_vertex
        # The input vertices are indices of the vertices on the graph
        elif mode == "Indices":
            current_vertex_coords = self.vertex_index_to_coordinates(idx=current_vertex)
            next_vertex_coords = self.vertex_index_to_coordinates(idx=next_vertex)
        # Encountered invalid mode
        else:
            raise ValueError(f"Invalid mode: {mode}")

        return current_vertex_coords, next_vertex_coords

    def is_path_available(self, current_vertex, next_vertex, mode):
        current_vertex_index, next_vertex_index = self.convert_to_node_indices(
            current_vertex=current_vertex,
            next_vertex=next_vertex,
            mode=mode
        )

        # Check if the edge is missing
        edge_missing_validation = (
            self.adjacency_matrix[current_vertex_index, next_vertex_index] == 0 or
            self.adjacency_matrix[current_vertex_index, next_vertex_index] == 0
        )
        if edge_missing_validation:
            return False

        # All validation passed
        return True

    def edge_cost(self, current_vertex, next_vertex, mode="Coords"):
        current_vertex_index, next_vertex_index = self.convert_to_node_indices(
            current_vertex=current_vertex,
            next_vertex=next_vertex,
            mode=mode
        )

        return self.adjacency_matrix[current_vertex_index, next_vertex_index]

    def __str__(self):
        # Coordinates
        print_data = (
            f"SEASON: \n"
            f"  P(low) = {self.season['low']}\n"
            f"  P(medium) = {self.season['medium']}\n"
            f"  P(high) = {self.season['high']}\n"
        )

        print_data += "\n"
        return print_data

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
