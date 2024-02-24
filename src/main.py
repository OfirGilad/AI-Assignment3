from ascii_parser import Parser
from bayes_network import BayesNetwork
from interface import Interface


def run(data_filepath: str):
    parser = Parser()
    environment_data = parser.parse_data(data_filepath=data_filepath)
    # print(environment_data)
    bayes_network = BayesNetwork(environment_data=environment_data)
    # print(bayes_network)
    interface = Interface(bayes_network=bayes_network)
    interface.run()


def main():
    # TODO: Fill the data_filepath parameter
    data_filepath = "../input/input.txt"
    run(data_filepath=data_filepath)


if __name__ == '__main__':
    main()
