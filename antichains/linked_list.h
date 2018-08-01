/*
 * This file is part of AaPAL, a library for the represention and
 * manipulation of antichains and pseudo-antichains.
 * Copyright (C) 2010-2014 UMONS-ULB
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
 * \file linked_list.h
 * \brief Headers of linked_list.c
 * \author Aaron Bohy
 * \version 1.1
 */

#ifndef LINKED_LIST_H
#define LINKED_LIST_H

#include <stdio.h>
#include <stdlib.h>
#include <glib.h>

/** Function prototypes **/
GSList* remove_last(GSList*);
GSList* remove_first(GSList*);
GSList* scan_add_or_remove(GSList*, void*, char (*)(void*, void*));
GSList* scan_add_or_remove_and_free(GSList*, void*, char (*)(void*, void*), void (*)(void*));
GSList* scan_add_or_remove_and_sort(GSList*, void*, char (*)(void*, void*, char (*)(void*, void*)), char (*)(void*, void*), char (*)(void*, void*));
GSList* scan_add_or_remove_and_sort_and_free(GSList*, void*, char (*)(void*, void*, char (*)(void*, void*)), char (*)(void*, void*), char (*)(void*, void*), void (*)(void*));
GSList* insert_sorted(GSList*, void*, char (*)(void*, void*));
char linked_list_contains_element(GSList*, void*, char (*)(void*, void*));
char is_link_null(GSList*);
void* get_link_data(GSList*);
GSList* clone_linked_list(GSList*, void* (*)(void*));
GSList* clone_linked_list_2(GSList*, void* (*)(void*, void*), void* (*)(void*));
void print_linked_list(GSList*, void* (*)(void*));

#endif

