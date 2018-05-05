import copy

from tools import timer, generators, optimizations
import matplotlib.pyplot as plt
import solvers.strongparity as sp
import solvers.weakparity as wp

import solvers.generalizedparity as gp
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

def gen(i):
    return generators.random(i, i, 1, (i / 2))

#rand(sp.strong_parity_solver, gp.disj_parity_win2, gen, 800, iterations=5, step=10, plot=True, path="random-notransform-win2.png")
#rand(sp.strong_parity_solver, gp.disj_parity_win2, generators.ladder, 800, iterations=5, step=10, plot=True, path="ladder-notransform-win2.png")
#rand(sp.strong_parity_solver, gp.disj_parity_win2, generators.weak_parity_worst_case, 200, iterations=5, step=10, plot=True, path="weak-notransform-win2.png")

#rand(sp.strong_parity_solver, gp.disj_parity_win2, generators.strong_parity_worst_case, 15, iterations=3, step=1, plot=True, path="worst-notransform-win2.png")

#rand(sp.strong_parity_solver, sp.strong_parity_solver, gen, 800, iterations=5, step=10, plot=True, path="normalVScompressed-rand.pdf")


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