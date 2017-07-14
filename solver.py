import argparse
import reachability as reachability


def command_line_handler():
    parser = argparse.ArgumentParser(description='Parity and reachability game solver')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', action='store_true', help='Reachability games')
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
    if args.r:
        return reachability.reachabilitySolver()
    elif args.wp:
        return None  # placeholder for weak parity solver
    else:
        return None  # placeholder for strong parity solver


def solver():
    args = command_line_handler()
    solver = get_solver(args)

    if args.mode == "solve":
        try:
            f = open(args.inputFile, 'r')
        except IOError:
            raise
            # handle exception

            # load file

    elif args.mode == "bench":
        iterations = args.n
        pass
        # benchmark


solver()
