# coding=utf-8
import argparse
from subprocess import call
from benchmarks import reachability_benchmark as r_bench
from solvers import reachability, weakParity, strongParity
from tools import fileHandler as tools
from tools import generators


def command_line_handler():
    """
    This function parses the arguments given in the command line using python's argparse module. A special format of
    command has been chosen and can be viewed by running "python solver.py -h".
    :return: A Namespace containing the arguments and their values.
    """
    parser = argparse.ArgumentParser(description='Parity and reachability game solver')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', type=str, action='store', dest='target', nargs=2,
                       help='Reachability games (supply target set)', metavar=('PLAYER', 'TARGET'))
    group.add_argument('-wp', action='store_true', help='Weak parity games')
    group.add_argument('-sp', action='store_true', help='Strong parity games')

    subparsers = parser.add_subparsers(title='Solving modes', description='This program can solve a given game in dot '
                                                                          'format (solve) or benchmark the selected '
                                                                          'algorithm (benchmark) '
                                       , help='solve or benchmark', dest='mode')

    # create the parser for the "solve" command
    parser_solve = subparsers.add_parser('solve', help='Solve a game')
    parser_solve.add_argument('-i', required=True, type=str, action='store', dest='inputFile', help='Input file')
    parser_solve.add_argument('-o', required=False, type=str, action='store', dest='outputFile', help='Output file')

    # create the parser for the "benchmark" command
    parser_benchmark = subparsers.add_parser('bench', help='Benchmark selected algorithm')
    parser_benchmark.add_argument('-iter', required=True, type=int, action='store', dest='n',
                                  help='Number of iterations')

    return parser.parse_args()


def get_solver(args):
    """
    Determines the solving function to be used by the program depending on the game type
    :param args: the Namespace given by the parser
    :return: the corresponding solving function
    """
    if args.target is not None:
        return reachability.reachability_solver
    elif args.wp:
        return None  # placeholder for weak parity solver
    else:
        return None  # placeholder for strong parity solver


def solver():
    """
    Takes appropriate actions according to the chosen options (using command_line_handler() output).
    """

    # Parsing the command line arguments
    args = command_line_handler()

    # Solving mode
    if args.mode == "solve":
        g = tools.load_from_file(args.inputFile)  # loading game

        # Reachability
        if args.target is not None:
            player = int(args.target[0])  # getting player (as int)
            target = map(int, args.target[1].split(","))  # getting targets (transforming them into ints)
            solution = reachability.reachability_solver(g, target,
                                                        player)  # calling reachability solver on the game

        # Weak parity
        elif args.wp:
            solution = weakParity.weakParity_solver(g)  # calling weak parity solver on the game
        else:
            solution = strongParity.strongparity_solver(g)  # calling weak parity solver on the game

        # If output option chosen
        if args.outputFile is not None:
            # TODO this needs to be changed to a writing function that takes a solution as argument
            g.regions = solution[0]
            g.strategies = solution[1]
            tools.write_solution_to_file(g, args.outputFile + "_sol.dot")
            # TODO remove : generated for testing
            call(["neato", "-Tpdf", args.outputFile + "_sol.dot", "-o", args.outputFile + "_sol.pdf"])

    # Benchmark mode
    elif args.mode == "bench":
        iter = args.n

        # Reachability
        if args.target is not None:
            output_array = u"Générateur".center(30)+"|"+u"Noeuds (n)".center(12)+"|"+"Arcs (m)".center(10)+"|"\
                       +u"Atteignabilité (joueur 1)".center(28)+"|"+u"Atteignabilité (joueur 2)".center(28)+"\n"+\
                           "-"*108+"\n"
            output_array+= r_bench.benchmark_complete_graph(iter,[1],plot=True)
            output_array += r_bench.benchmark_worstcase_graph(iter,[1],plot=True)
            print output_array
        # Weak parity
        elif args.wp:
            pass  # bench wp
        else:
            pass  # bench sp

solver()
