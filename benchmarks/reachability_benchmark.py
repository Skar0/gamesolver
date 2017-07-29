# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

from solvers.reachability import reachability_solver
from tools import timer, generators


def benchmark_complete_graph(n, t, iterations=3, plot=False):
    """
    Calls reachability solver for both players and target set t on games generated using the complete graph generator.
    Games of size 1 to n are solved and a timer records the time taken to get the solution. The solver can be timed
    several times and the minimum value is selected using optional parameter iterations (to avoid recording time spikes
    and delays due to system load). Time to solve the game for both players is recorded and a str representation is
    created using the time recording each 10 iterations. The comparison can be plotted using matplotlib.
    :param n: number of nodes in generated graph.
    :param t: target set.
    :param iterations: number of times the algorithm is timed (default is 10).
    :param plot: if True, plots the data using matplotlib.
    :return: a str containing benchmarking data.
    """
    y_p0 = [] # list for the time recordings of player 0
    y_p1 = [] # list for the time recordings of player 1
    acc_p0 = 0
    acc_p1 = 0

    n_ = [] # list for the x values (1 to n)

    formatted_output = ""
    chrono = timer.Timer(verbose=False) # Timer object

    # games generated are size 1 to n
    for i in range(1, n+1):
        temp_p0 = []  # temp list for #iterations recordings player 0
        temp_p1 = []  # temp list for #iterations recordings player 0

        g = generators.complete_graph(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                regions, strategies = reachability_solver(g, t, 0) # solver call player 0
            temp_p0.append(chrono.interval) # add time recording

        for j in range(iterations):
            with chrono:
                regions, strategies = reachability_solver(g, t, 1) # solver call player 1
            temp_p1.append(chrono.interval) # add time recording

        min_recording_p0 = min(temp_p0)
        y_p0.append(min_recording_p0) # get the minimum out of #iterations recordings of player 0
        acc_p0+=min_recording_p0

        min_recording_p1 = min(temp_p1)
        y_p1.append(min_recording_p1) # get the minimum out of #iterations recordings of player 1
        acc_p1+=min_recording_p1

        n_.append(i)

        if i%10 == 0:
            formatted_output += "complete graph".center(30)+"|"+str(i).center(12)+"|"+str(i*i).center(10)\
                                +"|"+str(y_p0[i-1]).center(28)+"|"+str(y_p1[i-1]).center(28)+"\n"

    formatted_output += "-" * 108 + "\n"+"total".center(30) + "|" + "#".center(12) + "|" + "#".center(10) + "|" + \
                        str(acc_p0).center(28) + "|" + str(acc_p1).center(28) +"\n"+ "-" * 108 + "\n"

    if plot:
        plt.grid(True)
        plt.title(u"\\textbf{\Large Générateur :} "+"graphes complets".replace("_"," "))
        plt.xlabel(u'\large nombre de nœuds')
        plt.ylabel(u'\large temps (s)')
        coeficients = np.polyfit(n_, y_p0, 2)
        polynom = np.poly1d(coeficients)
        points0, = plt.plot(n_, y_p0, 'g.',label=u'Mesures (joueur 0)')
        fit0, = plt.plot(n_, polynom(n_), 'b--', label=u"Régression polynomiale de degré 2") #\\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))

        coeficients = np.polyfit(n_, y_p1, 2)
        polynom = np.poly1d(coeficients)
        points1, = plt.plot(n_, y_p1, 'r.',label=u'Mesures (joueur 1)')
        fit1, = plt.plot(n_, polynom(n_), 'k--', label=u"Régression polynomiale de degré 2") #\\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))
        plt.legend(loc='upper left', handles=[points0,fit0,points1,fit1])
        plt.savefig(str(n)+"_"+"complets"+"_"+".png", bbox_inches='tight')
    return formatted_output

def benchmark_worstcase_graph(n, t, iterations=3, plot=False):
    """
    Calls reachability solver for both players and target set t on games generated using the reachability worst case
    graph generator. Games of size 1 to n are solved and a timer records the time taken to get the solution. The solver
    can be timed several times and the minimum value is selected using optional parameter iterations (to avoid recording
    time spikes and delays due to system load). Time to solve the game for both players is recorded and a str
    representation is created using the time recording each 10 iterations. The comparison can be plotted using
    matplotlib.
    :param n: number of nodes in generated graph.
    :param t: target set.
    :param iterations: number of times the algorithm is timed (default is 10).
    :param plot: if True, plots the data using matplotlib.
    :return: a str containing benchmarking data.
    """
    y_p0 = [] # list for the time recordings of player 0
    y_p1 = [] # list for the time recordings of player 1
    acc_p0 = 0
    acc_p1 = 0

    n_ = [] # list for the x values (1 to n)

    formatted_output = ""
    chrono = timer.Timer(verbose=False) # Timer object

    # games generated are size 1 to n
    for i in range(1, n+1):
        temp_p0 = []  # temp list for #iterations recordings player 0
        temp_p1 = []  # temp list for #iterations recordings player 0

        g = generators.reachability_worstcase_chain(i)  # generated game

        # #iterations calls to the solver are timed
        for j in range(iterations):
            with chrono:
                regions, strategies = reachability_solver(g, t, 0) # solver call player 0
            temp_p0.append(chrono.interval) # add time recording

        for j in range(iterations):
            with chrono:
                regions, strategies = reachability_solver(g, t, 1) # solver call player 1
            temp_p1.append(chrono.interval) # add time recording

        min_recording_p0 = min(temp_p0)
        y_p0.append(min_recording_p0) # get the minimum out of #iterations recordings of player 0
        acc_p0+=min_recording_p0

        min_recording_p1 = min(temp_p1)
        y_p1.append(min_recording_p1) # get the minimum out of #iterations recordings of player 1
        acc_p1+=min_recording_p1

        n_.append(i)

        if i%10 == 0:
            formatted_output += "worst case".center(30)+"|"+str(i).center(12)+"|"+str((i*(i+1))/2).center(10)\
                                +"|"+str(y_p0[i-1]).center(28)+"|"+str(y_p1[i-1]).center(28)+"\n"

    formatted_output += "-" * 108 + "\n"+"total".center(30) + "|" + "#".center(12) + "|" + "#".center(10) + "|" + \
                        str(acc_p0).center(28) + "|" + str(acc_p1).center(28) +"\n"+ "-" * 108 + "\n"

    if plot:
        plt.grid(True)
        plt.title(u"\\textbf{\Large Générateur :} "+"pire cas".replace("_"," "))
        plt.xlabel(u'\large nombre de nœuds')
        plt.ylabel(u'\large temps (s)')
        coeficients = np.polyfit(n_, y_p0, 2)
        polynom = np.poly1d(coeficients)
        points0, = plt.plot(n_, y_p0, 'g.',label=u'Mesures (joueur 0)')
        fit0, = plt.plot(n_, polynom(n_), 'b--', label=u"Régression polynomiale de degré 2") #\\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))

        coeficients = np.polyfit(n_, y_p1, 2)
        polynom = np.poly1d(coeficients)
        points1, = plt.plot(n_, y_p1, 'r.',label=u'Mesures (joueur 1)')
        fit1, = plt.plot(n_, polynom(n_), 'k--', label=u"Régression polynomiale de degré 2") #\\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))
        plt.legend(loc='upper left', handles=[points0,fit0,points1,fit1])
        plt.savefig(str(n)+"_"+"pirecas"+"_"+".png", bbox_inches='tight')
        plt.clf()

    return formatted_output

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
                regions, strategies = reachability_solver(g, t, p) # solver call
            temp.append(chrono.interval) # add time recording

        y.append(min(temp)) # get the minimum out of #iterations recordings
        n_.append(i)

    if plot:
        plt.grid(True)
        plt.title(u"\\textbf{\Large Générateur :} "+str(generator.__name__).replace("_"," "))
        plt.xlabel(u'\large nombre de nœuds')
        plt.ylabel(u'\large temps (s)')
        coeficients = np.polyfit(n_, y, 2)
        polynom = np.poly1d(coeficients)
        points, = plt.plot(n_, y, 'g.',label=u'Mesures')
        fit, = plt.plot(n_, polynom(n_), 'b--', label=u"Régression polynomiale de degré 2") #\\\\"+str(coeficients[0])+u"$x^2 +$"+str(coeficients[1])+u"x +"+str(coeficients[2]))
        plt.legend(loc='upper left', handles=[points,fit])
        plt.savefig(str(n)+"_"+generator.__name__+"_"+str(p)+".png", bbox_inches='tight')