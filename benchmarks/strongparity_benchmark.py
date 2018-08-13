# coding=utf-8
from random import randint
import matplotlib.pyplot as plt

from solvers.strongparity import strong_parity_solver, strong_parity_solver_non_removed
from tools import timer, generators
from bitarray import bitarray

"""
This module benchmarks the strong parity games.
"""


def benchmark_random(n, iterations=3, step=10, plot=False, path=""):
    """
    This function is unfinished.
    Benchmarks the recursive algorithm for strong parity games using a random generator. Calls strong parity solver
    on games generated using the random generator function. Games of 1 to n are solved and a timer records the
    time taken to get the solution.The solver can be timed several times and the minimum value is selected using
    optional parameter iterations (to avoid recording time spikes and delays due to system load). The result can be
    plotted using matplotlib.
    :param n: number of nodes in generated graph.
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param path: path to the file in which to write the result.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve"  # info about the current benchmark

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "\n" + \
          "-" * 108

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp = []  # temp list for #iterations recordings
        prio = randint(0, i)  # number of priorities
        min_out = randint(0, i)
        max_out = randint(min_out, i)
        g = generators.random(i, prio, min_out, max_out)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                strong_parity_solver(g)  # solver call
            temp.append(chrono.interval)  # add time recording

        min_recording = min(temp)
        y.append(min_recording)  # get the minimum out of #iterations recordings
        n_.append(i)
        total_time += min_recording

        print "Random graph".center(40) + "|" + str(i).center(12) + "|" \
              + str(y[nbr_generated]).center(40) + "\n" + "-" * 108

        nbr_generated += 1  # updating the number of generated mesures

        # at the end, print total time
    print "-" * 108 + "\n" + "Total time".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "\n" + "-" * 108 + "\n"

    if plot:
        plt.grid(True)
        plt.title(u"Graphes aléatoires de taille 1 à " + str(n))
        plt.xlabel(u'nombre de nœuds')
        plt.ylabel(u'temps (s)')
        points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
        plt.legend(loc='upper left', handles=[points])
        plt.savefig(path + "sp_random_" + str(n) + ".png", bbox_inches='tight')
        plt.clf()
        plt.close()


def benchmark_worst_case(n, iterations=3, step=10, plot=False, path=""):
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

    y = []  # list for the time recordings
    n_ = []  # list for the x values (5 to 5n)

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "\n" + \
          "-" * 108

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp = []  # temp list for #iterations recordings
        g = generators.strong_parity_worst_case(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                strong_parity_solver(g)  # solver call
            temp.append(chrono.interval)  # add time recording

        min_recording = min(temp)
        y.append(min_recording)  # get the minimum out of #iterations recordings
        n_.append(5 * i)
        total_time += min_recording

        print "Worst-case graph".center(40) + "|" + str(i * 5).center(12) + "|" \
              + str(y[nbr_generated]).center(40) + "\n" + "-" * 108

        nbr_generated += 1  # updating the number of generated mesures

        # at the end, print total time
    print "-" * 108 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "\n" + "-" * 108 + "\n"

    if plot:
        plt.grid(True)
        plt.title(u"Graphes 'pire cas' de taille 5 à " + str(5 * n))
        plt.xlabel(u'nombre de nœuds')
        plt.ylabel(u'temps (s)')
        # plt.yscale("log") allows logatithmic y-axis
        points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
        plt.legend(loc='upper left', handles=[points])
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()

def benchmark_random_removed_optimization(n, iterations=3, step=10, plot=False, path=""):
        """
        This function is unfinished.
        Benchmarks the recursive algorithm for strong parity games using a random generator. Calls strong parity solver
        on games generated using the random generator function. Games of 1 to n are solved and a timer records the
        time taken to get the solution.The solver can be timed several times and the minimum value is selected using
        optional parameter iterations (to avoid recording time spikes and delays due to system load). The result can be
        plotted using matplotlib.
        :param n: number of nodes in generated graph.
        :param iterations: number of times the algorithm is timed (default is 3).
        :param step: step to be taken in the generation.
        :param plot: if True, plots the data using matplotlib.
        :param path: path to the file in which to write the result.
        """

        y = []  # list for the time recordings
        n_ = []  # list for the x values

        total_time = 0  # accumulator to record total time

        nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

        chrono = timer.Timer(verbose=False)  # Timer object

        info = "Time to solve"  # info about the current benchmark

        # print first line of output
        print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "\n" + \
              "-" * 108

        # games generated are size 1 to n
        for i in range(1, n + 1, step):
            temp = []  # temp list for #iterations recordings
            prio = randint(0, i)  # number of priorities
            min_out = randint(0, i)
            max_out = randint(min_out, i)
            g = generators.random(i, prio, min_out, max_out)  # generated game

            # #iterations calls to the solver are timed
            for j in range(iterations):
                with chrono:
                    strong_parity_solver(g)  # solver call
                temp.append(chrono.interval)  # add time recording

            min_recording = min(temp)
            y.append(min_recording)  # get the minimum out of #iterations recordings
            n_.append(i)
            total_time += min_recording

            print "Random graph".center(40) + "|" + str(i).center(12) + "|" \
                  + str(y[nbr_generated]).center(40) + "\n" + "-" * 108

            nbr_generated += 1  # updating the number of generated mesures

            # at the end, print total time
        print "-" * 108 + "\n" + "Total time".center(40) + "|" + "#".center(12) + "|" + \
              str(total_time).center(40) + "\n" + "-" * 108 + "\n"

        if plot:
            plt.grid(True)
            plt.title(u"Graphes aléatoires de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
            plt.legend(loc='upper left', handles=[points])
            plt.savefig(path + "sp_random_" + str(n) + ".png", bbox_inches='tight')
            plt.clf()
            plt.close()

def benchmark_worst_case_removed_optimization(n, iterations=3, step=10, plot=False, path=""):
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

        y = []  # list for the time recordings
        n_ = []  # list for the x values (5 to 5n)
        y2 = []  # list for the time recordings
        n_2 = []  # list for the x values (5 to 5n)
        total_time = 0  # accumulator to record total time

        nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

        chrono = timer.Timer(verbose=False)  # Timer object

        info = "Time to solve (s)"  # info about the current benchmark

        # print first line of output
        print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "\n" + \
              "-" * 108

        # games generated are size 1 to n
        for i in range(1, n + 1, step):
            temp = []  # temp list for #iterations recordings
            g = generators.strong_parity_worst_case(i)  # generated game

            # #iterations calls to the solver are timed
            for j in range(iterations):
                with chrono:
                    strong_parity_solver(g)  # solver call
                temp.append(chrono.interval)  # add time recording

            min_recording = min(temp)
            y.append(min_recording)  # get the minimum out of #iterations recordings
            n_.append(5 * i)
            total_time += min_recording

            temp = []
            # #iterations calls to the solver are timed
            removed = bitarray([False] + ([False] * len(g.nodes)))
            for j in range(iterations):
                with chrono:
                    strong_parity_solver_non_removed(g, removed)  # solver call
                temp.append(chrono.interval)  # add time recording

            min_recording = min(temp)
            y2.append(min_recording)  # get the minimum out of #iterations recordings
            n_2.append(5 * i)

            min_recording = min(temp)

            print "Worst-case graph".center(40) + "|" + str(i * 5).center(12) + "|" \
                  + str(y[nbr_generated]).center(40) + "\n" + "-" * 108

            nbr_generated += 1  # updating the number of generated mesures

            # at the end, print total time
        print "-" * 108 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
              str(total_time).center(40) + "\n" + "-" * 108 + "\n"

        if plot:
            plt.grid(True)
            plt.title(u"Graphes 'pire cas' de taille 5 à " + str(5 * n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            # plt.yscale("log") allows logatithmic y-axis
            points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
            points2, = plt.plot(n_2, y2, 'r.', label=u"Temps d'exécution 2")

            plt.legend(loc='upper left', handles=[points, points2])
            plt.savefig(path, bbox_inches='tight')
            plt.clf()
            plt.close()
# benchmark_worst_case(30, iterations=3, step=1, plot=True)

def ladder(n, iterations=3, step=10, plot=False, path=""):
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

    y = []  # list for the time recordings
    n_ = []  # list for the x values (5 to 5n)
    y2 = []  # list for the time recordings
    n_2 = []  # list for the x values (5 to 5n)
    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "\n" + \
          "-" * 108

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp1 = []  # temp list for #iterations recordings
        g = generators.ladder(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                strong_parity_solver(g)  # solver call
            temp1.append(chrono.interval)  # add time recording

        min_recording = min(temp1)
        y.append(min_recording)  # get the minimum out of #iterations recordings
        n_.append(2 * i - 1)
        total_time += min_recording

        temp2 = []
        # #iterations calls to the solver are timed
        removed = bitarray([False] + ([False] * len(g.nodes)))
        for j in range(iterations):
            with chrono:
                strong_parity_solver_non_removed(g, removed)  # solver call
            temp2.append(chrono.interval)  # add time recording

        min_recording = min(temp2)
        y2.append(min_recording)  # get the minimum out of #iterations recordings
        n_2.append(2 * i - 1)


        print "Worst-case graph".center(40) + "|" + str(i * 5).center(12) + "|" \
              + str(y[nbr_generated]).center(40) + "\n" + "-" * 108

        nbr_generated += 1  # updating the number of generated mesures

        # at the end, print total time
    print "-" * 108 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "\n" + "-" * 108 + "\n"

    if plot:
        plt.grid(True)
        plt.title(u"Graphes 'pire cas' de taille 5 à " + str(2 * n - 1))
        plt.xlabel(u'nombre de nœuds')
        plt.ylabel(u'temps (s)')

        # plt.yscale("log") allows logatithmic y-axis
        points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
        points2, = plt.plot(n_2, y2, 'r.', label=u"Temps d'exécution 2")

        plt.legend(loc='upper left', handles=[points, points2])
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()


def rand(n, iterations=3, step=10, plot=False, path=""):
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

    y = []  # list for the time recordings
    n_ = []  # list for the x values (5 to 5n)
    y2 = []  # list for the time recordings
    n_2 = []  # list for the x values (5 to 5n)
    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "\n" + \
          "-" * 108

    # games generated are size 1 to n
    for i in range(4, n + 1, step):
        temp1 = []  # temp list for #iterations recordings
        g = generators.random(i, i, 1, (i/2))  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                strong_parity_solver(g)  # solver call
            temp1.append(chrono.interval)  # add time recording

        min_recording = min(temp1)
        y.append(min_recording)  # get the minimum out of #iterations recordings
        n_.append(i )
        total_time += min_recording

        temp2 = []
        # #iterations calls to the solver are timed
        removed = bitarray([False] + ([False] * len(g.nodes)))
        for j in range(iterations):
            with chrono:
                strong_parity_solver_non_removed(g, removed)  # solver call
            temp2.append(chrono.interval)  # add time recording

        min_recording = min(temp2)
        y2.append(min_recording)  # get the minimum out of #iterations recordings
        n_2.append(i)



        print "Worst-case graph".center(40) + "|" + str(i ).center(12) + "|" \
              + str(y[nbr_generated]).center(40) + "\n" + "-" * 108

        nbr_generated += 1  # updating the number of generated mesures

        # at the end, print total time
    print "-" * 108 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "\n" + "-" * 108 + "\n"

    if plot:
        plt.grid(True)
        plt.title(u"Graphes 'pire cas' de taille 5 à " + str(2 * n - 1))
        plt.xlabel(u'nombre de nœuds')
        plt.ylabel(u'temps (s)')

        # plt.yscale("log") allows logatithmic y-axis
        points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
        points2, = plt.plot(n_2, y2, 'r.', label=u"Temps d'exécution 2")

        plt.legend(loc='upper left', handles=[points, points2])
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()

#rand(500, iterations=4, step=1, plot=True, path="rand.png")
