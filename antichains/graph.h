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
#ifndef ANTICHAINE_GRAPH_H
#define ANTICHAINE_GRAPH_H

/* Adjacency list node*/
typedef struct adjlist_node
{
    int vertex;                /*Index to adjacency list array*/
    struct adjlist_node *next; /*Pointer to the next node*/
}adjlist_node_t, *adjlist_node_p;

/* Adjacency list */
typedef struct adjlist
{
    int num_members;           /*number of members in the list (for future use)*/
    adjlist_node_t *head;      /*head of the adjacency linked list*/
}adjlist_t, *adjlist_p;

/* Graph structure. A graph is an array of adjacency lists.
   Size of array will be number of vertices in graph*/
typedef struct graph
{
    int num_vertices;         /*Number of vertices*/
    int *priorities;         /*Number of vertices*/
    int *players;         /*Number of vertices*/
    adjlist_p succ;     /*Adjacency lists' array*/
    adjlist_p pred;     /*Adjacency lists' array*/
    //avoir tableau 0,1 en fct du joieur duy noeuid ou bien une liste des noeuds du j1 et une des noeuds du j2 pour optiomiser ? a voir
}graph_t, *graph_p;

void err_exit(char*);
adjlist_node_p createNode(int);
graph_p createGraph(int, int*,int*);
void destroyGraph(graph_p);
void addEdge(graph_t*, int, int);
void displayGraph(graph_p);
int* maximal_counter(graph_t*);

#endif //ANTICHAINE_GRAPH_H




