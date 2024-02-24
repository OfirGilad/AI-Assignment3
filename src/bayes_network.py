import numpy as np
from copy import deepcopy


class BayesNetwork:
    def __init__(self, environment_data: dict):
        # Parse state initial parameters
        self.X = environment_data["x"] + 1
        self.Y = environment_data["y"] + 1
        self.special_edges = environment_data.get("special_edges", list())
        self.special_vertices = environment_data.get("special_vertices", list())
        self.leakage_probability = environment_data.get("leakage_probability", 0.0)
        self.season = environment_data.get("season", {"low": 0.0, "medium": 0.0, "high": 0.0})

        # Build state graph
        self.total_vertices = self.X * self.Y
        self.adjacency_matrix = None
        self._build_adjacency_matrix()

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
