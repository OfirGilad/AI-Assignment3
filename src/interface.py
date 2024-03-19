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

    def _print_network_structure(self):
        result = self.bayes_network.bayes_network_structure()
        print(result)

    def _reset_evidence_list(self):
        self.evidence_dict = self.bayes_network.get_evidence_dict()
        print("Evidence list has been reset to empty.")

    def _add_evidence(self):
        '''
        Accepted evidence formats:
        - "Low reported at season"
        - "Medium reported at season"
        - "High reported at season"
        - "Package reported at vertex (0,0)"
        - "No Package reported at vertex (0,0)"
        - "Blockage reported at edge (0,0) (0,1)"
        - "No Blockage reported at edge (0,0) (0,1)"
        Other formats will fail.
        '''

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
                    self.evidence_dict["season"] = evidence_params[0].lower()
                    print("Season evidence has been added.")
                else:
                    print("Invalid season evidence! Only 'Low', 'Medium' and 'High' are accepted. Please try again.")

            # Vertex evidence
            elif self.piece_of_evidence_format[1] in evidence:
                evidence_params = evidence.split(self.piece_of_evidence_format[1])
                if evidence_params[0] in ["Package", "No Package"]:
                    if evidence_params[1] in self.evidence_dict.keys():
                        self.evidence_dict[evidence_params[1]] = evidence_params[0].lower()
                        print("Vertex evidence has been added.")
                    else:
                        print("This vertex isn't part of the network! Please try again.")
                else:
                    print("Invalid vertex evidence! Only 'Package' and 'No Package' are accepted. Please try again.")

            # Edge evidence
            elif self.piece_of_evidence_format[2] in evidence:
                evidence_params = evidence.split(self.piece_of_evidence_format[2])
                if evidence_params[0] in ["Blockage", "No Blockage"]:
                    if evidence_params[1] in self.evidence_dict.keys():
                        self.evidence_dict[evidence_params[1]] = evidence_params[0].lower()
                        print("Edge evidence has been added.")
                    else:
                        print("This edge isn't part of the network! Please try again.")
                else:
                    print("Invalid edge evidence! Only 'Blockage' and 'No Blockage' are accepted. Please try again.")

            # Back to main menu
            elif evidence.lower() == "back":
                break

            # Invalid evidence format
            else:
                print("Invalid evidence format! Please try again.")

    def _probabilistic_reasoning(self):
        print("TBD")

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
                print(f"Invalid input: {user_input}! Write either '0','1','2','3' or '4'. \n")
