# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

from graph import Graph
from solvers.weakParity import weak_parity_solver
from tools import timer, generators, operations

def benchmark(n, generator, iterations=3, step=10, plot=False, regression=False, order=1, path="", title=""):
    """
    General benchmarking function. Calls weak parity solver on games generated using the provided generator function.
    Games of size 1 to n are solved and a timer records the time taken to get the solution. The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time spikes
    and delays due to system load). The result as well as a regression can be plotted using matplotlib.
    :param n: number of nodes in generated graph.
    :param generator: graph generator function.
    :param iterations: number of times the algorithm is timed (default is 10).
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

    info = "Time to solve (s)"  # info about the current benchmark

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
            points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
            fit, = plt.plot(n_, polynom(n_), 'b--',  alpha=0.6, label=u"Régression polynomiale de degré " + str(order))
            plt.legend(loc='upper left', handles=[points, fit])
        else:
            points, = plt.plot(n_, y, 'g.', label=u"Temps d'exécution")
            plt.legend(loc='upper left', handles=[points])

        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()

#benchmark(10000,generators.complete_graph_weakparity,iterations=3,step=100,plot=True,regression=True, order=2,path="../figures/")
#benchmark(400, generators.weak_parity_worst_case, iterations=1, step=10, plot=True, regression=True, order=3, path="../figures/")
