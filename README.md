# Game solver
Python implementation of reachability/safety game solver as well as weak parity and strong parity game solver.

## Description
This project allows to solve a game provided by the user in the PGSolver file format.
The report associated to this project, explaining in details the algorithms used can be found at [link] (in french).

## Structure
The source code of the project can be found in src/be/ac/umons

    .
    ├── solver.py   #Console user interface (allowing to solve a game or test performances)
    ├── graph.py    #Game graph implementation
    ├── solvers     #Solving algorithms implementation for reachability, weak parity and strong parity games
    ├── benchmarks  #Benchmarking functions used for performance testing
    ├── operations  #Several general-purpose functions (file handling, generating games,ect.)
    └── test        #Tests

## How to run
To solve a reachability game : 
solver.py -r PLAYER TARGET_SET solve -i INPUTFILE [-o OUTPUTFILE]

To solve a weak parity game :
solver.py -wp solve -i INPUTFILE [-o OUTPUTFILE]

To solve a strong parity game :
solver.py -sp solve -i INPUTFILE [-o OUTPUTFILE]
