# coding=utf-8
import argparse
from benchmarks import reachability_benchmark as r_bench
from benchmarks import strongparity_benchmark as sp_bench
from benchmarks import weakparity_benchmark as wp_bench
from solvers import reachability, weakparity, strongparity, generalizedparity
from tools import file_handler as tools
from tools import generators
from tools import operations as ops
from test import strongparity_test as sp_test
from test import weakparity_test as wp_test
from test import reachability_test as r_test
from test import generalizedparity_test as gp_test



def command_line_handler():
    """
    This function parses the arguments given in the command line using python's argparse module. A special format of
    command has been chosen and can be viewed by running "python solver.py -h".
    :return: A Namespace containing the arguments and their values.
    """
    parser = argparse.ArgumentParser(description='GameSolver: a python implementation of game theory algorithms.')

    subparsers = parser.add_subparsers(title='Mode selection',
                                       description='This tool implements algorithms used to solve reachability/safety, '
                                                   'parity, weak parity and generalized parity games. '
                                                   'This program can solve a game given in the PGSolver format (solve),  '
                                                   'benchmark one of the implemented algorithms (bench) or run unit tests (test).',
                                       help='Solve a game, benchmark an algorithm or run tests.', dest='mode')

    # create the parser for the "solve" command
    parser_solve = subparsers.add_parser('solve', help='Solve a game')

    # adding the game options (mutually exclusive and required)
    group_solve = parser_solve.add_mutually_exclusive_group(required=True)
    group_solve.add_argument('-r', type=str, action='store', dest='target', nargs=2,
                             help='Solve a reachability game for a PLAYER and a TARGET_SET', metavar=('PLAYER', 'TARGET_SET'))
    group_solve.add_argument('-s', type=str, action='store', dest='safe', nargs = 1,
                             help='Solve a safety game with SAFE_SET for player 1', metavar=('SAFE_SET'))
    group_solve.add_argument('-wp', action='store_true', help='Solve a weak parity game')
    group_solve.add_argument('-sp',action='store', choices=['recursive', 'safety', 'antichain'],
                             dest='parity_algorithm', help='Solve a strong parity game')
    group_solve.add_argument('-gp', action='store_true', help='Solve a generalized parity game')

    parser_solve.add_argument('-i', required=True, type=str, action='store', dest='inputFile',
                              help='Path to the arena of the game to solve')
    parser_solve.add_argument('-o', required=False, type=str, action='store', dest='outputFile',
                              help='Path to the file in which to save the solution')

    # create the parser for the "benchmark" command
    parser_benchmark = subparsers.add_parser('bench', help='Benchmark selected algorithm')
    # adding the game options (mutually exclusive and required)
    group_bench = parser_benchmark.add_mutually_exclusive_group(required=True)
    group_bench.add_argument('-r', action='store', choices=['complete0', 'complete1', 'worstcase'],
                             dest='reachability_type', help='Benchmark the reachability algorithm')
    group_bench.add_argument('-wp', action='store', choices=['complete', 'worstcase'],
                             dest='weakparity_type', help='Benchmark the weak parity algorithm')
    group_bench.add_argument('-gp', action='store_true', help='Benchmark the generalized parity algorithm')

    parser_benchmark.add_argument('-max', required=True, type=int, action='store', dest='max',
                                  help='Maximum size of tested graph')
    parser_benchmark.add_argument('-step', required=True, type=int, action='store', dest='step',
                                  help='Step used in the benchmark (if 1 : test all graphs of size 1 to max)')
    parser_benchmark.add_argument('-rep', required=True, type=int, action='store', dest='repetitions',
                                  help='The number of times to compute solving time for a given size (to avoid time spikes due to system load)')
    parser_benchmark.add_argument('-plot', required=False, type=str, action='store', dest='outputPlot',
                                  help='Path to the file in which to save the plot')

    # create the parser for the "test" command
    parser_test = subparsers.add_parser('test', help='Runs all tests')

    return parser.parse_args()


def solver():
    """
    Takes appropriate actions according to the chosen options (using command_line_handler() output).
    """

    # Parsing the command line arguments
    args = command_line_handler()

    if args.mode == "solve":

        """ ----- Solving mode ----- """
        if args.gp:
            g = tools.load_generalized_from_file(args.inputFile)  # we have a generalized parity game arena
        else:
            g = tools.load_from_file(args.inputFile)  # loading game from the input file
        player = 0  # default player is 0, so solution comes as (W_0,sigma_0), (W_1,sigma_1) or (W_0, W_1)

        # Reachability (target and player is set)
        if args.target is not None:
            player = int(args.target[0])  # getting player (as int), replacing default player
            target = map(int, args.target[1].split(","))  # getting node ids in target (transforming them into int)
            solution = reachability.reachability_solver(g, target, player)  # calling reachability solver
            ops.print_solution(solution, player)  # printing the solution

        # Safety (safe set provided)
        if args.safe is not None:
            player = 1 # the player with the reachability objective (to write the solution later)
            safe_set = map(int, args.safe[0].split(","))  # getting node ids in safe set (transforming them into int)
            target_set = []
            # adds every node not in the safe set to the target set
            for node in g.get_nodes():
                if not (node in safe_set):
                    target_set.append(node)
            # the solution comes out as (W_1,sigma_1), (W_0,sigma_0)
            solution = reachability.reachability_solver(g, target_set, 1)  # calling reachability solver with target set for player 1 (2)
            ops.print_solution(solution, 1)  # printing the solution, player 1 (2) has the reachability objective

        # Weak parity
        elif args.wp:
            solution = weakparity.weak_parity_solver(g)  # calling weak parity solver on the game
            ops.print_solution(solution, player)  # printing the solution

        # Strong parity (an algorithm is chosen)
        elif args.parity_algorithm is not None:
            if (args.parity_algorithm == 'recursive'):
                solution = strongparity.strong_parity_solver(g)  # calling recursive algorithm for parity games
                ops.print_solution(solution, player)  # printing the solution (with strategy)
            elif (args.parity_algorithm == 'safety'):
                solution = strongparity.reduction_to_safety_parity_solver(g)  # calling reduction to safety algorithm
                ops.print_winning_regions(solution[0], solution[1]) # printing the solution (without strategy)
            elif (args.parity_algorithm == 'antichain'):
                # calling antichain-based algorithm, assumes indexes start with 1
                solution = strongparity.strong_parity_antichain_based(g,1)
                ops.print_winning_regions(solution[0], solution[1]) # printing the solution (without strategy)
            else:
                # this should not happen
                solution = None

        # Generalized parity
        elif args.gp:
            solution = generalizedparity.generalized_parity_solver(g)  # calling classical algorithm for generalized parity games
            ops.print_winning_regions(solution[0], solution[1])  # printing the solution (without strategy)

        # If output option is chosen and the algorithm is the classical algo for generalized parity games, use special
        # function dedicated to writing solution of generalized parity games (need to consider several priorities)
        if (args.outputFile is not None) and args.gp:
            tools.write_generalized_solution_to_file(g, solution[0], solution[1], args.outputFile)

        # If output option is chosen and the algorithm is the reduction to safety algorithm for parity games or the
        # antichain-based algorithm for parity games then the output is only the winning regions, not the strategies
        elif (args.outputFile is not None) and (args.parity_algorithm == 'safety' or args.parity_algorithm == 'antichain'):
            tools.write_solution_to_file_no_strategies(g, solution[0], solution[1], args.outputFile)

        # Else the regular regions + strategies are output
        elif args.outputFile is not None:
            tools.write_solution_to_file(g, solution, player, args.outputFile)

    elif args.mode == "bench":
        """ ----- Benchmark mode ----- """
        max = args.max
        step = args.step
        rep = args.repetitions
        plot = args.outputPlot is not None

        # Reachability
        if args.reachability_type is not None:
            if args.reachability_type == 'complete0':
                r_bench.benchmark(max, generators.complete_graph, [1], 0, iterations=rep, step=step, plot=plot,
                                  regression=True, order=2, path=args.outputPlot,
                                  title=u"Graphes complets de taille 1 à " + str(max))
            elif args.reachability_type == 'complete1':
                r_bench.benchmark(max, generators.complete_graph, [1], 1, iterations=rep, step=step, plot=plot,
                                  regression=True, order=2, path=args.outputPlot,
                                  title=u"Graphes complets de taille 1 à " + str(max))
            elif args.reachability_type == 'worstcase':
                r_bench.benchmark(max, generators.reachability_worst_case, [1], 0, iterations=rep, step=step,
                                  plot=plot, regression=True, order=2, path=args.outputPlot,
                                  title=u"Graphes 'pire cas' de taille 1 à " + str(max))

        # Weak parity
        elif args.weakparity_type is not None:
            if args.weakparity_type == 'complete':
                wp_bench.benchmark(max, generators.complete_graph_weakparity, iterations=rep, step=step, plot=plot,
                                   regression=True, order=2, path=args.outputPlot,
                                   title=u"Graphes complets de taille 1 à " + str(max))
            elif args.weakparity_type == 'worstcase':
                wp_bench.benchmark(max, generators.weak_parity_worst_case, iterations=rep, step=step, plot=plot,
                                   regression=True, order=3, path=args.outputPlot,
                                   title=u"Graphes 'pire cas' de taille 1 à " + str(max))

        # Strong parity
        else:
            sp_bench.benchmark_worst_case(max, iterations=rep, step=step, plot=plot, path=args.outputPlot)

    elif args.mode == "test":
        sp_test_result = sp_test.launch_tests()
        wp_test_result = wp_test.launch_tests()
        r_test_result = r_test.launch_tests()
        gp_test_result = gp_test.launch_tests()
        if (sp_test_result and wp_test_result and r_test_result and gp_test_result):
            print "All tests passed with success"
        else:
            print "Some tests failed"


solver()
