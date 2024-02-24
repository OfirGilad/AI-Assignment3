class Parser:
    def __init__(self):
        self.parsed_data = {
            "x": 0,
            "y": 0,
            "special_edges": list(),
            "special_vertices": list(),
            "leakage_probability": 0.0,
            "season": {"low": 0.0, "medium": 0.0, "high": 0.0}
        }
        self.options_dict = {
            "#X": self._handle_x,
            "#Y": self._handle_y,
            "#B": self._handle_b,
            "#F": self._handle_f,
            "#V": self._handle_v,
            "#L": self._handle_l,
            "#S": self._handle_s
        }

    def _handle_x(self, line_data_args):
        self.parsed_data["x"] = int(line_data_args[1])

    def _handle_y(self, line_data_args):
        self.parsed_data["y"] = int(line_data_args[1])

    def _handle_b(self, line_data_args):
        edge = {
            "type": "always blocked",
            "from": [int(line_data_args[1]), int(line_data_args[2])],
            "to": [int(line_data_args[3]), int(line_data_args[4])],
        }
        self.parsed_data["special_edges"].append(edge)

    def _handle_f(self, line_data_args):
        edge = {
            "type": "fragile",
            "from": [int(line_data_args[1]), int(line_data_args[2])],
            "to": [int(line_data_args[3]), int(line_data_args[4])],
            "p": float(line_data_args[5]),
        }
        self.parsed_data["special_edges"].append(edge)

    def _handle_v(self, line_data_args):
        vertex = {
            "type": "vertex",
            "at": [int(line_data_args[1]), int(line_data_args[2])],
            "p": float(line_data_args[4])
        }
        self.parsed_data["special_vertices"].append(vertex)

    def _handle_l(self, line_data_args):
        self.parsed_data["leakage_probability"] = float(line_data_args[1])

    def _handle_s(self, line_data_args):
        self.parsed_data["season"]["low"] = float(line_data_args[1])
        self.parsed_data["season"]["medium"] = float(line_data_args[2])
        self.parsed_data["season"]["high"] = float(line_data_args[3])

    def parse_data(self, data_filepath):
        with open(data_filepath) as data_file:
            line_data = data_file.readline()
            while line_data != "":
                line_data_args = line_data.split()
                if len(line_data_args) != 0 and line_data_args[0] in self.options_dict.keys():
                    self.options_dict[line_data_args[0]](line_data_args)
                line_data = data_file.readline()
        return self.parsed_data
