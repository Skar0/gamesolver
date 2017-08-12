# coding=utf-8
import argparse
from subprocess import call
from benchmarks import reachability_benchmark as r_bench
from benchmarks import strongParity_benchmark as sp_bench
from solvers import reachability, weakParity, strongParity
from tools import fileHandler as tools
from tools import generators
from tools import operations as ops


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
    parser_solve.add_argument('-i', required=True, type=str, action='store', dest='inputFile', help='Input path for the arena file')
    parser_solve.add_argument('-o', required=False, type=str, action='store', dest='outputFile', help='Output path for the solution')

    # create the parser for the "benchmark" command
    parser_benchmark = subparsers.add_parser('bench', help='Benchmark selected algorithm')
    parser_benchmark.add_argument('-n', required=True, type=int, action='store', dest='n',
                                  help='Number of iterations')
    parser_benchmark.add_argument('-step', required=True, type=int, action='store', dest='s',
                                  help='Steps taken by the benchmarker (1 = test all sizes from 1 to iter)')
    parser_benchmark.add_argument('-plot', required=False, type=str, action='store', dest='outputPlot', help='Output path for the plot')

    return parser.parse_args()


def solver():
    """
    Takes appropriate actions according to the chosen options (using command_line_handler() output).
    """

    # Parsing the command line arguments
    args = command_line_handler()

    if args.mode == "solve":
        """ ----- Solving mode ----- """
        g = tools.load_from_file(args.inputFile)  # loading game from the input file
        player = 0 # default player is 0, so solution comes as (W_0,sigma_0), (W_1,sigma_1)

        # Reachability (target and player is set)
        if args.target is not None:
            player = int(args.target[0])  # getting player (as int)
            target = map(int, args.target[1].split(","))  # getting targets (transforming them into ints)
            solution = reachability.reachability_solver_tuples(g, target,
                                                        player)  # calling reachability solver on the game
            ops.print_solution(solution,player)


        # Weak parity
        elif args.wp:
            solution = weakParity.weak_parity_solver(g)  # calling weak parity solver on the game
            ops.print_solution(solution,player)

        # Strong parity
        else:
            solution = strongParity.strongparity_solver2(g)  # calling weak parity solver on the game
            ops.print_solution(solution, player)

        # If output option chosen
        if args.outputFile is not None:
            tools.write_solution_to_file(g, solution, player, args.outputFile)

    elif args.mode == "bench":
        """ ----- Benchmark mode ----- """
        iter = args.n
        isPlot = args.outputPlot is not None

        # Reachability
        if args.target is not None:
            print u"Générateur".center(30)+"|"+u"Noeuds (n)".center(12)+"|"+"Arcs (m)".center(10)+"|"\
                       +u"Atteignabilité (joueur 1)".center(28)+"|"+u"Atteignabilité (joueur 2)".center(28)+"\n"+\
                           "-"*108+"\n"
            r_bench.benchmark(iter, generators.complete_graph2, [1], 1, iterations=3, plot=True,order=1,regression=True, step=100)

        # Weak parity
        elif args.wp:
            pass  # bench wp
        else:
            pass  # bench sp

solver()
