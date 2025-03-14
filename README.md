## Graph-Based Multi-Agent Bayesian-Network based Simulation

This repository implements a simulation environment for a pursuit-evasion problem on a graph. In this project, a "target" moves randomly on a network of interconnected nodes while multiple "agents" use various strategies to catch it. The simulation is implemented entirely in Python and uses only standard libraries.

---

## Overview

The core of the simulation is a custom graph structure where:
- **Nodes** represent positions in the environment.
- **Edges** define connections between nodes.
- Each node stores extra information (e.g., flags for target, agent, check positions, and estimated probabilities).

Multiple agent strategies are implemented, each using a different algorithm to pursue the target:
- **Agent 0:** Selects a random starting position for the agent and lets the target perform a random walk.
- **Agent 1:** Uses Breadth-First Search (BFS) to plan its pursuit.
- **Agent 2:** Employs Depth-First Search (DFS) to navigate the graph.
- **Agent 3:** A variant of random search with additional messaging.
- **Agent 4:** Implements a probability-based approach by estimating likelihoods based on neighbor information.
- **Agent 5:** Enhances the probability-based search with evidence weighting.
- **Agent 6:** Combines BFS with a check-position strategy to update its movement.
- **Agent 7:** Integrates BFS and probability-based refinements to decide the next move.

A test section at the end of the code repeatedly runs one of the agent strategies (e.g., Agent 2) over a graph of 40 nodes, computes the average number of steps taken to catch the target, and calculates the standard deviation.

---

## Key Components

### Import and Utility Functions

- **Imports:**  
  Uses standard Python libraries:
  - `random`
  - `collections.deque`
  - `statistics`
  
- **Utility Functions:**  
  - `list_stdev(l)`: Calculates the population standard deviation of a list.
  - `Average(lst)`: Computes the average of a list.
  - `randomS(l)`: Returns a random element from a list.
  - `normalize(probs)`: Normalizes a list of probabilities so that they sum to 1.
  - `sortL(l)`: Converts list items to integers, sorts them, and converts them back to strings.

### Graph Class

The `graph` class encapsulates the environment and includes methods for:
- **Graph Construction:**  
  - `addNode(k)` and `addEdge(k, val)` add nodes and edges.
  - `EvnSet(numN)`: Sets up a circular graph of `numN` nodes with additional random edges (10 extra edges are added).
  - `printNb()`: Displays the neighbors for each node.
  
- **Position Management:**  
  - `setA(pos)`, `setT(pos)`, and `setC(pos)` to set the agent, target, and check positions respectively.
  - `printA()`, `printT()`, `printC()`: Print current positions of the agent, target, and check position.
  - `clearAT()`: Resets the positions of the target and agent.

- **Agent Implementations:**  
  The graph class defines several methods for different agent strategies:
  - **Agent 0:**  
    - `agent0()` selects a random starting position for the agent.
    - `agent0_main(t_pos)` runs the random-walk strategy where the target moves randomly until it is caught.
  - **Agent 1:**  
    - `agent1_main(t_pos)` uses BFS to determine the agent's next move.
  - **Agent 2:**  
    - `agent2_main(t_pos)` uses DFS to plan the pursuit path.
  - **Agent 3:**  
    - `agent3_main(t_pos)` is similar to Agent 0 with extra messaging.
  - **Agent 4 & Agent 5:**  
    - `agent4_main()` and `agent5_main()` use probability estimates to determine which neighboring node is most likely to lead to the target.
    - Additional helper functions update and normalize probability estimates.
  - **Agent 6 & Agent 7:**  
    - `agent6_main()` and `agent7_main()` combine BFS search with probability-based adjustments for more informed movement.
  
- **Search Algorithms:**  
  - The code includes custom implementations of BFS (`bfs`, `bfs_agent6`, `bfs_agent7`) and DFS (`DFS`) to find paths between nodes.
  
- **Testing and Simulation:**  
  At the end of the file, a test loop runs one of the agent methods repeatedly (e.g., Agent 2) and collects the number of steps taken to catch the target. It then prints the average number of steps and standard deviation.

---

## How to Run

1. **Clone or Download the Repository:**  
   Place the code file (e.g., `res34_imageClassification.ipynb` for image classification or this simulation file for pursuit) in your working directory.

2. **Run the Code:**  
   Execute the script in your Python environment. You can run the file directly from the command line:
   ```bash
   python your_script.py
