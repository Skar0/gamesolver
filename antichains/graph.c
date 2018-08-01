/**
* The code contained in this file was downloaded from
* http://simplestcodings.blogspot.com/2013/09/graphs.html
* Copyright © 2017 Varun Gupta.
*
* This file was modified in july 2018 to create a directed graph
* implementation to be used in Game solver, a python implementation
* of game solving algorithms.
* Copyright (C) 2018 Clément Tamines
*
**/

#include <stdio.h>
#include <stdlib.h>
#include "graph.h"


/* Exit function to handle fatal errors*/
__inline void err_exit(char* msg)
{
    printf("[Fatal Error]: %s \nExiting...\n", msg);
    exit(1);
}

/* Function to create an adjacency list node*/
adjlist_node_p createNode(int v)
{
    adjlist_node_p newNode = (adjlist_node_p)malloc(sizeof(adjlist_node_t));
    if(!newNode)
        err_exit("Unable to allocate memory for new node");

    newNode->vertex = v;
    newNode->next = NULL;

    return newNode;
}

/* Function to create a graph with n vertices; Creates both directed and undirected graphs*/
graph_p createGraph(int n, int *priorities, int* players )
{
    int i;
    graph_p graph = (graph_p)malloc(sizeof(graph_t));
    if(!graph)
        err_exit("Unable to allocate memory for graph");
    graph->num_vertices = n;

    graph->priorities = (int*)malloc(n*sizeof(int));

    for(i=0; i<n; i++) {
        graph->priorities[i] = priorities[i];
    }

    graph->players = (int*)malloc(n*sizeof(int));

    for(i=0; i<n; i++) {
        graph->players[i] = players[i];
    }

    /* Create an array of adjacency lists*/
    graph->succ = (adjlist_p)malloc(n * sizeof(adjlist_t));
    if(!graph->succ)
        err_exit("Unable to allocate memory for adjacency list array");

    graph->pred = (adjlist_p)malloc(n * sizeof(adjlist_t));
    if(!graph->pred)
        err_exit("Unable to allocate memory for adjacency list array");

    for(i = 0; i < n; i++)
    {
        graph->succ[i].head = NULL;
        graph->succ[i].num_members = 0;

        graph->pred[i].head = NULL;
        graph->pred[i].num_members = 0;
    }

    return graph;
}

int* maximal_counter(graph_t *graph) {
    //printf("MAXIMAL COUNTER\n");
    int maximum = -1;
    int c;
    //printf("VERTICES %d\n", graph->num_vertices);
    for (c = 0; c < graph->num_vertices; c++)
    {
       // printf("Max : %d, current : %D", maximum, graph->priorities[c] );
        if (graph->priorities[c] > maximum)
        {
            //printf("rentre dans le update max");
            maximum  = graph->priorities[c];
        }
    }

    //printf("MAX : %d\n", maximum);
    int maxOdd;
    //even max
    if (maximum % 2 == 0) {
        maxOdd = maximum - 1;
    }
    else {
        maxOdd = maximum;
    }
    int nbr_counters = (maxOdd/2)+1;
    //printf("NBR COUNTERS %d\n", nbr_counters);
    int *counters =(int*) calloc(nbr_counters, sizeof(int));


    int i;
    // First are set to the max, max is copied
    for(i=0; i<graph->num_vertices; i++) {
        if(graph->priorities[i] % 2 != 0) {
            counters[graph->priorities[i] /2] = counters[graph->priorities[i] /2] + 1;
        }
    }
    printf("\n");
    return counters;
}

/*Destroys the graph*/
void destroyGraph(graph_p graph)
{
    if(graph)
    {
        if(graph->succ)
        {
            int v;
            /*Free up the nodes*/
            for (v = 0; v < graph->num_vertices; v++)
            {
                adjlist_node_p adjListPtr = graph->succ[v].head;
                while (adjListPtr)
                {
                    adjlist_node_p tmp = adjListPtr;
                    adjListPtr = adjListPtr->next;
                    free(tmp);
                }
            }
            /*Free the adjacency list array*/
            free(graph->succ);
        }

        if(graph->pred)
        {
            int v;
            /*Free up the nodes*/
            for (v = 0; v < graph->num_vertices; v++)
            {
                adjlist_node_p adjListPtr = graph->pred[v].head;
                while (adjListPtr)
                {
                    adjlist_node_p tmp = adjListPtr;
                    adjListPtr = adjListPtr->next;
                    free(tmp);
                }
            }
            /*Free the adjacency list array*/
            free(graph->pred);
        }
        /*Free the graph*/
        free(graph);
    }
}

/* Adds an edge to a graph*/
void addEdge(graph_t *graph, int src, int dest)
{
    /* Add an edge from src to dst in the adjacency list*/
    adjlist_node_p newNode = createNode(dest);
    newNode->next = graph->succ[src].head;
    graph->succ[src].head = newNode;
    graph->succ[src].num_members++;

    newNode = createNode(src);
    newNode->next = graph->pred[dest].head;
    graph->pred[dest].head = newNode;
    graph->pred[dest].num_members++;
}

/* Function to print the adjacency list of graph*/
void displayGraph(graph_p graph)
{
    int i;
    for (i = 0; i < graph->num_vertices; i++)
    {
        adjlist_node_p adjListPtr = graph->succ[i].head;
        printf("%d: ", i);
        while (adjListPtr)
        {
            printf("%d->", adjListPtr->vertex);
            adjListPtr = adjListPtr->next;
        }
        printf("NULL\n");
    }
    printf("--------------------------\n");
    for (i = 0; i < graph->num_vertices; i++)
    {
        adjlist_node_p adjListPtr = graph->pred[i].head;
        printf("%d: ", i);
        while (adjListPtr)
        {
            printf("%d->", adjListPtr->vertex);
            adjListPtr = adjListPtr->next;
        }
        printf("NULL\n");
    }

    for (i = 0; i < graph->num_vertices; i++)
    {
        printf("node %d, priority %d, player %d\n", i, graph->priorities[i], graph->players[i]);
    }
}