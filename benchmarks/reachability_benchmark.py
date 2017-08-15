# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

from solvers.reachability import reachability_solver
from tools import timer, generators

"""
This module benchmarks the strong parity games.
"""


def benchmark_complete_graph(n, iterations=3, step=10, plot=False, regression=False, path=""):
    """
    Unused. This was made to compare execution time between players on complete graphs.
    Calls reachability solver for both players and target set [1] on games generated using the complete graph generator.
    Games of size 1 to n by step of #step are solved and a timer records the time taken to get the solution. The solver
    can be timed several times and the minimum value is selected depending on the value of optional parameter iterations
    (to avoid recording time spikes and delays due to system load). Time to solve the game for both players is recorded
    and printed to the console in a formatted way. Both results can be plotted using matplotlib.
    :param n: number of nodes in generated graph.
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step between two sizes of graphs generated.
    :param plot: if True, plots the data using matplotlib.
    :param regression: if True, plots a polynomial regression.
    :param path: path to the file in which to write the result.
    """
    y_p0 = []  # list for the time recordings of player 0
    y_p1 = []  # list for the time recordings of player 1
    acc_p0 = 0  # accumulator for total time of player 0
    acc_p1 = 0  # accumulator for total time of player 1

    n_ = []  # list for the x values (1 to n)

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    # print first line of output
    print u"Generator".center(30) + "|" + u"Nodes (n)".center(12) + "|" + "Edges (m)".center(10) + "|" \
          + u"Time to solve, player 0".center(28) + "|" + u"Time to solve, player 1".center(28) + "\n" + \
          "-" * 108

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp_p0 = []  # temp list for #iterations recordings player 0
        temp_p1 = []  # temp list for #iterations recordings player 0

        g = generators.complete_graph(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                (W_0, sigma_0), (W_1, sigma_1) = reachability_solver(g, [1], 0)  # solver call player 0
            temp_p0.append(chrono.interval)  # add time recording

        for j in range(iterations):
            with chrono:
                (W_1, sigma_1), (W_0, sigma_0) = reachability_solver(g, [1], 1)  # solver call player 1
            temp_p1.append(chrono.interval)  # add time recording

        min_recording_p0 = min(temp_p0)
        y_p0.append(min_recording_p0)  # get the minimum out of #iterations recordings of player 0
        acc_p0 += min_recording_p0

        min_recording_p1 = min(temp_p1)
        y_p1.append(min_recording_p1)  # get the minimum out of #iterations recordings of player 1
        acc_p1 += min_recording_p1

        n_.append(i)

        print "Complete graph".center(30) + "|" + str(i).center(12) + "|" + str(i * i).center(10) \
              + "|" + str(y_p0[nbr_generated]).center(28) + "|" + str(y_p1[nbr_generated]).center(28) + "\n" + "-" * 108

        nbr_generated += 1  # updating the number of generated mesures

    # at the end, print total time
    print "-" * 108 + "\n" + "Total time".center(30) + "|" + "#".center(12) + "|" + "#".center(10) + "|" + \
          str(acc_p0).center(28) + "|" + str(acc_p1).center(28) + "\n" + "-" * 108 + "\n"

    if plot:
        if regression:
            plt.grid(True)
            plt.title(u"Graphes complets de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            coeficients = np.polyfit(n_, y_p0, 2)
            polynom = np.poly1d(coeficients)
            points0, = plt.plot(n_, y_p0, 'g.', label=u"Temps d'exécution, joueur 0,\nensemble cible {v1}")
            fit0, = plt.plot(n_, polynom(n_), 'b--', label=u"Régression polynomiale de degré 2")
            plt.legend(loc='upper left', handles=[points0, fit0])
            plt.savefig(path + "completeGraph_" + str(n) + "nodes_player0.png", bbox_inches='tight')
            plt.clf()
            plt.close()

            plt.grid(True)
            plt.title(u"Graphes complets de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            coeficients = np.polyfit(n_, y_p1, 2)
            polynom = np.poly1d(coeficients)
            points1, = plt.plot(n_, y_p1, 'g.', label=u"Temps d'exécution, joueur 1,\nensemble cible {v1}")
            fit1, = plt.plot(n_, polynom(n_), 'b--',
                             label=u"Régression polynomiale de degré 2")  # \\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))
            plt.legend(loc='upper left', handles=[points1, fit1])
            plt.savefig(path + "completeGraph_" + str(n) + "nodes_player1.png", bbox_inches='tight')
            plt.clf()
            plt.close()
        else:
            plt.grid(True)
            plt.title(u"Graphes complets de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            points0, = plt.plot(n_, y_p0, 'g.', label=u"Temps d'exécution, joueur 0,\nensemble cible {v1}")
            plt.legend(loc='upper left', handles=[points0])
            plt.savefig(path + "completeGraph_" + str(n) + "nodes_player0.png", bbox_inches='tight')
            plt.clf()
            plt.close()

            plt.grid(True)
            plt.title(u"Graphes complets de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            points1, = plt.plot(n_, y_p1, 'g.', label=u"Temps d'exécution, joueur 1,\nensemble cible {v1}")
            plt.legend(loc='upper left', handles=[points1])
            plt.savefig(path + "completeGraph_" + str(n) + "nodes_player1.png", bbox_inches='tight')
            plt.clf()
            plt.close()


def benchmark_worst_case(n, iterations=3, step=10, plot=False, regression=False, path=""):
    """
    Unused. This was made to compare execution time between players on worst case graphs.
    Calls reachability solver for both players and target set [1] on games generated using the worst case graph
    generator. Games of size 1 to n by step of #step are solved and a timer records the time taken to get the solution.
    The solver can be timed several times and the minimum value is selected depending on the value of optional parameter
    iterations (to avoid recording time spikes and delays due to system load). Time to solve the game for both players
    is recorded and printed to the console in a formatted way. Both results can be plotted using matplotlib.
    :param n: number of nodes in generated graph.
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step between two sizes of graphs generated.
    :param plot: if True, plots the data using matplotlib.
    :param regression: if True, plots a polynomial regression.
    :param path: path to the file in which to write the result.
    """
    y_p0 = []  # list for the time recordings of player 0
    y_p1 = []  # list for the time recordings of player 1
    acc_p0 = 0  # accumulator for total time of player 0
    acc_p1 = 0  # accumulator for total time of player 1

    n_ = []  # list for the x values (1 to n)

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    # print first line of output
    print u"Generator".center(30) + "|" + u"Nodes (n)".center(12) + "|" + "Edges (m)".center(10) + "|" \
          + u"Time to solve, player 0".center(28) + "|" + u"Time to solve, player 1".center(28) + "\n" + \
          "-" * 108

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp_p0 = []  # temp list for #iterations recordings player 0
        temp_p1 = []  # temp list for #iterations recordings player 0

        g = generators.reachability_worst_case(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                (W_0, sigma_0), (W_1, sigma_1) = reachability_solver(g, [1], 0)  # solver call player 0
            temp_p0.append(chrono.interval)  # add time recording

        for j in range(iterations):
            with chrono:
                (W_1, sigma_1), (W_0, sigma_0) = reachability_solver(g, [1], 1)  # solver call player 1
            temp_p1.append(chrono.interval)  # add time recording

        min_recording_p0 = min(temp_p0)
        y_p0.append(min_recording_p0)  # get the minimum out of #iterations recordings of player 0
        acc_p0 += min_recording_p0

        min_recording_p1 = min(temp_p1)
        y_p1.append(min_recording_p1)  # get the minimum out of #iterations recordings of player 1
        acc_p1 += min_recording_p1

        n_.append(i)

        print "Worst-case graph".center(30) + "|" + str(i).center(12) + "|" + str((i * (i + 1)) / 2).center(10) \
              + "|" + str(y_p0[nbr_generated]).center(28) + "|" + str(y_p1[nbr_generated]).center(28) + "\n" + "-" * 108

        nbr_generated += 1  # updating the number of generated mesures

    # at the end, print total time
    print "-" * 108 + "\n" + "Total time".center(30) + "|" + "#".center(12) + "|" + "#".center(10) + "|" + \
          str(acc_p0).center(28) + "|" + str(acc_p1).center(28) + "\n" + "-" * 108 + "\n"

    if plot:
        if regression:
            plt.grid(True)
            plt.title(u"Graphes 'pire cas' de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            coeficients = np.polyfit(n_, y_p0, 2)
            polynom = np.poly1d(coeficients)
            points0, = plt.plot(n_, y_p0, 'g.', label=u"Temps d'exécution, joueur 0,\nensemble cible {v1}")
            fit0, = plt.plot(n_, polynom(n_), 'b--', label=u"Régression polynomiale de degré 2")
            plt.legend(loc='upper left', handles=[points0, fit0])
            plt.savefig(path + "worstCase_" + str(n) + "nodes_player0.png", bbox_inches='tight')
            plt.clf()
            plt.close()

            plt.grid(True)
            plt.title(u"Graphes 'pire cas' de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            coeficients = np.polyfit(n_, y_p1, 1)
            polynom = np.poly1d(coeficients)
            points1, = plt.plot(n_, y_p1, 'g.', label=u"Temps d'exécution, joueur 1,\nensemble cible {v1}")
            fit1, = plt.plot(n_, polynom(n_), 'b--',
                             label=u"Régression linéaire")  # \\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))
            plt.legend(loc='upper left', handles=[points1, fit1])
            plt.savefig(path + "worstCase_" + str(n) + "nodes_player1.png", bbox_inches='tight')
            plt.clf()
            plt.close()
        else:
            plt.grid(True)
            plt.title(u"Graphes pire cas de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            points0, = plt.plot(n_, y_p0, 'g.', label=u"Temps d'exécution, joueur 0,\nensemble cible {v1}")
            plt.legend(loc='upper left', handles=[points0])
            plt.savefig(path + "worstCase_" + str(n) + "nodes_player0.png", bbox_inches='tight')
            plt.clf()
            plt.close()

            plt.grid(True)
            plt.title(u"Graphes pire cas de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            points1, = plt.plot(n_, y_p1, 'g.', label=u"Temps d'exécution, joueur 1,\nensemble cible {v1}")
            plt.legend(loc='upper left', handles=[points1])
            plt.savefig(path + "worstCase_" + str(n) + "nodes_player1.png", bbox_inches='tight')
            plt.clf()
            plt.close()


def benchmark_complete_targetset(n, iterations=3, step=10, plot=False, regression=False, path=""):
    """
    Unused. This was made to compare execution time between players on graphs where the target set is the set of nodes.
    Calls reachability solver for player 1 on complete graphs where the target set is the set of all nodes. This makes
    the algorithm add all nodes to the queue and all predecessor lists are iterated over.
    Games of size 1 to n by step of #step are solved and a timer records the time taken to get the solution. The solver
    can be timed several times and the minimum value is selected depending on the value of optional parameter iterations
    (to avoid recording time spikes and delays due to system load). Time to solve the game is recorded and printed to
    the console in a formatted way. The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph.
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step between two sizes of graphs generated.
    :param plot: if True, plots the data using matplotlib.
    :param regression: if True, plots a polynomial regression.
    :param path: path to the file in which to write the result.
    """
    y = []  # list for the time recordings
    n_ = []  # list for the x values (1 to n)

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s), player " + str(1) + ", target set : V"  # info about the current benchmark

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "\n" + \
          "-" * 108

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp = []  # temp list for #iterations recordings
        g = generators.complete_graph(i)  # generated game

        # #iterations calls to the solver are timed

        target = range(1, i + 1)  # target set is the set of all nodes

        for j in range(iterations):
            with chrono:
                reachability_solver(g, target, 1)  # solver call
            temp.append(chrono.interval)  # add time recording

        min_recording = min(temp)
        y.append(min_recording)  # get the minimum out of #iterations recordings
        n_.append(i)
        total_time += min_recording

        print "Complete graph".center(40) + "|" + str(i).center(12) + "|" \
              + str(y[nbr_generated]).center(40) + "\n" + "-" * 108

        nbr_generated += 1  # updating the number of generated mesures

        # at the end, print total time
    print "-" * 108 + "\n" + "Total time".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "\n" + "-" * 108 + "\n"

    if plot:
        plt.grid(True)
        plt.title(u"Graphes complets de taille 1 à " + str(n))
        plt.xlabel(u'nombre de nœuds')
        plt.ylabel(u'temps (s)')
        if regression:
            coeficients = np.polyfit(n_, y, 2)
            polynom = np.poly1d(coeficients)
            points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution,\nensemble cible : V")
            fit, = plt.plot(n_, polynom(n_), 'b--', label=u"Régression polynomiale de degré 2")
            plt.legend(loc='upper left', handles=[points, fit])
        else:
            points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution,\nensemble cible : V")
            plt.legend(loc='upper left', handles=[points])
        plt.savefig(path + "complete_graph" + "_" + str(n) + "nodes_targetallnodes" + ".png",
                    bbox_inches='tight')
        plt.clf()
        plt.close()


def benchmark(n, generator, t, p, iterations=3, step=10, plot=False, regression=False, order=1, path="", title=""):
    """
    General benchmarking function. Calls reachability solver on games generated using the provided generator function
    and for provided player and target set. Games of size 1 to n by a certain step are solved and a timer records the
    time taken to get the solution. The solver can be timed several times and the minimum value is selected using
    optional parameter iterations (to avoid recording time spikes and delays due to system load). The result as well as
    a regression can be plotted using matplotlib.
    :param n: number of nodes in generated graph.
    :param generator: graph generator function.
    :param iterations: number of times the algorithm is timed (default is 3).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param regression: if True, plots a polynomial regression along with the data.
    :param order: order of that regression.
    :param path: path to the file in which to write the result.
    :param title: the title to be used in the plot.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (1 to n)

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s), player " + str(p) + ", target set " + str(t)  # info about the current benchmark

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "\n" + \
          "-" * 108

    # games generated are size 1 to n with a certain step
    for i in range(1, n + 1, step):
        temp = []  # temp list for #iterations recordings
        g = generator(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                reachability_solver(g, t, p)  # solver call
            temp.append(chrono.interval)  # add time recording

        min_recording = min(temp)
        y.append(min_recording)  # get the minimum out of #iterations recordings
        n_.append(i)
        total_time += min_recording

        print generator.__name__.center(40) + "|" + str(i).center(12) + "|" \
              + str(y[nbr_generated]).center(40) + "\n" + "-" * 108

        nbr_generated += 1  # updating the number of generated mesures

    # at the end, print total time
    print "-" * 108 + "\n" + "Total (s)".center(40) + "|" + "#".center(12) + "|" + \
          str(total_time).center(40) + "\n" + "-" * 108 + "\n"

    # if we need to plot
    if plot:
        plt.grid(True)
        if title != "":
            plt.title(title)
        else:
            plt.title(u"Générateur : " + str(generator.__name__).replace("_", " "))
        plt.xlabel(u'nombre de nœuds')
        plt.ylabel(u'temps (s)')
        if regression:
            coeficients = np.polyfit(n_, y, order)
            polynom = np.poly1d(coeficients)
            points, = plt.plot(n_, y, 'g.',
                               label=u"Temps d'exécution, joueur " + str(p) + u',\nensemble cible ' + str(t))
            fit, = plt.plot(n_, polynom(n_), 'b--', alpha=0.6, label=u"Régression polynomiale de degré " + str(order))
            plt.legend(loc='upper left', handles=[points, fit])
        else:
            points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
            plt.legend(loc='upper left', handles=[points])

        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()
