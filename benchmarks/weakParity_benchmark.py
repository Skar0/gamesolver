# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

from graph import Graph
from solvers.weakParity import weak_parity_solver
from tools import timer, generators, operations

def benchmark(n, generator, iterations=3, step=10, plot=False, regression=False, order=1, path=""):
    """
    General benchmarking function. Calls weak parity solver for player p and target set t on games generated using the
    provided generator function. Games of size 1 to n are solved and a timer records the time taken to get the solution.
    The solver can be timed several times and the minimum value is selected using optional parameter iterations (to
    avoid recording time spikes and delays due to system load). The result as well as a regression can be plotted using
    matplotlib.
    :param n: number of nodes in generated graph.
    :param generator: graph generator function.
    :param iterations: number of times the algorithm is timed (default is 10).
    :param step: step to be taken in the generation.
    :param plot: if True, plots the data using matplotlib.
    :param regression: if True, plots a polynomial regression along with the data.
    :param order: order of that regression.
    :param path: path to the file in which to write the result.
    """

    y = []  # list for the time recordings
    n_ = []  # list for the x values (1 to n)

    total_time = 0  # accumulator to record total time

    nbr_generated = 0  # conserving the number of generated mesures (used to get the index of a mesure)

    chrono = timer.Timer(verbose=False)  # Timer object

    info = "Time to solve (s)"  # info about the current benchmark

    # print first line of output
    print u"Generator".center(40) + "|" + u"Nodes (n)".center(12) + "|" + info.center(40) + "\n" + \
          "-" * 108

    p = 1
    c = 1

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp = []  # temp list for #iterations recordings
        g = generator(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                weak_parity_solver(g)  # solver call
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

    if plot:
        plt.grid(True)
        plt.title(u"Generateur" + str(generator.__name__).replace("_", " "))
        plt.xlabel(u'nombre de nœuds')
        plt.ylabel(u'temps (s)')
        if regression:
            coeficients = np.polyfit(n_, y, order)
            polynom = np.poly1d(coeficients)
            points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
            fit, = plt.plot(n_, polynom(n_), 'b--', label=u"Régression polynomiale de degré " + str(
                order))  # \\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))
            plt.legend(loc='upper left', handles=[points, fit])
        else:
            points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
            plt.legend(loc='upper left', handles=[points])
        plt.savefig(path +"wp_"+generator.__name__ + "_" + str(n) + "_"+str(p)+"_"+str(c)+".png",
                    bbox_inches='tight')
        plt.clf()
        plt.close()

def benchmark_worst_case(n, iterations=3, step=10, plot=False, path=""):
    """
    Calls reachability solver for both players and target set [1] on games generated using the worst case graph
    generator. Games of size 1 to n by step of #step are solved and a timer records the time taken to get the solution.
    The solver can be timed several times and the minimum value is selected depending on the value of optional parameter
    iterations (to avoid recording time spikes and delays due to system load). Time to solve the game for both players
    is recorded and printed to the console in a formated way. Both results can be plotted using matplotlib.
    :param n: number of nodes in generated graph.
    :param iterations: number of times the algorithm is timed (default is 10).
    :param step: step between two sizes of graphs generated.
    :param plot: if True, plots the data using matplotlib.
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
          + u"Reachability (player 0)".center(28) + "|" + u"Reachability (player 1)".center(28) + "\n" + \
          "-" * 108

    # games generated are size 1 to n
    for i in range(1, n + 1, step):
        temp_p0 = []  # temp list for #iterations recordings player 0
        temp_p1 = []  # temp list for #iterations recordings player 0

        g1 = generators.complete_graph_oneplayer_sevparity3(i) # generated game
        g2 = generators.complete_graph_oneplayer_sevparity4(i) # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                pass
                #(W_0, sigma_0), (W_1, sigma_1) = weak_parity_solver(g1)  # solver call player 0
            temp_p0.append(chrono.interval)  # add time recording

        for j in range(iterations):
            with chrono:
                (W_1, sigma_1), (W_0, sigma_0) = weak_parity_solver(g2)  # solver call player 1
            temp_p1.append(chrono.interval)  # add time recording

        min_recording_p0 = min(temp_p0)
        y_p0.append(min_recording_p0)  # get the minimum out of #iterations recordings of player 0
        acc_p0 += min_recording_p0

        min_recording_p1 = min(temp_p1)
        y_p1.append(min_recording_p1)  # get the minimum out of #iterations recordings of player 1
        acc_p1 += min_recording_p1

        n_.append(i)

        print "worst case graph".center(30) + "|" + str(i).center(12) + "|" + str((i * (i + 1)) / 2).center(10) \
              + "|" + str(y_p0[nbr_generated]).center(28) + "|" + str(y_p1[nbr_generated]).center(28) + "\n" + "-" * 108

        nbr_generated += 1  # updating the number of generated mesures

    # at the end, print total time
    print "-" * 108 + "\n" + "total".center(30) + "|" + "#".center(12) + "|" + "#".center(10) + "|" + \
          str(acc_p0).center(28) + "|" + str(acc_p1).center(28) + "\n" + "-" * 108 + "\n"

    if plot:
        if 0 ==1:
            plt.grid(True)
            plt.title(u"Graphes complets de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            coeficients = np.polyfit(n_, y_p0, 2)
            polynom = np.poly1d(coeficients)
            points0, = plt.plot(n_, y_p0, 'g.', label=u'Mesures pour le joueur 0\nEnsemble cible {v1}')
            fit0, = plt.plot(n_, polynom(n_), 'b--', label=u"Régression polynomiale de degré 2")
            plt.legend(loc='upper left', handles=[points0, fit0])
            plt.savefig(path + "worstCase_" + str(n) + "nodes_player0.png", bbox_inches='tight')
            plt.clf()
            plt.close()

            plt.grid(True)
            plt.title(u"Graphes complets de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            coeficients = np.polyfit(n_, y_p1, 1)
            polynom = np.poly1d(coeficients)
            points1, = plt.plot(n_, y_p1, 'g.', label=u'Mesures pour le joueur 1\nEnsemble cible {v1}')
            fit1, = plt.plot(n_, polynom(n_), 'b--',
                             label=u"Régression linéaire")  # \\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))
            plt.legend(loc='upper left', handles=[points1, fit1])
            plt.savefig(path + "worstCase_" + str(n) + "nodes_player1.png", bbox_inches='tight')
            plt.clf()
            plt.close()
        else:
            plt.grid(True)
            plt.title(u"Graphes complets de taille 1 à " + str(n))
            plt.xlabel(u'nombre de nœuds')
            plt.ylabel(u'temps (s)')
            points0, = plt.plot(n_, y_p0, 'g.', label=u'3\nEnsemble cible {v1}')
            points1, = plt.plot(n_, y_p1, 'r.', label=u'4\nEnsemble cible {v1}')
            coeficients1 = np.polyfit(n_, y_p1, 2)
            polynom1 = np.poly1d(coeficients1)
            print polynom1
            fit1, = plt.plot(n_, polynom1(n_), 'b--',
                             label=u"Régression 2")
            coeficients2 = np.polyfit(n_, y_p1, 3)
            polynom2 = np.poly1d(coeficients2)
            print polynom2
            fit2, = plt.plot(n_, polynom2(n_), 'k--',
                             label=u"Régression 3")
            plt.legend(loc='upper left', handles=[points1,points0,fit1,fit2])
            plt.savefig(path + "worstCase_" + str(n) + "nodes_player1.png", bbox_inches='tight')
            plt.clf()
            plt.close()

benchmark(10000,generators.complete_graph_weakparity,iterations=3,step=100,plot=True,regression=True, order=2,path="../resu/")
benchmark(10000,generators.complete_graph_oneplayer_sevparity4,iterations=3,step=100,plot=True,regression=True, order=3,path="../resu/")