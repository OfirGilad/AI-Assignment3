# Introduction to Artificial Intelligence - Programming Assignment 3

## Detailed installation instructions:

In order to run the code create a Python environment as follows: \
`Python3.10` \
`numpy==1.26.3`

And to run the project:
1. open the [main.py](src/main.py) script.
2. Update the `data_filepath` parameter with the path to the input txt file.
3. Run the `main` function.

## Explanation of the method for constructing the BN and our reasoning algorithm:

The BN is constructed inside the `BayesNetwork` class inside the [bayes_network.py](src%2Fbayes_network.py) script,
that receives the parsed input data and build all the network nodes in the following order:
1. Create the `season` node 
   (using the values from parameter `#S`).
2. Create the `vertices` nodes, and set the season node as their parent
   (using the values from parameter `#V`).
3. Create the `edges` nodes, and set the vertices nodes as their parents
   (using the values from parameters `#B`,`#F`,`#L`).

**Notice:** We also create `dummy vertices` nodes (Used for the probabilistic reasoning as suggested in the assignment)
which are not part of the input data. 

Each node in the BN is an object of the `Node` class inside the [node.py](src%2Fnode.py),
where each node has reference to its parents and children (if they exist).

The reasoning algorithm is implemented using the `Variable Elimination` algorithm.\
The algorithm is implemented in the `probabilistic_reasoning` function in the 
[bayes_network.py](src%2Fbayes_network.py) script.

## How to work with the interface:

When you run the `main` function, you will be prompted with the following options:
```
The probabilistic reasoning 3 items:
1. What is the probability that each of the vertices contains packages?
2. What is the probability that each of the edges is blocked?
3. What is the distribution of the season variable?

Choose operation from the following options:
0. Print network structure.
1. Reset evidence list to empty.
2. Add piece of evidence to evidence list.
3. Do probabilistic reasoning according to items 1, 2, 3 and report the results.
4. Quit.
Your choice: _
```

The available options are: `0`, `1`, `2`, `3`, `4`, where:
1. Option `0`: Prints the network structure similar to the example in the assignment description.
   (See the example output format in the file: [output_example.txt](input%2Foutput_example.txt))\
   **Notice:** The updated distributions according to the current evidence list are displayed.
2. Option `1`: Resets the evidence list to be an empty list.
3. Option `2`: Adds a piece of evidence to the evidence list.
   You will be prompted with the following message:
   ```
   What piece of evidence do you want to add? (Write 'back' to go back)
   Your answer: _
   ```
   You can add evidence in the following format:
   - `Low reported at season`
   - `Medium reported at season`
   - `High reported at season`
   - `Package reported at vertex (0,0)`
   - `No Package reported at vertex (0,0)`
   - `Blockage reported at edge (0,0) (0,1)`
   - `No Blockage reported at edge (0,0) (0,1)`
4. Option `3`: Does probabilistic reasoning according to items 1, 2, 3:
   - `Item 1`: What is the probability that each of the vertices contains packages?
   - `Item 2`: What is the probability that each of the edges is blocked?
   - `Item 3`: What is the distribution of the season variable?
   
   And the results will be printed in the following format:
   ```
   SEASON:
     P(low) = 0.1
     P(medium) = 0.4
     P(high) = 0.5
   
   VERTEX (1,0):
     P(package) = 0.4800000000000001
     P(no package) = 0.52
   
   EDGE (1,0) (1,1):
     P(blocked) = 0.73912
     P(unblocked) = 0.26088
   
   VERTEX (1,1):
   etc.
   ```
5. Option `4`: Quits the program.

## Non-trivial example runs on at least 2 scenarios, including the input and output:

See the file [input_results.txt](input_results.txt) for the example runs of the 2 scenarios 
in the following input files:
- [input1.txt](input%2Finput1.txt)
- [input2.txt](input%2Finput2.txt)