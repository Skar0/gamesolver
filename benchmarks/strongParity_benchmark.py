# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from tools.fileHandler import load_from_file

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True

from solvers.strongParity import strongparity_solver2
from tools import timer, generators,fileHandler



def benchmark(n, iterations=10, step=10, plot=False, regression=False, order=1):
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
    for i in range(1, n+1,step):
        temp = []  # temp list for #iterations recordings
        g = load_from_file("../assets/strong parity/recursive_ladder_"+str(i)+".txt")

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                strongparity_solver2(g)# solver call
            temp.append(chrono.interval) # add time recording

        y.append(min(temp)) # get the minimum out of #iterations recordings
        n_.append(i*5)

    if plot:
        plt.grid(True)
        plt.title(u"\\textbf{\Large Générateur :} recursive ladder games")
        plt.xlabel(u'\large nombre de nœuds')
        plt.ylabel(u'\large temps (s)')
        if regression:
            coeficients = np.polyfit(n_, y, order)
            polynom = np.poly1d(coeficients)
            points, = plt.plot(n_, y, 'g.',label=u'Mesures')
            fit, = plt.plot(n_, polynom(n_), 'b--', label=u"Régression de degré "+str(order)) #\\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))
            plt.legend(loc='upper left', handles=[points,fit])
        else:
            points, = plt.plot(n_, y, 'g.', label=u'Mesures')
            plt.legend(loc='upper left', handles=[points])
        plt.savefig(str(n)+"_strongParity.png", bbox_inches='tight')
        plt.clf()
        plt.close()