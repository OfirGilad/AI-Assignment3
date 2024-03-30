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
   (See the example output format in the file: [output_example.txt](input%2Foutput_example.txt))
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
     P(no package) = 0.5199999999999999
    
   EDGE (1,0) (1,1): 
     P(blocked) = 0.7533760000000002
     P(unblocked) = 0.24662399999999984
   
   VERTEX (1,1): 
   etc.
   ```
5. Option `4`: Quits the program.


## Important note: 
Option `0` does not display updated distributions (after the addition of a new edivdance).
To inspect such changes, please choose option `3`. 


## Non-trivial example runs on at least 2 scenarios, including the input and output:

1. Every edge is fragile and every vertex may contain a package. 

Input:

#X 1                ; Maximum x coordinate
#Y 1                ; Maximum y coordinate


#F 0 0 0 1 0.1      ; Edge from (0,0) to (0,1) is fragile, with p = 1-qi = 0.1
#F 0 0 1 0 0.2      ; Edge from (0,0) to (0,1) is fragile, with p = 1-qi = 0.2
#F 0 1 1 1 0.3      ; Edge from (0,0) to (0,1) is fragile, with p = 1-qi = 0.3
#F 1 0 1 1 0.4      ; Edge from (0,0) to (0,1) is fragile, with p = 1-qi = 0.4

#V 0 0 F 0.4        ; Vertex (1,0) probability of package given low demand season 0.4
#V 0 1 F 0.3        ; Vertex (1,1) probability of package given low demand season 0.3
#V 1 0 F 0.2        ; Vertex (1,0) probability of package given low demand season 0.2
#V 1 1 F 0.1        ; Vertex (1,1) probability of package given low demand season 0.1

#L 0.1              ; Global leakage probability 0.1
#S 0.5 0.4 0.1      ; Prior distribution over season: 0.5 for low, 0.4 for medium, 0.1 for high

Output:

SEASON: 
  P(low) = 0.5
  P(medium) = 0.4
  P(high) = 0.1

VERTEX (0,0): 
  P(package|low) = 0.4
  P(package|medium) = 0.8
  P(package|high) = 1.0

VERTEX (0,1): 
  P(package|low) = 0.3
  P(package|medium) = 0.6
  P(package|high) = 0.8999999999999999

VERTEX (1,0): 
  P(package|low) = 0.2
  P(package|medium) = 0.4
  P(package|high) = 0.6000000000000001

VERTEX (1,1): 
  P(package|low) = 0.1
  P(package|medium) = 0.2
  P(package|high) = 0.30000000000000004

EDGE (0,0) (0,1): 
  P(blocked|no package (0,0), no package (0,1)) = 0.1
  P(blocked|no package (0,0), package (0,1)) = 0.09999999999999998
  P(blocked|package (0,0), no package (0,1)) = 0.09999999999999998
  P(blocked|package (0,0), package (0,1)) = 0.18999999999999995

EDGE (0,0) (1,0): 
  P(blocked|no package (0,0), no package (1,0)) = 0.1
  P(blocked|no package (0,0), package (1,0)) = 0.19999999999999996
  P(blocked|package (0,0), no package (1,0)) = 0.19999999999999996
  P(blocked|package (0,0), package (1,0)) = 0.3599999999999999

EDGE (0,1) (1,1): 
  P(blocked|no package (0,1), no package (1,1)) = 0.1
  P(blocked|no package (0,1), package (1,1)) = 0.30000000000000004
  P(blocked|package (0,1), no package (1,1)) = 0.30000000000000004
  P(blocked|package (0,1), package (1,1)) = 0.51

EDGE (1,0) (1,1): 
  P(blocked|no package (1,0), no package (1,1)) = 0.1
  P(blocked|no package (1,0), package (1,1)) = 0.4
  P(blocked|package (1,0), no package (1,1)) = 0.4
  P(blocked|package (1,0), package (1,1)) = 0.64

2. One third of the edges is fragile and one third is blocked. Every vertex may contain a package.

Input: 

#X 2                ; Maximum x coordinate
#Y 2                ; Maximum y coordinate


#F 0 0 0 1 0.1      ; Edge from (0,0) to (0,1) is fragile, with p = 1-qi = 0.1
#F 1 0 2 0 0.1      ; Edge from (1,0) to (2,0) is fragile, with p = 1-qi = 0.1
#F 0 1 0 2 0.3      ; Edge from (0,1) to (0,2) is fragile, with p = 1-qi = 0.3
#F 2 0 1 2 0.3      ; Edge from (2,0) to (1,2) is fragile, with p = 1-qi = 0.3

#B 0 0 1 0 0.2      ; Edge from (0,0) to (1,0) is always blocked
#B 1 1 2 1 0.2      ; Edge from (1,1) to (2,1) is always blocked
#B 1 1 1 2 0.4      ; Edge from (1,1) to (1,2) is always blocked
#B 2 1 2 2 0.3      ; Edge from (2,1) to (2,2) is always blocked

#V 0 0 F 0.1        ; Vertex (0,0) probability of package given low demand season 0.1
#V 0 1 F 0.2        ; Vertex (0,1) probability of package given low demand season 0.2
#V 1 0 F 0.3        ; Vertex (1,0) probability of package given low demand season 0.3
#V 1 1 F 0.4        ; Vertex (1,1) probability of package given low demand season 0.4
#V 0 2 F 0.5        ; Vertex (0,2) probability of package given low demand season 0.5
#V 2 0 F 0.6        ; Vertex (2,0) probability of package given low demand season 0.6
#V 1 2 F 0.7        ; Vertex (1,2) probability of package given low demand season 0.7
#V 2 1 F 0.8        ; Vertex (2,1) probability of package given low demand season 0.8
#V 2 2 F 0.9        ; Vertex (2,2) probability of package given low demand season 0.9

#L 0.1              ; Global leakage probability 0.1
#S 0.25 0.25 0.5      ; Prior distribution over season: 0.25 for low, 0.25 for medium, 0.5 for high



Output:

SEASON: 
  P(low) = 0.25
  P(medium) = 0.25
  P(high) = 0.5

VERTEX (0,0): 
  P(package|low) = 0.1
  P(package|medium) = 0.2
  P(package|high) = 0.30000000000000004

VERTEX (0,1): 
  P(package|low) = 0.2
  P(package|medium) = 0.4
  P(package|high) = 0.6000000000000001

VERTEX (1,0): 
  P(package|low) = 0.3
  P(package|medium) = 0.6
  P(package|high) = 0.8999999999999999

VERTEX (1,1): 
  P(package|low) = 0.4
  P(package|medium) = 0.8
  P(package|high) = 1.0

VERTEX (0,2): 
  P(package|low) = 0.5
  P(package|medium) = 1.0
  P(package|high) = 1.0

VERTEX (2,0): 
  P(package|low) = 0.6
  P(package|medium) = 1.0
  P(package|high) = 1.0

VERTEX (1,2): 
  P(package|low) = 0.7
  P(package|medium) = 1.0
  P(package|high) = 1.0

VERTEX (2,1): 
  P(package|low) = 0.8
  P(package|medium) = 1.0
  P(package|high) = 1.0

VERTEX (2,2): 
  P(package|low) = 0.9
  P(package|medium) = 1.0
  P(package|high) = 1.0

EDGE (0,0) (0,1): 
  P(blocked|no package (0,0), no package (0,1)) = 0.1
  P(blocked|no package (0,0), package (0,1)) = 0.09999999999999998
  P(blocked|package (0,0), no package (0,1)) = 0.09999999999999998
  P(blocked|package (0,0), package (0,1)) = 0.18999999999999995

EDGE (1,0) (2,0): 
  P(blocked|no package (1,0), no package (2,0)) = 0.1
  P(blocked|no package (1,0), package (2,0)) = 0.09999999999999998
  P(blocked|package (1,0), no package (2,0)) = 0.09999999999999998
  P(blocked|package (1,0), package (2,0)) = 0.18999999999999995

EDGE (0,1) (0,2): 
  P(blocked|no package (0,1), no package (0,2)) = 0.1
  P(blocked|no package (0,1), package (0,2)) = 0.30000000000000004
  P(blocked|package (0,1), no package (0,2)) = 0.30000000000000004
  P(blocked|package (0,1), package (0,2)) = 0.51

EDGE (2,0) (1,2): 
  P(blocked|no package (2,0), no package (1,2)) = 0.1
  P(blocked|no package (2,0), package (1,2)) = 0.30000000000000004
  P(blocked|package (2,0), no package (1,2)) = 0.30000000000000004
  P(blocked|package (2,0), package (1,2)) = 0.51

EDGE (0,0) (1,0): 
  P(blocked|no package (0,0), no package (1,0)) = 1.0
  P(blocked|no package (0,0), package (1,0)) = 1.0
  P(blocked|package (0,0), no package (1,0)) = 1.0
  P(blocked|package (0,0), package (1,0)) = 1.0

EDGE (1,1) (2,1): 
  P(blocked|no package (1,1), no package (2,1)) = 1.0
  P(blocked|no package (1,1), package (2,1)) = 1.0
  P(blocked|package (1,1), no package (2,1)) = 1.0
  P(blocked|package (1,1), package (2,1)) = 1.0

EDGE (1,1) (1,2): 
  P(blocked|no package (1,1), no package (1,2)) = 1.0
  P(blocked|no package (1,1), package (1,2)) = 1.0
  P(blocked|package (1,1), no package (1,2)) = 1.0
  P(blocked|package (1,1), package (1,2)) = 1.0

EDGE (2,1) (2,2): 
  P(blocked|no package (2,1), no package (2,2)) = 1.0
  P(blocked|no package (2,1), package (2,2)) = 1.0
  P(blocked|package (2,1), no package (2,2)) = 1.0
  P(blocked|package (2,1), package (2,2)) = 1.0
