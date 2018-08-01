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

#include "vector.h"
#include "tuple.h"

/*extern int nb_vector_built;
extern int nb_vector_freed;*/

/** Creates a new vector of dimension d where each component is value **/
vector*
new_vector(int d, int *values, int *max_values) {
    vector *v = (vector*)malloc(sizeof(vector));
    //nb_vector_built++;
    v->dimension = d;
    v->max_values = (int*)malloc(d*sizeof(int));
    v->values = (int*)malloc(d*sizeof(int));
    int i;
    for(i=0; i<d; i++) {
        v->max_values[i] = max_values[i];
        v->values[i] = values[i];
    }

    return v;
}

/** Creates a new vector which is the exact copy of v **/
vector*
clone_vector(vector *v) {
    vector *copy = (vector*)malloc(sizeof(vector));
    //nb_vector_built++;
    copy->dimension = v->dimension;
    copy->max_values = (int*)malloc((copy->dimension)*sizeof(int));
    copy->values = (int*)malloc((copy->dimension)*sizeof(int));
    int i;
    for(i=0; i<copy->dimension; i++) {
        copy->max_values[i] = v->max_values[i];
        copy->values[i] = v->values[i];
    }

    return copy;
}

/** Returns TRUE if for all i, v1[i] <= v2[i], FALSE otherwise **/
char
compare_vectors(vector *v1, vector *v2) {
    int i;
    char smaller = TRUE;
    for(i=0; i<v1->dimension; i++) {
        if(v1->values[i] > v2->values[i]) {
            smaller = FALSE;
            break;
        }
    }
    if(smaller == TRUE) {
        return TRUE;
    }
    return FALSE;
}


/** Returns TRUE if v1[i] = v2[i] for all i, FALSE otherwise **/
char
are_vectors_equal(vector *v1, vector *v2) {
    int i;
    for(i=0; i<v1->dimension; i++) {
        if(v1->values[i] != v2->values[i]) {
            return FALSE;
        }
    }
    return TRUE;
}

/** Compute the intersection of two vectors
    the result is a new vector where each component is the maximum between the corresponding components of v1 and v2 **/
vector*
compute_vectors_intersection(vector *v1, vector *v2) {
    vector *inters = (vector*)malloc(sizeof(vector));
    //nb_vector_built++;
    inters->dimension = v1->dimension;
    inters->max_values = (int*)malloc((inters->dimension)*sizeof(int));
    inters->values = (int*)malloc((inters->dimension)*sizeof(int));
    int i;
    for(i=0; i<inters->dimension; i++) {
        inters->max_values[i] = v1->max_values[i];
        inters->values[i] = MIN(v1->values[i], v2->values[i]);
    }

    return inters;
}

/** Computes the predecessor of v
 	Warning: the omega function is not total and returns NULL when is not defined **/
vector*
vector_omega(vector *v, int priority) {
    vector *result = (vector*)malloc(sizeof(vector));
    result->dimension = v->dimension;
    result->max_values = (int*)malloc((result->dimension)*sizeof(int));
    result->values = (int*)malloc((result->dimension)*sizeof(int));

    int concerned_counter = priority/2;

    if(priority%2== 0) {
        int i;
        // First are set to the max, max is copied
        for(i=0; i<concerned_counter; i++) {
            result->max_values[i] = v->max_values[i];
            result->values[i] = v->max_values[i];
        }
        // Rest is just copying value and max
        for(i; i<result->dimension; i++) {
            result->max_values[i] = v->max_values[i];
            result->values[i] = v->values[i];
        }
    }
    else {
        //Down undefined when counter is 0, else copy counters and decrement the right one
        if (v->values[concerned_counter] == 0) {
            free_vector(result);
            return NULL;
        }
        else {
            int i;
            for(i=0; i<result->dimension; i++) {
                result->max_values[i] = v->max_values[i];
                result->values[i] = v->values[i];
            }
            result->values[concerned_counter] = v->values[concerned_counter] - 1;
        }
    }

    return result;
}

/** Computes the successor of v by adding value to each of its component, with the oplus operator
vector2*
vector_succ(vector2 *v, int *value) {
    vector *result = (vector*)malloc(sizeof(vector));
    //nb_vector_built++;
    result->dimension = v->dimension;
    result->max_values = (int*)malloc((result->dimension)*sizeof(int));
    result->values = (int*)malloc((result->dimension)*sizeof(int));

    int i;
    for(i=0; i<result->dimension; i++) {
        result->max_values[i] = v->max_values[i];
        result->values[i] = oplus(v->values[i], value[i], result->max_values[i]);
    }

    return result;
}
**/
/** Frees the vector **/
void
free_vector(vector *v) {
    //nb_vector_freed++;
    free(v->values);
    free(v->max_values);
    free(v);
}

/** Prints the vector **/
void
print_vector(vector *v) {
    printf("(");
    int i;
    for(i=0; i<v->dimension; i++) {
        printf("%d", v->values[i]);
        if(i != (v->dimension)-1) {
            printf(", ");
        }
    }
    printf(")");
}
