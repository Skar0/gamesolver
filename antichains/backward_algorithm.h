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

#ifndef BACKWARD_ALGORITHM_H_
#define BACKWARD_ALGORITHM_H_

#include <math.h>
#include "antichain.h"
//#include "bits.h"
//#include "cache.h"
#include "linked_list.h"
//include "safety_game.h"
#include "tuple.h"
#include "graph.h"

extern tuple *NOT_DEFINED;
//extern GHashTable *cache_antichains; //the cache memory used to store computed antichains by the pre_O operator
//extern GHashTable *cache_tuples; //the cache memory used to store computed tuples by the pre_I and pre_I_crit operators

//void set_k_value(tbucw*, int);
antichain* build_start_antichain(graph_p, int, int*);
antichain* fixpoint(graph_p);
int* winning_regions(graph_p);
antichain* pre(antichain*, antichain*, int, graph_p);
static antichain* pre_O(antichain*, antichain*, graph_p);
static antichain* pre_I(antichain*, antichain*, graph_p);
static antichain* pre_1(antichain*, antichain*, graph_p);

//antichain* pre_crit(antichain*, antichain*, int*, alphabet_info*);
//int* compute_critical_set(antichain*, alphabet_info*);

#endif

