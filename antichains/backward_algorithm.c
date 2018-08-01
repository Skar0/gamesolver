/*
 * This file is part of Acacia+, a tool for synthesis of reactive systems using antichain-based techniques
 * Copyright (C) 2011-2013 UMONS-ULB
 *
 * This file was modified in july 2018 to allow the use of antichains in
 * Game solver, a python implementation of game solving algorithms.
 * Copyright (C) 2018 Clément Tamines
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#include "backward_algorithm.h"
#include "antichain.h"
#include "tuple.h"
#include "graph.h"
#include "vector.h"

/*extern int nb_antichain_built;
extern int nb_antichain_freed;*/
//extern GSList *a_built;
int*
winning_regions(graph_p graph) {
    antichain *fix = fixpoint(graph);
    int *regions =(int*) calloc(graph->num_vertices, sizeof(int));

    tuple *tup;
    int node;
    GSList *curlink = fix->incomparable_elements;
    while(curlink != NULL) {
        tup = (tuple*) curlink->data;
        node = tup->node;
        regions[node] = 1;
        curlink = curlink->next;
    }
    return regions;
}

/** Builds the initial antichain for the fix point computation where player starts **/
antichain*
fixpoint(graph_p graph) {

    int print = 0;

    antichain *start_antichain;

    int *max_counters = maximal_counter(graph);

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

    /**
    if (maxOdd == 11) {
        print = 1;
    }
    **/
    //printf("MAX COUNTER SIZE %d MAX ODD %d\n",nbr_counters, maxOdd);


    //change 2 to size of counters
    start_antichain = build_start_antichain(graph, nbr_counters, max_counters);
    if (print==1 ) {
        printf("Start antichain : ");
        print_antichain(start_antichain, (void *) print_tuple);
        printf("\n");
    }

    antichain *a1;

    a1 = start_antichain;

    antichain *pre_1 = pre(start_antichain, start_antichain, 1, graph);
    if (print) {
    printf("Pre 1 of start ");
    print_antichain(pre_1, (void *) print_tuple);
    printf("\n");
    }
    antichain *pre_0 = pre(start_antichain, start_antichain, 0, graph);
    if (print) {
        printf("Pre 0 of start ");
        print_antichain(pre_0, (void *) print_tuple);
        printf("\n");
    }

    //Here we should union the antichain efficiently, because we know the nodes to be incomparable, this is TODO

    antichain* temp = compute_antichains_union2(pre_1, pre_0);

    if (print) {
        printf("Union of Pre 0 and Pre 1 ");
        print_antichain(temp, (void *) print_tuple);
        printf("\n");
    }

    antichain* a2 = compute_antichains_intersection2(a1, temp);

    if (print) {
        printf("Inter of start and previous Union  ");
        print_antichain(a2, (void *) print_tuple);
        printf("\n");
    }
    int nb_iter = 0;
            //Iterate while the fix point isn't reached
    while (!compare_antichains(a1, a2,(void*)compare_tuples)) {
        nb_iter += 1;
        a1 = a2;
        pre_1 = pre(a1, a1, 1, graph);
        if(print) {
            printf("ITER %d Pre 1 of prev ",nb_iter);
            print_antichain(pre_1, (void *) print_tuple);
            printf("\n");
        }
        pre_0 = pre(a1, a1, 0, graph);
        if(print) {
            printf("ITER %d Pre 0 of prev ",nb_iter);
            print_antichain(pre_0, (void *) print_tuple);
            printf("\n");
        }
        temp = compute_antichains_union2(pre_0, pre_1);
        if (print) {
            printf("Union of Pre 0 and Pre 1 ");
            print_antichain(temp, (void *) print_tuple);
            printf("\n");
        }
        a2 = compute_antichains_intersection2(a1, temp);
        if( print) {
            printf("ITER %d final set ",nb_iter);
            print_antichain( a2 , (void *) print_tuple);
            printf("\n");
        }
    }

    return a1;
}
/** Builds the initial antichain for the fix point computation where player starts **/
antichain*
build_start_antichain(graph_p graph, int dimension, int *max_counters) {
	antichain* a_init = (antichain*)malloc(sizeof(antichain));
	a_init->size = 0;
	GSList *list = NULL;
    int i;
    for(i=0; i<graph->num_vertices; i++) {
        list = g_slist_append(list, build_maximal_tuple(i, dimension, max_counters));
        a_init->size += 1;
    }
	a_init->incomparable_elements = list;

	return a_init;
}

/** Calls pre_O or pre_I function according to the player value **/
antichain*
pre(antichain* a, antichain* prev_a, int player, graph_p graph) {
	if(player == 0) {
		return pre_O(a, prev_a, graph);
	}
	else {
		return pre_1(a, prev_a, graph);
	}
}
static antichain*
pre_I(antichain* a, antichain* prev_a, graph_p graph) {
    // If the antichain is empty, the fix point is reached
    if(a->incomparable_elements == NULL) {
        return clone_antichain(a, (void*)clone_tuple);
    }

    antichain *cur_antichain = new_antichain();

    GSList *curlink = a->incomparable_elements;

    tuple *tup;
    tuple *down;
    int node;
    int pred;
    int i;
    int *toremove = (int*) calloc(graph->num_vertices, sizeof(int));
    while(curlink != NULL) {
        //curlink is a tuple of the antichain
        // get the node corresponding to the tuple
        tup = (tuple*) curlink->data;
        node = tup->node;
        //get predecessors of node
        adjlist_node_p adjListPtr = graph->pred[node].head;
        // Go trough predecessors
        while (adjListPtr)
        {
            // current predecessor
            pred = adjListPtr->vertex;

            // only consider predecessors that belong to player 1 (0) not 2 (1)
            if(graph->players[pred] == 1) {
                //need to compute predecessor with priority of node pred, node is node pred and counters is computed by tuple_omega
                /**
                if(node == 5 ) {
                    printf("%d, %d, %d\n", tup->counters->values[0], tup->counters->values[1], pred);
                }
                **/
                down = tuple_omega(tup,graph->priorities[pred], pred);
                /**
                if(node == 5 ) {
                    printf("Node %d, %d, %d\n",  down->node, down->counters->values[0], down->counters->values[1]);
                }
                **/
                if (!(down == NOT_DEFINED)) {
                        /**
                        if(node == 5 ) {
                               printf("AJOUT ANTICHAIN - ");
                               printf("Node %d, %d, %d\n",  down->node, down->counters->values[0], down->counters->values[1]);
                        }
                        **/
                    add_element_to_antichain_and_free(cur_antichain, down, (void*)compare_tuples, (void*)free_tuple_full);
                }
                else {
                    toremove[pred] = 1;
                }
            }

            adjListPtr = adjListPtr->next;
        }
        /**
        int i;
        //on teste chaque pred du noeud correspondant au tuple
        for(i=0; i<graph->num_vertices; i++) {
            printf("-%d-\n", max_count[i]);
        }
         **/
        curlink = curlink->next;
    }

    //remove nodes (v,m) where toremove[v] est vrai ie un underflow pour ce v

    GSList *removeLink = cur_antichain->incomparable_elements;
    antichain *before_inter_antichain = new_antichain();
    while(removeLink != NULL) {
        tup = (tuple*) removeLink->data;
        if(toremove[tup->node] == 0) {
            add_element_to_antichain_and_free(before_inter_antichain, tup, (void*)compare_tuples, (void*)free_tuple_full);
        }
        removeLink = removeLink->next;
    }

    antichain *inter_antichains =  compute_antichains_intersection(before_inter_antichain,    clone_antichain(before_inter_antichain, (void*)clone_tuple)
    ,(void*)compare_tuples,(void*)compute_tuples_intersection, (void*)clone_tuple, (void*)free_tuple_full);

    return inter_antichains;
}

static antichain *
pre_1(antichain *a, antichain *prev_a, graph_p graph) {
    // If the antichain is empty, the fix point is reached
    if (a->incomparable_elements == NULL) {
        return clone_antichain(a, (void *) clone_tuple);
    }

    antichain *cur_antichain = new_antichain();

    antichain *temp1 = new_antichain();
    antichain *temp2 = new_antichain();

    tuple *tup;
    tuple *down;
    int node;
    int succ;
    int i;
    //pour chaque noeud du joeur 2
    for (i = 0; i < graph->num_vertices; i++) {
        if (graph->players[i] == 1) {
            //printf("Node %d player %d\n",i,graph->players[i] );
            //pour chaque successuer
            adjlist_node_p adjListPtr = graph->succ[i].head;
            int first_iter = 0;

            while (adjListPtr) {
                succ = adjListPtr->vertex;

                //on considère ce succ et on applique down sur l'ensemble des noeuds (v,m) de l'anti ou v est le succ considere ici
                GSList *curlink = a->incomparable_elements;
                temp1 = new_antichain();
                while (curlink != NULL) {

                    tup = (tuple *) curlink->data;
                    node = tup->node;
                    //si le v est correct, ajoute a l'antichain donc d'abord on down
                    if (node == succ) {
                            /**
                            if(i == 5 ) {
                               printf("CHECK - considering node %d ", succ);
                               printf("Node %d, %d, %d\n",  tup->node, tup->counters->values[0], tup->counters->values[1]);
                            }
                            **/
                        down = tuple_omega(tup, graph->priorities[i], i);
                        if (!(down == NOT_DEFINED)) {
                            /**
                            if(i == 5 ) {
                               printf("AJOUT ANTICHAIN - ");
                               printf("Node %d, %d, %d\n",  down->node, down->counters->values[0], down->counters->values[1]);
                            }

                            printf("AJOUT ANTICHAIN - ");
                               printf("Node %d, %d, %d, %d, %d, %d, %d\n",  down->node, down->counters->values[0], down->counters->values[1],  down->counters->values[2], down->counters->values[3],  down->counters->values[4], down->counters->values[5]);
                            **/
                            add_element_to_antichain_and_free(temp1, down, (void *) compare_tuples,
                                                              (void *) free_tuple_full);
                        }
                        /**
                        Il peut y avoir un non defini pas ajoute et un defini dasn cet ensemble. avoir un non def veut pas dire que l'ensemble ne contient que des non deifnis
                                 c'est seulement si un des ensemble temp est vide car il ne contient QUE des non def que ca foire.
                           else {
                            //Temp1 vide l'inter sera toujours vide
                            temp1 = new_antichain();
                            break;
                        }
                        **/

                    }
                    curlink = curlink->next;
                }
                if(first_iter == 0) {
                    temp2 = clone_antichain(temp1,(void *) clone_tuple);
                    first_iter = 1;
                }
                else {
                       //seulement si un des sets de l'inter donc un des temp est vide alors le tout est vide
                    temp2 = compute_antichains_intersection(temp2,   temp1
                            ,(void*)compare_tuples,(void*)compute_tuples_intersection, (void*)clone_tuple, (void*)free_tuple_full);
                }

                adjListPtr = adjListPtr->next;
            }

            cur_antichain = compute_antichains_union(cur_antichain, temp2, (void*)compare_tuples, (void*)free_tuple_full);

        }

    }
    return cur_antichain;
}
static antichain*
pre_O(antichain* a, antichain* prev_a, graph_p graph) {
    // If the antichain is empty, the fix point is reached
    if(a->incomparable_elements == NULL) {
        return clone_antichain(a, (void*)clone_tuple);
    }

    antichain *cur_antichain = new_antichain();

    GSList *curlink = a->incomparable_elements;

    tuple *tup;
    tuple* down;
    int node;
    int pred;
    int i;
    while(curlink != NULL) {
        //curlink is a tuple of the antichain
        // get the node corresponding to the tuple
        tup = (tuple*) curlink->data;
        node = tup->node;
        //get predecessors of node
        adjlist_node_p adjListPtr = graph->pred[node].head;
        // Go trough predecessors
        while (adjListPtr)
        {
            // current predecessor
            pred = adjListPtr->vertex;

            // only consider predecessors that belong to player 1 (0) not 2 (1)
            if(graph->players[pred] == 0) {
                //need to compute predecessor with priority of node pred, node is node pred and counters is computed by tuple_omega
                down = tuple_omega(tup,graph->priorities[pred], pred);
                if (!(down == NOT_DEFINED)) {
                    add_element_to_antichain_and_free(cur_antichain, down, (void*)compare_tuples, (void*)free_tuple_full);
                }
            }

            adjListPtr = adjListPtr->next;
        }
        /**
        int i;
        //on teste chaque pred du noeud correspondant au tuple
        for(i=0; i<graph->num_vertices; i++) {
            printf("-%d-\n", max_count[i]);
        }
         **/
        curlink = curlink->next;
    }

    return cur_antichain;
}


/** Computes the function Pre_O(a)
 	prev_a is the last antichain of P_O computed
 	Uses a cache memory to prevent to recompute already computed antichains
static antichain*
pre_O(antichain* a, antichain* prev_a, alphabet_info *alphabet) {
	// If the antichain is empty, the fix point is reached
    if(a->incomparable_elements == NULL) {
		return clone_antichain(a, (void*)clone_tuple);
    }

    antichain *pre, *cur_antichain;
    tuple *cur_omega;
    GSList *curlink = a->incomparable_elements;
    int j, sigma_size = alphabet->sigma_output_size;
    char first_iteration = TRUE;
    LABEL_BIT_REPRES **sigma = alphabet->sigma_output;

	while(curlink != NULL) {
		//Check whether we have already computed the antichain of predecessors for curlink->data
		cur_antichain = (antichain*)get_from_cache(cache_antichains, curlink->data, -1);
		if(cur_antichain == NULL) { //cache miss -> compute cur_antichain
			cur_antichain = new_antichain();
			for(j=0; j<sigma_size; j++) {
				cur_omega = tuple_omega((tuple*)(curlink->data), j, sigma);

				if(cur_omega != NOT_DEFINED) {
					//Add to cur_antichain
					add_element_to_antichain_and_free(cur_antichain, cur_omega, (void*)compare_tuples, (void*)free_tuple_full);
				}
			}
			add_to_cache(cache_antichains, clone_tuple(curlink->data), -1, (void*)cur_antichain); //add the computed antichain to cache
		}

		if(first_iteration == TRUE) {
			//Clone the antichain because cur_antichain (which is stored in cache) must be a constant pointer (constant = never modified)
			pre = clone_antichain(cur_antichain, (void*)clone_tuple);
			first_iteration = FALSE;
		}
		else {
			pre = compute_antichains_union(pre, clone_antichain(cur_antichain, (void*)clone_tuple), (void*)compare_tuples, (void*)free_tuple_full);
		}
		curlink = curlink->next;
	}

    antichain *inters = compute_antichains_intersection(pre, prev_a, (void*)compare_tuples, (void*)compute_tuples_intersection, (void*)clone_tuple, (void*)free_tuple_full);
    free_antichain_full(pre, (void*)free_tuple_full);

    return inters;
}
**/

/** Computes the function Pre_I(a)
 	prev_a is the last antichain of P_I computed
 	Uses a cache memory to prevent to recompute already computed omega
static antichain*
pre_I(antichain* a, antichain* prev_a, alphabet_info *alphabet) {
	// If the antichain is empty, the fix point is reached
	if(a->incomparable_elements == NULL) {
		return clone_antichain(a, (void*)clone_tuple);
	}

	antichain *pre, *cur_antichain;
	tuple *cur_omega;
	GSList *antichains_list = NULL;
	GSList *curlink;
	int i, sigma_size = alphabet->sigma_input_size;
	LABEL_BIT_REPRES **sigma = alphabet->sigma_input;

	for(i=0; i<sigma_size; i++) {
		cur_antichain = new_antichain();
		curlink = a->incomparable_elements;
		while(curlink != NULL) {
			//Check whether we have already computed omega for curlink->data and sigma i
			cur_omega = (tuple*)get_from_cache(cache_tuples, curlink->data, i);
			if(cur_omega == NULL) { //cache miss
				cur_omega = tuple_omega(curlink->data, i, sigma);
				add_to_cache(cache_tuples, clone_tuple(curlink->data), i, (void*)cur_omega); //add the computed tuple to cache
			}
			if(cur_omega != NOT_DEFINED) {
				//Add to cur_antichain
				add_element_to_antichain(cur_antichain, cur_omega, (void*)compare_tuples); // no need to free as all omega computed are stored in cache
			}
			curlink = curlink->next;
		}
		antichains_list = scan_add_or_remove_and_sort_and_free(antichains_list, cur_antichain, (void*)compare_antichains, (void*)compare_tuples, (void*)compare_antichains_size, (void*)free_antichain);
	}
	if(antichains_list != NULL) {
		antichain* prev_pre;
		pre = clone_antichain(antichains_list->data, (void*)clone_tuple);
		free_antichain(antichains_list->data);
		curlink = antichains_list->next;
		while(curlink != NULL) {
			prev_pre = pre;
			pre = compute_antichains_intersection(prev_pre, curlink->data, (void*)compare_tuples, (void*)compute_tuples_intersection, (void*)clone_tuple, (void*)free_tuple_full);
			free_antichain(curlink->data);
			free_antichain_full(prev_pre, (void*)free_tuple_full);
			curlink = curlink->next;
		}
		g_slist_free(antichains_list);
	}
	else { // impossible (?)
		printf("antichains_list empty!!!");
	}

	return pre;
}
**/
/** Computes the function Pre_crit(a) (critical signals optimization) where critical_signals_index is the set of critical
    signals for a (the first element of the array is the number of critical signals)
    prev_a is the last antichain of the input computed
 	Uses a cache memory to prevent to recompute already computed omega
antichain*
pre_crit(antichain* a, antichain* prev_a, int *critical_signals_index, alphabet_info *alphabet) {
	int nb_critical_signals = critical_signals_index[0];

    // If the set of critical signal or the antichain is empty, the fixpoint is reached
    if(nb_critical_signals == 0 || a->incomparable_elements == NULL) {
    	return clone_antichain(prev_a, (void*)clone_tuple);
    }

    antichain *pre, *cur_antichain;
    tuple *cur_omega;
    GSList *antichains_list = NULL;
    GSList *curlink;
    int i;
    LABEL_BIT_REPRES **sigma = alphabet->sigma_input;

	for(i=1; i<=nb_critical_signals; i++) {
		cur_antichain = new_antichain();
		curlink = a->incomparable_elements;
		while(curlink != NULL) {
			//Check whether we have already computed omega for curlink->data and sigma i
			cur_omega = (tuple*)get_from_cache(cache_tuples, curlink->data, critical_signals_index[i]);
			if(cur_omega == NULL) { //cache miss
				cur_omega = tuple_omega(curlink->data, critical_signals_index[i], sigma);
				add_to_cache(cache_tuples, clone_tuple(curlink->data), critical_signals_index[i], (void*)cur_omega); //add the computed tuple to cache
			}
			if(cur_omega != NOT_DEFINED) {
				//Add to antichain
				add_element_to_antichain(cur_antichain, cur_omega, (void*)compare_tuples); // no need to free as all omega computed are stored in cache
			}
			curlink = curlink->next;
		}
		antichains_list = scan_add_or_remove_and_sort_and_free(antichains_list, cur_antichain, (void*)compare_antichains, (void*)compare_tuples, (void*)compare_antichains_size, (void*)free_antichain);
	}

	if(antichains_list != NULL) {
		antichain* prev_pre;
		pre = clone_antichain(antichains_list->data, (void*)clone_tuple);
		free_antichain(antichains_list->data);
		curlink = antichains_list->next;
		while(curlink != NULL) {
			prev_pre = pre;
			pre = compute_antichains_intersection(prev_pre, curlink->data, (void*)compare_tuples, (void*)compute_tuples_intersection, (void*)clone_tuple, (void*)free_tuple_full);
			free_antichain(curlink->data);
			free_antichain_full(prev_pre, (void*)free_tuple_full);
			curlink = curlink->next;
		}
		g_slist_free(antichains_list);
	}
	else { // impossible (?)
		printf("antichains_list empty!!!");
	}

	return pre;
}
**/
/** Critical input signals optimization: Computes a minimal critical set of inputs signals for antichain
    For each element f of antichain, for each symbol s_O of the output alphabet, find a critical input signal,
    i.e. a signal s_I s.t. succ(succ(f, s_O), s_I) does not belong to antichain (+ privilege already added signals to try to minimize the set)
    Stops when the critical signals for one one-step-loosing tuple is found
int*
compute_critical_set(antichain *a, alphabet_info *alphabet) {
//  Note: local cache memories optimization disabled since it seems less efficient
//	GHashTable *cache_lvl1 = g_hash_table_new_full(hash_key, compare_keys, (GDestroyNotify)free_hash_table_key, NULL); //cache memory used to avoid redondant computation (for the successors of t)
//	GHashTable *cache_lvl2 = g_hash_table_new_full(hash_key, compare_keys, (GDestroyNotify)free_hash_table_key, NULL); //cache memory used to avoid redondant computation (for the successors of the successors of t)

	char found, inC, is_one_step_loosing, is_in_antichain;
	//char *info_lvl1, *info_lvl2;
	//char *true_value = (char*)malloc(sizeof(char));
	//true_value[0] = TRUE;
	//char *false_value = (char*)malloc(sizeof(char));
	//false_value[0] = FALSE;

	int i, input_size = alphabet->sigma_input_size;
	tuple *t, *succ_t, *succ_succ_t;
	antichain *min_succ;

	int* c = (int*)malloc((input_size+1)*sizeof(int)); //array of critical signals index in the input alphabet
	char* c_bool = (char*)malloc((input_size)*sizeof(char)); //array of booleans representing the critical set on a boolean format
	int* curC = (int*)malloc((input_size+1)*sizeof(int)); //array of signals found to be critical till here and for t (will be added to c only if t is one step loosing)
	char* curC_bool = (char*)malloc((input_size)*sizeof(char)); //c_bool but on a boolean format

	// Initialize c and c_bool
	c[0] = 0;
	for(i=0; i<input_size; i++) {
		c[i+1] = -1;
		c_bool[i] = FALSE;
	}

	GSList *succ_t_link, *cur_link = a->incomparable_elements;
	while(cur_link != NULL) { //for each element t of the antichain
		t = cur_link->data;

		//Copy c and c_bool in curC and curC_bool
		curC[0] = c[0];
		for(i=0; i<input_size; i++) {
			curC[i+1] = c[i+1];
			curC_bool[i] = c_bool[i];
		}

		is_one_step_loosing = TRUE;
		min_succ = (antichain*)get_from_cache(cache_min_succ, t, -1);
		if(min_succ == NULL) { //cache miss
			min_succ = minimal_tuple_succ(t, alphabet); //compute the antichain of minimal successors of t (no need of analyzing non minimal successors)
			add_to_cache(cache_min_succ, clone_tuple(t), -1, (void*)min_succ); //add the computed antichain to cache
		}
		succ_t_link = min_succ->incomparable_elements;
		while(succ_t_link != NULL) { //for all succ of t s.t. succ is minimal
			found = FALSE; //will be set to TRUE if a critical s_I is found for t
			inC = FALSE; //will be set to True if the critical signal s_I found has already been for another t or min_succ
			//succ_t = clone_tuple(succ_t_link->data); // Cloning is mandatory with local caching
			succ_t = succ_t_link->data;

			//Seek on cache if succ_t has already been processed, i.e. if we have already checked if there exists a s_I s.t. succ(succ_t, s_I) does not belong to the antichain
			//info_lvl1 = get_from_cache(cache_lvl1, succ_t, -1); //attempt to retrieve data from cache_lvl1
			//if(info_lvl1 == NULL) { //cache miss
				for(i=1; i<=curC[0]; i++) { //for s_I in c (privilege already added signals)
					succ_succ_t = (tuple*)get_from_cache(cache_succ, succ_t, curC[i]);
					if(succ_succ_t == NULL) { // cache miss
						succ_succ_t = tuple_succ(succ_t, curC[i], alphabet);
						add_to_cache(cache_succ, clone_tuple(succ_t), curC[i], (void*)succ_succ_t); //add the computed succ to cache
					}

					//Seek on cache if succ_succ_t has already been processed
					//info_lvl2 = get_from_cache(cache_lvl2, succ_succ_t, -1); //attempt to retrieve data from cache_lvl2
					//if(info_lvl2 == NULL) { //cache miss
						is_in_antichain = contains_element(a, succ_succ_t, (void*)compare_tuples);


					if(is_in_antichain == FALSE) {
						inC = TRUE;
						break;
					}
				}

				if(inC == FALSE) { //if not found yet
					for(i=0; i<input_size; i++) { //for s_I in input alphabet
						if(curC_bool[i] == FALSE) { //if s_I does not belong to curC (otherwise it has already been tested)
							succ_succ_t = (tuple*)get_from_cache(cache_succ, succ_t, i);
							if(succ_succ_t == NULL) { // cache miss
								succ_succ_t = tuple_succ(succ_t, i, alphabet);
								add_to_cache(cache_succ, clone_tuple(succ_t), i, (void*)succ_succ_t); //add the computed succ to cache
							}

							//Seek on cache if succ_succ_t has already been processed
							//info_lvl2 = get_from_cache(cache_lvl2, succ_succ_t, -1); //attempt to retrieve data from cache_lvl2
							//if(info_lvl2 == NULL) { //cache miss
								is_in_antichain = contains_element(a, succ_succ_t, (void*)compare_tuples);


							if(is_in_antichain == FALSE) {
								found = TRUE; //there exists a s_I s.t. succ(succ(f, s_O), s_I) does not belong to antichain
								curC[0] = curC[0]+1; //increment the number of critical signals
								curC[curC[0]] = i; //add s_I to curC
								curC_bool[i] = TRUE; //set the boolean of s_I to True
								break;
							}
						}
					}
				}

				if(found == FALSE && inC == FALSE) { //there exists a s_O s.t. for all s_I succ(succ(t, s_O), s,I) belongs to antichain -> t is not one step loosing
					is_one_step_loosing = FALSE;
				}

			if(is_one_step_loosing == FALSE) {
				break; //not one step loosing -> skip to the next t
			}

			succ_t_link = succ_t_link->next;
		}

		//free_antichain_full(min_succ, (void*)free_tuple_full); // Not freed here because min_succ is added in cache (will be freed at the end on the fix point computation)

		// If f is one step loosing, add signals in curC to c
		if(is_one_step_loosing == TRUE) {
			c[0] = curC[0];
			for(i=0; i<input_size; i++) {
				c[i+1] = curC[i+1];
				c_bool[i] = curC_bool[i];
			}
			break; //break here because we found critical signals for one one-step-loosing tuple (enough)
		}

		cur_link = cur_link->next;
	}
	free(c_bool);
	free(curC);
	free(curC_bool);
//	free(true_value);
//	free(false_value);

//	g_hash_table_destroy(cache_lvl1);
//	g_hash_table_destroy(cache_lvl2);

	return c;
}

**/