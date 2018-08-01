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

#include "tuple.h"

/*extern int nb_tuple_built;
extern int nb_tuple_freed;
//extern GSList *t_built;
extern int nb_antichain_built;
extern int nb_antichain_freed;
//extern GSList *a_built;*/

/** Sets the "not defined" tuple that might be returned by tuple_omega **/
void
set_not_defined_tuple() {
    NOT_DEFINED = new_tuple(NULL, NULL);
}

/** Creates a new tuple composed by cf and credits **/
/** Clem : changed counting func to int representing a node **/
tuple*
new_tuple(int node, vector *counters) {
    tuple *t = (tuple*)malloc(sizeof(tuple));
    t->node = node;
    t->counters = counters;

    return t;
}

/** Builds the maximal tuple, i.e. the tuple composed by the maximal counting_function and the credits vector where each component maps 0 **/
/** Clem : max_counters is size dimension*int and contains max val of each counter **/
tuple*
build_maximal_tuple(int node, int dimension, int *max_counters) {
    int *values = (int*)malloc(dimension*sizeof(int));
    int i;
    for(i=0; i<dimension; i++) {
        values[i] = max_counters[i];
    }
    tuple *t = new_tuple(node, new_vector(dimension, values, max_counters));
    free(values);

    return t;
}


/** Creates a new tuple which is the exact copy of t **/
tuple*
clone_tuple(tuple *t) {
    int node_copy = t->node;
    return new_tuple(node_copy, clone_vector(t->counters));
}


/** Returns TRUE if t1->cf <= t2->cf and t1->c_i >= t2->c_i, forall 0<=i<dimension, FALSE otherwise **/
char
compare_tuples(tuple *t1, tuple *t2) {
    if (t1->node == t2->node) {
        if (compare_vectors(t1->counters, t2->counters) == TRUE) {
            return TRUE;
        }
    }
    return FALSE;
}


/** Returns TRUE if t2->cf <= t1->cf and t2->c_i >= t1->c_i, forall 0<=i<dimension, FALSE otherwise **/
char
compare_tuples_reverse(tuple *t1, tuple *t2) {
    return compare_tuples(t2, t1);
}

/** Returns TRUE if t1 and t2 are equal, FALSE otherwise **/
char
are_tuples_equal(tuple *t1, tuple *t2) {
    if (t1->node == t2->node) {
        if (are_vectors_equal(t1->counters, t2->counters) == TRUE) {
            return TRUE;
        }
    }
    return FALSE;
}

/** Computes the number of tuples t' such that t' <= t
unsigned long
compute_tuple_closure_size(tuple2* t) {
    return compute_vector_closure_size(t->counters);
}
**/

/** Computes the predecessor of the tuple for label indexed label_index in sigma
 	Warning: the omega function is not total and returns the special NOT_DEFINED tuple when is not defined **/
tuple*
tuple_omega(tuple *t, int priority, int pred) {

    vector *result_vector = vector_omega(t->counters, priority);
    int node = t->node;
    if (result_vector != NULL) {
        new_tuple(pred,result_vector);
    }
    else {
        return NOT_DEFINED;
    }

}

/** Computes the intersection of two tuples
    the result is the intersection of the counting_functions and the maximal of credits vectors (component-wize) **/
tuple*
compute_tuples_intersection(tuple *t1, tuple *t2) {
    /**
    printf("Trying to max_elem between\n");
    print_tuple(t1);
    printf("\n");
    print_tuple(t2);
    printf("~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
    **/
    if (t1->node == t2->node) {
        return new_tuple(t1->node, compute_vectors_intersection(t1->counters, t2->counters));

    } else
    {
        return NOT_DEFINED;
    }
}

/** Computes the antichain of minimal successor of tuple t for all sigma in the player alphabet
antichain*
minimal_tuple_succ(tuple2 *t, alphabet_info *alphabet) {
    GSList *minimal_elements = NULL;
    int sigma_size, i;
    if(t->cf->player == P_O) {
        sigma_size = alphabet->sigma_output_size;
    }
    else {
        sigma_size = alphabet->sigma_input_size;
    }

    tuple *cur_succ;
    for(i=0; i<sigma_size; i++) {
        cur_succ = tuple_succ(t, i, alphabet);
        minimal_elements = scan_add_or_remove_and_free(minimal_elements, cur_succ, (void*)compare_tuples_reverse, (void*)free_tuple_full);
    }

    antichain* minimal_succ = (antichain*)malloc(sizeof(antichain));
    minimal_succ->size = g_slist_length(minimal_elements);
    minimal_succ->incomparable_elements = minimal_elements;
    //nb_antichain_built++;
    //a_built = g_slist_append(a_built, GINT_TO_POINTER(nb_antichain_built));
    //minimal_succ->id = nb_antichain_built;
    return minimal_succ;
}
**/
/** Computes the antichain of maximal successor of tuple t for all sigma in the player alphabet
antichain*
maximal_tuple_succ(tuple2 *t, alphabet_info *alphabet) {
    GSList *maximal_elements = NULL;
    int sigma_size, i;
    if(t->cf->player == P_O) {
        sigma_size = alphabet->sigma_output_size;
    }
    else {
        sigma_size = alphabet->sigma_input_size;
    }

    tuple *cur_succ;
    for(i=0; i<sigma_size; i++) {
        cur_succ = tuple_succ(t, i, alphabet);
        maximal_elements = scan_add_or_remove_and_free(maximal_elements, cur_succ, (void*)compare_tuples, (void*)free_tuple_full);
    }

    antichain* maximal_succ = (antichain*)malloc(sizeof(antichain));

    maximal_succ->size = g_slist_length(maximal_elements);
    maximal_succ->incomparable_elements = maximal_elements;
    //nb_antichain_built++;
    //a_built = g_slist_append(a_built, GINT_TO_POINTER(nb_antichain_built));
    //maximal_succ->id = nb_antichain_built;
    return maximal_succ;
}
**/
/** Frees the tuple **/
void
free_tuple(tuple *t) {
    //t_built = g_slist_remove(t_built, GINT_TO_POINTER(t->id));
    free_vector(t->counters);
    free(t);
    //nb_tuple_freed++;
}

/** Frees the tuple and the counting_function **/
void
free_tuple_full(tuple *t) {
    free_tuple(t);
}

/** Frees the tuple t with the free_tuple_full function if t is not the special tuple NOT_DEFINED **/
void
free_tuple_full_protected(tuple *t) {
    if(t != NOT_DEFINED) {
        free_tuple_full(t);
    }
}

/** Frees the NOT_DEFINED tuple **/
void
free_not_defined_tuple() {
    //t_built = g_slist_remove(t_built, GINT_TO_POINTER(NOT_DEFINED->id));
    free(NOT_DEFINED);
    //nb_tuple_freed++;
}

/** Prints the tuple **/
void
print_tuple(tuple *t) {
    if(t != NOT_DEFINED) {
        printf("[");
        printf("%d ,", t->node);
        print_vector(t->counters);
        printf("]");
    }
    else {
        printf("[NOT DEFINED TUPLE]");
    }
}
