from bayes_network import BayesNetwork


class Interface:
    def __init__(self, bayes_network: BayesNetwork):
        self.bayes_network = bayes_network
        self.user_actions = {
            "1": self._reset_evidence_list,
            "2": self._add_evidence,
            "3": self._probabilistic_reasoning,
            "4": self._quit
        }

    def _reset_evidence_list(self):
        print("TBD")

    def _add_evidence(self):
        print("TBD")

    def _probabilistic_reasoning(self):
        self.bayes_network.calculate_probs()

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
                print(f"Invalid input: {user_input}! Write either '1','2','3' or '4'. \n")
