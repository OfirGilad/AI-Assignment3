from bayes_network import BayesNetwork


class Interface:
    def __init__(self, bayes_network: BayesNetwork):
        self.bayes_network = bayes_network
        self.user_actions = {
            "0": self._print_network_structure,
            "1": self._reset_evidence_list,
            "2": self._add_evidence,
            "3": self._probabilistic_reasoning,
            "4": self._quit
        }

        # Evidence handle
        self.evidence_dict = self.bayes_network.get_evidence_dict()
        self.piece_of_evidence_format = [
            " reported at season",
            " reported at vertex ",
            " reported at edge ",
        ]
        self.evidence_values_map = {
            "Low": "low",
            "Medium": "medium",
            "High": "high",
            "Package": "package",
            "No Package": "no package",
            "Blockage": "blocked",
            "No Blockage": "unblocked"
        }

    def _print_network_structure(self):
        cloned_bayes_network = self.bayes_network.clone_bayes_network()
        cloned_bayes_network.evidence_dict = self.evidence_dict
        result = cloned_bayes_network.bayes_network_structure()
        print(result)

    def _reset_evidence_list(self):
        self.evidence_dict = self.bayes_network.get_evidence_dict()
        print("Evidence list has been reset to empty.\n")

    def _add_evidence(self):
        """
        Accepted evidence formats:
        - "Low reported at season"
        - "Medium reported at season"
        - "High reported at season"
        - "Package reported at vertex (0,0)"
        - "No Package reported at vertex (0,0)"
        - "Blockage reported at edge (0,0) (0,1)"
        - "No Blockage reported at edge (0,0) (0,1)"
        Other formats will fail.
        """

        evidence_info = (
            "What piece of evidence do you want to add? (Write 'back' to go back)\n"
            "Your answer: "
        )
        while True:
            evidence = input(evidence_info)

            # Season evidence
            if self.piece_of_evidence_format[0] in evidence:
                evidence_params = evidence.split(self.piece_of_evidence_format[0])
                if evidence_params[0] in ["Low", "Medium", "High"]:
                    self.evidence_dict["season"] = self.evidence_values_map[evidence_params[0]]
                    result_str = "Season evidence has been added."
                else:
                    result_str = (
                        "Invalid season evidence! Only 'Low', 'Medium' and 'High' are accepted. Please try again."
                    )

            # Vertex evidence
            elif self.piece_of_evidence_format[1] in evidence:
                evidence_params = evidence.split(self.piece_of_evidence_format[1])
                if evidence_params[0] in ["Package", "No Package"]:
                    if evidence_params[1] in self.evidence_dict.keys():
                        self.evidence_dict[evidence_params[1]] = self.evidence_values_map[evidence_params[0]]
                        result_str = "Vertex evidence has been added."
                    else:
                        result_str = "This vertex isn't part of the network! Please try again."
                else:
                    result_str = (
                        "Invalid vertex evidence! Only 'Package' and 'No Package' are accepted. Please try again."
                    )

            # Edge evidence
            elif self.piece_of_evidence_format[2] in evidence:
                evidence_params = evidence.split(self.piece_of_evidence_format[2])
                if evidence_params[0] in ["Blockage", "No Blockage"]:
                    if evidence_params[1] in self.evidence_dict.keys():
                        self.evidence_dict[evidence_params[1]] = self.evidence_values_map[evidence_params[0]]
                        result_str = "Edge evidence has been added."
                    else:
                        result_str = "This edge isn't part of the network! Please try again."
                else:
                    result_str = (
                        "Invalid edge evidence! Only 'Blockage' and 'No Blockage' are accepted. Please try again."
                    )

            # Back to main menu
            elif evidence.lower() == "back":
                break

            # Invalid evidence format
            else:
                result_str = "Invalid evidence format! Please try again."

            result_str += "\n"
            print(result_str)

    def _probabilistic_reasoning(self):
        cloned_bayes_network = self.bayes_network.clone_bayes_network()
        result = cloned_bayes_network.probabilistic_reasoning(evidence_dict=self.evidence_dict)
        print(result)

    @staticmethod
    def _quit():
        exit()

    def run(self):
        items_information = (
            "The probabilistic reasoning 3 items:\n" +
            "1. What is the probability that each of the vertices contains packages?\n" +
            "2. What is the probability that each of the edges is blocked?\n" +
            "3. What is the distribution of the season variable?\n"
        )
        print(items_information)

        user_information = (
            "Choose operation from the following options:\n"
            "0. Print network structure.\n"
            "1. Reset evidence list to empty.\n"
            "2. Add piece of evidence to evidence list.\n"
            "3. Do probabilistic reasoning according to items 1, 2, 3 and report the results.\n"
            "4. Quit.\n"
            "Your choice: "
        )

        while True:
            user_input = input(user_information)
            user_action = self.user_actions.get(user_input, None)
            if user_action is not None:
                user_action()
            else:
                print(f"Invalid input: {user_input}! Write either '0','1','2','3' or '4'.\n")
