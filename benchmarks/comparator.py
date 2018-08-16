import copy

from tools import timer, generators, optimizations
import matplotlib.pyplot as plt
import solvers.strongparity as sp
import solvers.weakparity as wp

import solvers.generalizedparity as gp
from tools.operations import transform_graph_into_c_spec, are_lists_equal,transform_graph_into_c

"""
This module contains functions used to compare our algorithms
"""
def compare_algorithms2(algo1, algo2, generator, n, preprocess1=None, preprocess2=None, iterations=3, step=10, plot=False, path="", title="Comparison", label1="Algorithm 1", label2="Algorithm2"):
    """
            Benchmarks the recursive algorithm for strong parity games using the worst case generator which yields an
            exponential complexity. Calls strong parity solver on games generated using the worst case generator function.
            Games of size 5 to 5*n are solved and a timer records the time taken to get the solution.The solver can be timed
            several times and the minimum value is selected using optional parameter iterations (to avoid recording time
            spikes and delays due to system load). The result can be plotted using matplotlib.
            :param n: number of nodes in generated graph (nodes is 5*n due to construction).
            :param iterations: number of times the algorithm is timed (default is 3).
            :param step: step to be taken in the generation.
            :param plot: if True, plots the data using matplotlib.
            :param path: path to the file in which to write the result.
            """

    y1 = []  # list for the time recordings of algorithm 1
    n1 = []  # list for the x values of algorithm 1
    y2 = []  # list for the time recordings of algorithm 2
    n2 = []  # list for the x values of algorithm 2

    chrono = timer.Timer(verbose=False)  # Timer object

    # games generated are size 1 to n
    for i in range(5, n, step):
        temp1 = []  # temp list for #iterations recordings of algorithm 1
        g1 = generator(i) # game generation
        g2 = copy.deepcopy(g1)

        if preprocess1 is not None:
            g1 = preprocess1(g1)
        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                solution_regular = algo1(g1,0)
            temp1.append(chrono.interval)  # add time recording

        min_recording = min(temp1)
        y1.append(min_recording)  # get the minimum out of #iterations recordings
        n1.append(i)

        if preprocess2 is not None:
            g2 = preprocess2(g2)

        temp2 = []
        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                #algo2(u[0],u[1],u[2],u[3])  # solver call
                solution_symbolic = algo2(g2,0)
            temp2.append(chrono.interval)  # add time recording

        min_recording = min(temp2)
        y2.append(min_recording)  # get the minimum out of #iterations recordings
        n2.append(i)


    if plot:
        plt.grid(True)
        plt.title(title)
        plt.xlabel(u'number of nodes')
        plt.ylabel(u'time')

        # plt.yscale("log") allows logatithmic y-axis
        points, = plt.plot(n1, y1, 'g.', label=label1)
        points2, = plt.plot(n2, y2, 'r.', label=label2)

        plt.legend(loc='upper left', handles=[points, points2])
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()

def compare_algorithms3(algo1, algo2, algo3, generator, n, preprocess1=None, preprocess2=None, preprocess3=None, iterations=3, step=10, plot=False, path="", title="Comparison", label1="Algorithm 1", label2="Algorithm2", label3="Algorithm3"):
    """
            Benchmarks the recursive algorithm for strong parity games using the worst case generator which yields an
            exponential complexity. Calls strong parity solver on games generated using the worst case generator function.
            Games of size 5 to 5*n are solved and a timer records the time taken to get the solution.The solver can be timed
            several times and the minimum value is selected using optional parameter iterations (to avoid recording time
            spikes and delays due to system load). The result can be plotted using matplotlib.
            :param n: number of nodes in generated graph (nodes is 5*n due to construction).
            :param iterations: number of times the algorithm is timed (default is 3).
            :param step: step to be taken in the generation.
            :param plot: if True, plots the data using matplotlib.
            :param path: path to the file in which to write the result.
            """

    y1 = []  # list for the time recordings of algorithm 1
    n1 = []  # list for the x values of algorithm 1
    y2 = []  # list for the time recordings of algorithm 2
    n2 = []  # list for the x values of algorithm 2
    y3 = []  # list for the time recordings of algorithm 3
    n3 = []  # list for the x values of algorithm 3

    chrono = timer.Timer(verbose=False)  # Timer object

    # games generated are size 1 to n
    for i in range(5, n, step):
        temp1 = []  # temp list for #iterations recordings of algorithm 1
        g1 = generator(i) # game generation
        g2 = copy.deepcopy(g1)
        g3 = copy.deepcopy(g1)

        if preprocess1 is not None:
            g1 = preprocess1(g1)

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                solution_regular = algo1(g1)
            temp1.append(chrono.interval)  # add time recording

        min_recording = min(temp1)
        y1.append(min_recording)  # get the minimum out of #iterations recordings
        n1.append(i)

        if preprocess2 is not None:
            g2 = preprocess2(g2)

        g2, nbr_nodes = transform_graph_into_c_spec(g2)

        temp2 = []
        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                #algo2(u[0],u[1],u[2],u[3])  # solver call
                solution_symbolic = algo2(g2, nbr_nodes,0)
            temp2.append(chrono.interval)  # add time recording

        min_recording = min(temp2)
        y2.append(min_recording)  # get the minimum out of #iterations recordings
        n2.append(i)

        temp3 = []  # temp list for #iterations recordings of algorithm 1
        if preprocess3 is not None:
            g3 = preprocess3(g3)
        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                solution_third = algo3(g3)
            temp3.append(chrono.interval)  # add time recording

        min_recording = min(temp3)
        y3.append(min_recording)  # get the minimum out of #iterations recordings
        n3.append(i)

        #print("symb "+str(solution_symbolic[0])+" "+str(solution_symbolic[1]))
        #print("reg  "+str(solution_regular[0])+" "+str(solution_regular[1]))


    if plot:
        plt.grid(True)
        plt.title(title)
        plt.xlabel(u'number of nodes')
        plt.ylabel(u'time')

        # plt.yscale("log") allows logatithmic y-axis
        points, = plt.plot(n1, y1, 'g.', label=label1)
        points2, = plt.plot(n2, y2, 'r.', label=label2)
        points3, = plt.plot(n3, y3, 'b.', label=label3)

        plt.legend(loc='upper left', handles=[points, points2, points3])
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()

def compare_algorithms(algo1, algo2, generator, n, preprocess1=None, preprocess2=None, iterations=3, step=10, plot=False, path="", title="Comparison", label1="Algorithm 1", label2="Algorithm2"):
    """
            Benchmarks the recursive algorithm for strong parity games using the worst case generator which yields an
            exponential complexity. Calls strong parity solver on games generated using the worst case generator function.
            Games of size 5 to 5*n are solved and a timer records the time taken to get the solution.The solver can be timed
            several times and the minimum value is selected using optional parameter iterations (to avoid recording time
            spikes and delays due to system load). The result can be plotted using matplotlib.
            :param n: number of nodes in generated graph (nodes is 5*n due to construction).
            :param iterations: number of times the algorithm is timed (default is 3).
            :param step: step to be taken in the generation.
            :param plot: if True, plots the data using matplotlib.
            :param path: path to the file in which to write the result.
            """

    y1 = []  # list for the time recordings of algorithm 1
    n1 = []  # list for the x values of algorithm 1
    y2 = []  # list for the time recordings of algorithm 2
    n2 = []  # list for the x values of algorithm 2

    chrono = timer.Timer(verbose=False)  # Timer object

    # games generated are size 1 to n
    for i in range(5, n, step):
        temp1 = []  # temp list for #iterations recordings of algorithm 1
        g1 = generator(i) # game generation
        g2 = copy.deepcopy(g1)

        if preprocess1 is not None:
            g1 = preprocess1(g1)

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                algo1(g1)  # solver call
            temp1.append(chrono.interval)  # add time recording

        min_recording = min(temp1)
        y1.append(min_recording)  # get the minimum out of #iterations recordings
        n1.append(i)

        if preprocess2 is not None:
            g2 = preprocess2(g2)

        temp2 = []
        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                #algo2(u[0],u[1],u[2],u[3])  # solver call
                algo2(g2)
            temp2.append(chrono.interval)  # add time recording

        min_recording = min(temp2)
        y2.append(min_recording)  # get the minimum out of #iterations recordings
        n2.append(i)
        print(i)

    if plot:
        plt.grid(True)
        plt.title(title)
        plt.xlabel(u'number of nodes')
        plt.ylabel(u'time')

        # plt.yscale("log") allows logatithmic y-axis
        points, = plt.plot(n1, y1, 'g.', label=label1)
        points2, = plt.plot(n2, y2, 'r.', label=label2)

        plt.legend(loc='upper left', handles=[points, points2])
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()

def compare_algorithms4(algo1, algo2, generator, n, preprocess1=None, preprocess2=None, iterations=3, step=10, plot=False, path="", title="Comparison", label1="Algorithm 1", label2="Algorithm2"):
    """
            Benchmarks the recursive algorithm for strong parity games using the worst case generator which yields an
            exponential complexity. Calls strong parity solver on games generated using the worst case generator function.
            Games of size 5 to 5*n are solved and a timer records the time taken to get the solution.The solver can be timed
            several times and the minimum value is selected using optional parameter iterations (to avoid recording time
            spikes and delays due to system load). The result can be plotted using matplotlib.
            :param n: number of nodes in generated graph (nodes is 5*n due to construction).
            :param iterations: number of times the algorithm is timed (default is 3).
            :param step: step to be taken in the generation.
            :param plot: if True, plots the data using matplotlib.
            :param path: path to the file in which to write the result.
            """

    y1 = []  # list for the time recordings of algorithm 1
    n1 = []  # list for the x values of algorithm 1
    y2 = []  # list for the time recordings of algorithm 2
    n2 = []  # list for the x values of algorithm 2

    chrono = timer.Timer(verbose=False)  # Timer object

    # games generated are size 1 to n
    for i in range(5, n, step):
        temp1 = []  # temp list for #iterations recordings of algorithm 1
        g1 = generator(i) # game generation
        g2 = copy.deepcopy(g1)

        if preprocess1 is not None:
            g1 = preprocess1(g1)

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                algo1(g1)  # solver call
            temp1.append(chrono.interval)  # add time recording

        min_recording = min(temp1)
        y1.append(min_recording)  # get the minimum out of #iterations recordings
        n1.append(i)

        if preprocess2 is not None:
            g2 = preprocess2(g2)

        temp2 = []
        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                #algo2(u[0],u[1],u[2],u[3])  # solver call
                algo2(g2,0)
            temp2.append(chrono.interval)  # add time recording

        min_recording = min(temp2)
        y2.append(min_recording)  # get the minimum out of #iterations recordings
        n2.append(i)
        print(i)

    if plot:
        plt.grid(True)
        plt.title(title)
        plt.xlabel(u'number of nodes')
        plt.ylabel(u'time')

        # plt.yscale("log") allows logatithmic y-axis
        points, = plt.plot(n1, y1, 'g.', label=label1)
        points2, = plt.plot(n2, y2, 'r.', label=label2)

        plt.legend(loc='upper left', handles=[points, points2])
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()

def gen(i):
    return generators.random(i, i, 1, (i / 2))

#rand(sp.strong_parity_solver, gp.disj_parity_win2, gen, 800, iterations=5, step=10, plot=True, path="random-notransform-win2.png")
#rand(sp.strong_parity_solver, gp.disj_parity_win2, generators.ladder, 800, iterations=5, step=10, plot=True, path="ladder-notransform-win2.png")
#rand(sp.strong_parity_solver, gp.disj_parity_win2, generators.weak_parity_worst_case, 200, iterations=5, step=10, plot=True, path="weak-notransform-win2.png")

#rand(sp.strong_parity_solver, gp.disj_parity_win2, generators.strong_parity_worst_case, 15, iterations=3, step=1, plot=True, path="worst-notransform-win2.png")

#rand(sp.strong_parity_solver, sp.strong_parity_solver, gen, 800, iterations=5, step=10, plot=True, path="normalVScompressed-rand.pdf")

"""
compare_algorithms(wp.weak_parity_solver, wp.weak_parity_solver, gen, 1500, preprocess2=optimizations.compress_priorities, iterations=5
                   , step=10, plot=True, path="wp_random_normalVScompressed_n1500_it5_s10.pdf",
                   title="Weak parity solver runtime comparison (random graphs)", label1="Without compression", label2="With compression")

compare_algorithms(wp.weak_parity_solver, wp.weak_parity_solver, generators.weak_parity_worst_case, 400, preprocess2=optimizations.compress_priorities, iterations=5
                   , step=10, plot=True, path="wp_wors-case_normalVScompressed_n400_it5_s10.pdf",
                   title="Weak parity solver runtime comparison (worst-case graphs)", label1="Without compression", label2="With compression")

compare_algorithms(sp.strong_parity_solver, sp.strong_parity_solver, gen, 2000, preprocess2=optimizations.compress_priorities, iterations=5
                   , step=10, plot=True, path="sp_random_normalVScompressed_n2000_it5_s10.pdf",
                   title="Recursive algorithm runtime comparison (random graphs)", label1="Without compression", label2="With compression")

compare_algorithms(sp.strong_parity_solver, sp.strong_parity_solver, generators.ladder, 2000, preprocess2=optimizations.compress_priorities, iterations=5
                   , step=10, plot=True, path="sp_ladder_normalVScompressed_n2000_it5_s10.pdf",
                   title="Recursive algorithm runtime comparison (ladder graphs)", label1="Without compression", label2="With compression")

compare_algorithms(sp.strong_parity_solver, sp.strong_parity_solver, generators.weak_parity_worst_case, 2000, preprocess2=optimizations.compress_priorities, iterations=5
                   , step=10, plot=True, path="sp_wp-worst-case_normalVScompressed_n2000_it5_s10.pdf",
                   title="Recursive algorithm runtime comparison (sparce priorities graphs)", label1="Without compression", label2="With compression")

compare_algorithms(sp.strong_parity_solver, sp.strong_parity_solver, generators.strong_parity_worst_case, 15, preprocess2=optimizations.compress_priorities, iterations=5
                   , step=10, plot=True, path="sp_worst-case_normalVScompressed_n20_it5_s10.pdf",
                   title="Recursive algorithm runtime comparison (worst-case graphs)", label1="Without compression", label2="With compression")
"""


#compare_algorithms3(sp.strong_parity_solver, sp.symbolic_strong_parity_solver, sp.reduction_to_safety_parity_solver, generators.strong_parity_worst_case, 30, preprocess2=optimizations.compress_priorities, iterations=3
#                   , step=1, plot=True, path="COMPARE3-RANDOM-200n-1s-noopt.pdf",
#                   title="Parity game algorithms runtime comparison (random graphs)", label1="Recursive", label2="Antichain-based", label3="Reduction to safety")


#compare_algorithms2(sp.strong_parity_solver_no_strategies, sp.symbolic_strong_parity_solver,gen, 100, iterations=3
                   #, step=10, plot=True, path="sp_symbolicVSnormal_n500_it3_step10_RAN.pdf",
                  # title="Recursive vs symbolic algorithm runtime comparison (random graphs)", label1="Recursive solver", label2="Symbolic solver")
"""
# Compare strong parity recursive vs symbolic vs reuction on ladder with no opti
compare_algorithms3(sp.strong_parity_solver_no_strategies, sp.symbolic_strong_parity_solver, sp.reduction_to_safety_parity_solver,generators.ladder, 250, iterations=3
                   , step=10, plot=True, path="COMPARE3-LADDER-250n-10s-noopt.pdf",
                   title="Parity game algorithms runtime comparison (ladder graphs)", label1="Recursive", label2="Antichain-based", label3="Reduction to safety")
# Compare strong parity recursive vs symbolic vs reuction on ladder with compression
compare_algorithms3(sp.strong_parity_solver_no_strategies, sp.symbolic_strong_parity_solver, sp.reduction_to_safety_parity_solver,generators.ladder, 250,preprocess1=optimizations.compress_priorities,preprocess2=optimizations.compress_priorities, preprocess3=optimizations.compress_priorities, iterations=3
                   , step=10, plot=True, path="COMPARE3-LADDER-250n-10s-compress.pdf",
                   title="Parity game algorithms runtime comparison (ladder graphs + compression)", label1="Recursive", label2="Antichain-based", label3="Reduction to safety")

# Compare strong parity recursive vs symbolic vs reuction on worst with no opti
compare_algorithms3(sp.strong_parity_solver_no_strategies, sp.symbolic_strong_parity_solver, sp.reduction_to_safety_parity_solver,generators.strong_parity_worst_case, 20, iterations=3
                   , step=1, plot=True, path="COMPARE3-WORST-20n-1s-noopt.pdf",
                   title="Parity game algorithms runtime comparison (worst-case graphs)", label1="Recursive", label2="Antichain-based", label3="Reduction to safety")
# Compare strong parity recursive vs symbolic vs reuction on worst with compression
compare_algorithms3(sp.strong_parity_solver_no_strategies, sp.symbolic_strong_parity_solver, sp.reduction_to_safety_parity_solver,generators.strong_parity_worst_case, 20,preprocess1=optimizations.compress_priorities,preprocess2=optimizations.compress_priorities, preprocess3=optimizations.compress_priorities, iterations=3
                   , step=1, plot=True, path="COMPARE3-WORST-20n-1s-compress.pdf",
                   title="Parity game algorithms runtime comparison (wost-case graphs + compression)", label1="Recursive", label2="Antichain-based", label3="Reduction to safety")


#compare_algorithms2(sp.strong_parity_solver_no_strategies, sp.symbolic_strong_parity_solver, generators.ladder, 2000, preprocess2=optimizations.compress_priorities, iterations=5
                  # , step=10, plot=True, path="sp_ladder_normalVScompressed_n2000_it5_s10.pdf",
                  # title="Recursive algorithm runtime comparison (ladder graphs)", label1="Without compression", label2="With compression")

# Compare strong parity recursive vs symbolic vs reuction on random with no opti
compare_algorithms3(sp.strong_parity_solver_no_strategies, sp.symbolic_strong_parity_solver, sp.reduction_to_safety_parity_solver, gen, 30, iterations=3
                   , step=1, plot=True, path="COMPARE3-RANDOM-30n-1s-noopt.pdf",
                   title="Parity game algorithms runtime comparison (random graphs)", label1="Recursive", label2="Antichain-based", label3="Reduction to safety")

# Compare strong parity recursive vs symbolic vs reuction on random with compression 
compare_algorithms3(sp.strong_parity_solver_no_strategies, sp.symbolic_strong_parity_solver, sp.reduction_to_safety_parity_solver, gen, 30,preprocess1=optimizations.compress_priorities,preprocess2=optimizations.compress_priorities, preprocess3=optimizations.compress_priorities,
 iterations=3
                   , step=1, plot=True, path="COMPARE3-RANDOM-30n-1s-compress.pdf",
                   title="Parity game algorithms runtime comparison (random graphs + compression)", label1="Recursive", label2="Antichain-based", label3="Reduction to safety")

# Compare strong parity recursive vs symbolic vs reuction on worst case with no opti
compare_algorithms3(sp.strong_parity_solver_no_strategies, sp.symbolic_strong_parity_solver, sp.reduction_to_safety_parity_solver, generators.strong_parity_worst_case, 20, iterations=3
                   , step=1, plot=True, path="COMPARE3-WORST-20n-1s-noopt.pdf",
                   title="Parity game algorithms runtime comparison (worst-case graphs)", label1="Recursive", label2="Antichain-based", label3="Reduction to safety")
# Compare strong parity recursive vs symbolic vs reuction on worst case with compression
compare_algorithms3(sp.strong_parity_solver_no_strategies, sp.symbolic_strong_parity_solver, sp.reduction_to_safety_parity_solver,generators.strong_parity_worst_case, 20,preprocess1=optimizations.compress_priorities,preprocess2=optimizations.compress_priorities, preprocess3=optimizations.compress_priorities,
                    iterations=3, step=1, plot=True, path="COMPARE3-WORST-20n-1s-compress.pdf",
                   title="Parity game algorithms runtime comparison (worst-case graphs + compression)", label1="Recursive", label2="Antichain-based", label3="Reduction to safety")

# Compare strong vs symb with and without compression on random

compare_algorithms4(sp.strong_parity_solver_no_strategies, sp.strong_parity_antichain_based,gen, 350, iterations=3
                   , step=10, plot=True, path="COMPARE-REC-ANTI-RAND-350n-10s-noopt.pdf",
                  title="Parity game algorithms runtime comparison (random graphs)", label1="Recursive", label2="Antichain-based")
compare_algorithms4(sp.strong_parity_solver_no_strategies, sp.strong_parity_antichain_based,gen, 350, iterations=3,preprocess1=optimizations.compress_priorities,preprocess2=optimizations.compress_priorities
                   , step=10, plot=True, path="COMPARE-REC-ANTI-RAND-350n-10s-opti.pdf",
                  title="Parity game algorithms runtime comparison (random graphs + compression)", label1="Recursive", label2="Antichain-based")


# Compare strong vs symb with and without compression on ladder
compare_algorithms4(sp.strong_parity_solver_no_strategies, sp.strong_parity_antichain_based,generators.ladder, 300, iterations=3
                   , step=10, plot=True, path="COMPARE-REC-ANTI-LADDER-300n-10s-noopt.pdf",
                  title="Parity game algorithms runtime comparison (ladder graphs)", label1="Recursive", label2="Antichain-based")
compare_algorithms4(sp.strong_parity_solver_no_strategies, sp.strong_parity_antichain_based,generators.ladder, 300, iterations=3,preprocess1=optimizations.compress_priorities,preprocess2=optimizations.compress_priorities
                   , step=10, plot=True, path="COMPARE-REC-ANTI-LADDER-300n-10s-opti.pdf",
                  title="Parity game algorithms runtime comparison (ladder graphs + compression)", label1="Recursive", label2="Antichain-based")

# Compare strong vs symb with and without compression on worst case
compare_algorithms4(sp.strong_parity_solver_no_strategies, sp.strong_parity_antichain_based,generators.strong_parity_worst_case, 20, iterations=3
                   , step=1, plot=True, path="COMPARE-REC-ANTI-WORST-20n-1s-noopt.pdf",
                  title="Parity game algorithms runtime comparison (worst-case graphs)", label1="Recursive", label2="Antichain-based")
compare_algorithms4(sp.strong_parity_solver_no_strategies, sp.strong_parity_antichain_based,generators.strong_parity_worst_case, 20, iterations=3,preprocess1=optimizations.compress_priorities,preprocess2=optimizations.compress_priorities
                   , step=1, plot=True, path="COMPARE-REC-ANTI-WORST-20n-1s-opti.pdf",
                  title="Parity game algorithms runtime comparison (worst-case graphs + compression)", label1="Recursive", label2="Antichain-based")



# Compare reduction vs symb with and without compression
compare_algorithms4(sp.reduction_to_safety_parity_solver, sp.strong_parity_antichain_based,gen, 25, iterations=3
                   , step=1, plot=True, path="COMPARE-RED-ANTI-RAND-25n-1s-noopt.pdf",
                  title="Parity game algorithms runtime comparison (random graphs)", label1="Reduction to safety", label2="Antichain-based")

compare_algorithms4(sp.reduction_to_safety_parity_solver, sp.strong_parity_antichain_based,gen, 25, iterations=3,preprocess1=optimizations.compress_priorities,preprocess2=optimizations.compress_priorities
                   , step=1, plot=True, path="COMPARE-RED-ANTI-RAND-25n-1s-opti.pdf",
                  title="Parity game algorithms runtime comparison (random graphs + compression)", label1="Reduction to safety", label2="Antichain-based")

# Compare symbolic no opt vs symb with sopt
compare_algorithms2(sp.strong_parity_antichain_based, sp.strong_parity_antichain_based,gen, 350, iterations=3,preprocess2=optimizations.compress_priorities
                   , step=10, plot=True, path="COMPARE-ANTI-ANTI-RAND-350n-10s-optsvsnoopt.pdf",
                  title="Antichain-based algorithm runtime comparison (random graphs)", label1="Without compression", label2="With compression")


# Compare recursive no opt vs recursive with opt
compare_algorithms(sp.strong_parity_solver_no_strategies, sp.strong_parity_solver_no_strategies,gen, 3000, iterations=3,preprocess2=optimizations.compress_priorities
                   , step=10, plot=True, path="COMPARE-REC-REC-RAND-3000n-10s-optsvsnoopt.pdf",
                  title="Recursive algorithm runtime comparison (random graphs)", label1="Without compression", label2="With compression")

# Compare recursive no opt vs recursive with opt
compare_algorithms(sp.strong_parity_solver_no_strategies, sp.strong_parity_solver_no_strategies,generators.strong_parity_worst_case, 25, iterations=3,preprocess2=optimizations.compress_priorities
                   , step=1, plot=True, path="COMPARE-REC-REC-WORST-25n-1s-optsvsnoopt.pdf",
                  title="Recursive algorithm runtime comparison (worst-case graphs)", label1="Without compression", label2="With compression")
"""