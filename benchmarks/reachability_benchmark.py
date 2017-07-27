# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

from solvers.reachability import reachability_solver_updated
from tools import timer, generators


def benchmark(n, generator, t, p, iterations=10, plot=False):
    """
    Modular benchmarking function. Calls reachability solver for player p and target set t on games generated using the
    provided generator function. Games of size 1 to n are solved and a timer records the time taken to get the solution.
    The solver can be timed several times and the minimum value is selected using optional parameter iterations (to
    avoid recording time spikes and delays due to system load). The result can be plotted using matplotlib.
    :param n: number of nodes in generated graph.
    :param generator: graph generator function.
    :param t: target set.
    :param p: player for attractor computation.
    :param iterations: number of times the algorithm is timed (default is 10).
    :param plot: if True, plots the data using matplotlib.
    :return: a str containing benchmarking data.
    """
    y = [] # list for the time recordings
    n_ = [] # list for the x values (1 to n)

    chrono = timer.Timer(verbose=False) # Timer object

    # games generated are size 1 to n
    for i in range(1, n+1):
        temp = []  # temp list for #iterations recordings
        g = generator(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                regions, strategies = reachability_solver_updated(g, t, p) # solver call
            temp.append(chrono.interval) # add time recording

        y.append(min(temp)) # get the minimum out of #iterations recordings
        n_.append(i)

    if plot:
        plt.grid(True)
        plt.title(u"\\textbf{\Large Générateur 2 : graphes complets}")
        plt.xlabel(u'\large nombre de nœuds')
        plt.ylabel(u'\large temps (s)')
        coeficients = np.polyfit(n_, y, 2)
        polynom = np.poly1d(coeficients)
        points, = plt.plot(n_, y, 'g.',label=u'Mesures')
        fit, = plt.plot(n_, polynom(n_), 'b--', label=u"Régression polynomiale de degré 2") #\\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))
        plt.legend(handles=[points,fit])
        plt.show()
        #plt.savefig("figures/" + str(n) + "_gen2_n.png", bbox_inches='tight')

#benchmark(100, generators.complete_graph, [1], 0, iterations=3, plot=True)
