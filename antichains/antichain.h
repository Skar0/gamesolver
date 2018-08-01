/*
 * This file is part of AaPAL, a library for the represention and
 * manipulation of antichains and pseudo-antichains.
 * Copyright (C) 2010-2014 UMONS-ULB
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

/**
 * \file antichain.h
 * \brief Headers of antichain.c
 * \author Aaron Bohy
 * \version 1.1
 */

#ifndef ANTICHAIN_H
#define ANTICHAIN_H

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <glib.h>
#include "linked_list.h"

/* Structures */

/** \struct antichain antichain.h
 *  \brief An antichain is composed of a size and a list of incomparable elements.
 *
 *  Use new_antichain() to create new antichains.
 */
typedef struct {
	int size;
	GSList *incomparable_elements;
} antichain;


/* Function prototypes */
antichain* new_antichain();

void add_element_to_antichain_and_free(antichain*, void*, char (*)(void*, void*), void (*)(void*));
void add_element_to_antichain(antichain*, void*, char (*)(void*, void*));

antichain* compute_antichains_intersection(antichain*, antichain*, char (*)(void*, void*), void* (*)(void*, void*), void* (*)(void*), void (*)(void*));
antichain* compute_antichains_union(antichain*, antichain*, char (*)(void*, void*), void (*)(void*));

antichain* compute_antichains_intersection2(antichain*, antichain*);
antichain* compute_antichains_union2(antichain*, antichain*);

char compare_antichains(antichain*, antichain*, char (*)(void*, void*));
static int* compare_antichains_extended(antichain*, antichain*, char (*)(void*, void*));
char compare_antichains_size(antichain*, antichain*);

char is_antichain_empty(antichain*, char (*)(void*));
char contains_element(antichain*, void*, char (*)(void*, void*));
unsigned long compute_antichain_closure_size(antichain*, int (*)(void*), void* (*)(void*, void*), char (*)(void*, void*), void (*)(void*));

void print_antichain(antichain*, void (*)(void*));
void print_antichain_custom(antichain*, void (*)(void*, void*), void*);

antichain* clone_antichain(antichain*, void* (*)(void*));

void free_antichain(antichain*);
void free_antichain_full(antichain*, void (*)(void*));

#endif
