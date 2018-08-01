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

#ifndef ACACIAPLUS_V2_3_TUPLE_H
#define ACACIAPLUS_V2_3_TUPLE_H

#include <stdlib.h>
#include <stdio.h>
#include <glib.h>
#include "antichain.h"
#include "vector.h"

/** Structures **/
typedef struct {
    //int id;
    int node;
    vector *counters;
} tuple;

tuple *NOT_DEFINED;

/** Function prototypes **/
void set_not_defined_tuple();
tuple* new_tuple(int, vector*);
tuple* build_maximal_tuple(int, int, int*);

tuple* clone_tuple(tuple*);

char is_tuple_empty(tuple*);
char compare_tuples(tuple*, tuple*);
char compare_tuples_reverse(tuple*, tuple*);
char are_tuples_equal(tuple*, tuple*);
unsigned long compute_tuple_closure_size(tuple *);

tuple* compute_tuples_intersection(tuple*, tuple*);


tuple* tuple_omega(tuple*, int, int);
/**
tuple2* tuple_succ(tuple2*, int, alphabet_info*);
antichain* minimal_tuple_succ(tuple2*, alphabet_info*);
antichain* maximal_tuple_succ(tuple2*, alphabet_info*);
**/

void free_tuple(tuple*);
void free_tuple_full(tuple*);
void free_tuple_full_protected(tuple*);
void free_not_defined_tuple();

void print_tuple(tuple*);

#endif //ACACIAPLUS_V2_3_TUPLE2_H