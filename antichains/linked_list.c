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
 * \file linked_list.c
 * \brief Custom functions for the manipulation of GSLists of glib.h
 * \author Aaron Bohy
 * \version 1.1
 */

#include "linked_list.h"

/** \brief Removes the last link of a GSList.
 *  \param a_list a GSList
 *  \return the new start of the list with last link removed.
 *
 *	Warning: it does not free the data contained into the removed link
 */
GSList*
remove_last(GSList *a_list) {
	GSList *last = g_slist_last(a_list);
	if(last != NULL) {
		a_list = g_slist_delete_link(a_list, last); //removes and frees the last link from a_list
	}
	return a_list;
}

/** \brief Removes the first link of a GSList.
  * \param a_list a GSList
  * \return the new start of the list with first link removed
  *
  *	Warning: it does not free the data contained into the removed link
  */
GSList*
remove_first(GSList *a_list) {
	if(a_list != NULL) {
		a_list = g_slist_delete_link(a_list, a_list); //removes and frees the first link from a_list
	}
	return a_list;
}

/** \brief Function for the manipulation of GSLists of incomparable data (called elements).
 *  \param a_list a GSList containing incomparable elements
 *  \param data an element to add to a_list
 *  \param compare the function to compare the elements
 *  \return the new first link of a_list
 *
 *  Scans the GSList.
 *  Removes links which contain data d such that d <= data (according to compare).
 *  Adds a link containing data if there is no d in a_list such that data <= d.
 *  Returns the first link of the resulting GSList.
 *  Warning: it does not free the elements removed from a_list or data when it is not added to a_list.
 *  If this is not what you want, see scan_add_or_remove_and_free.
 */
GSList*
scan_add_or_remove(GSList *a_list, void* data, char (*compare)(void*, void*)) {
	GSList *links_to_remove = NULL;
	GSList *current_link = a_list;
	int is_maximal = TRUE, diff_nb_links = 0;
	while(current_link != NULL) {
		if(compare(data, current_link->data) == TRUE) {
			is_maximal = FALSE;
			break;
		}
		else if(compare(current_link->data, data) == TRUE) {
			links_to_remove = g_slist_append(links_to_remove, current_link);
		}
		current_link = current_link->next;
	}
	if(is_maximal == TRUE) {
		current_link = links_to_remove;
		while(current_link != NULL) {
			a_list = g_slist_delete_link(a_list, current_link->data);
			current_link = current_link->next;
			diff_nb_links--;
		}
		a_list = g_slist_append(a_list, data);
		diff_nb_links++;
	}

	g_slist_free(links_to_remove);
	return a_list;
}

/** \brief Function for the manipulation of GSLists of incomparable data (called elements).
 *  \param a_list a GSList containing incomparable elements
 *  \param data an element to add to a_list
 *  \param compare the function to compare the elements
 *  \param free_element the function to free the elements
 *  \return the new first link of a_list
 *
 *  Scans the GSList.
 *  Removes links which contain data d such that d <= data (according to compare).
 *  Adds a link containing data if there is no d in a_list such that data <= d.
 *  Returns the first link of the resulting GSList.
 *  Frees each element removed from a_list and data if it is not added to a_list.
 *  If you do not want those removed elements to be freed, use scan_add_or_remove.
 */
GSList*
scan_add_or_remove_and_free(GSList *a_list, void* data, char (*compare)(void*, void*), void (*free_element)(void*)) {
	GSList *links_to_remove = NULL;
	GSList *current_link = a_list;
	int is_maximal = TRUE, diff_nb_links = 0;
	while(current_link != NULL) {
		if(compare(data, current_link->data) == TRUE) {
			is_maximal = FALSE;
			break;
		}
		else if(compare(current_link->data, data) == TRUE) {
			links_to_remove = g_slist_append(links_to_remove, current_link);
		}
		current_link = current_link->next;
	}
	if(is_maximal == TRUE) {
		current_link = links_to_remove;
		while(current_link != NULL) {
			free_element(((GSList*)(current_link->data))->data);
			a_list = g_slist_delete_link(a_list, current_link->data);
			current_link = current_link->next;
			diff_nb_links--;
		}
		a_list = g_slist_append(a_list, data);
		diff_nb_links++;
	}
	else {
		free_element(data);
	}
	g_slist_free(links_to_remove);
	return a_list;
}

/** \brief Function for the manipulation of sorted GSLists of incomparable data (called elements).
 *  \param a_list a sorted GSList containing incomparable elements
 *  \param data an element to add to a_list
 *  \param compare the function to compare the elements such that there can not be two comparable elements in the list
 *  \param compare2 the function needed by compare to execute (see explanations below)
 *  \param compare3 the function to compare the elements (the list is sorted according to this compare3 function)
 *  \return the new first link of a_list
 *
 *  Scans the GSList.
 *  Removes links which contain data d such that d <= data (according to compare).
 *  Function compare2 is used by compare (e.g. data type antichain: compare is compare_antichain and compare2 is the method used to compare the element stored by the antichain).
 *  Adds a link (at the right place according to compare3) containing data if there is no d in a_list such that data <= d.
 *  Returns the first link of the resulting GSList.
 *  Warning: it does not free the elements removed from a_list or data when it is not added to a_list.
 *  If this is not what you want, see scan_add_or_remove_and_sort_and_free.
 */
GSList*
scan_add_or_remove_and_sort(GSList *a_list, void* data, char (*compare)(void*, void*, char (*)(void*, void*)), char (*compare2)(void*, void*), char (*compare3)(void*, void*)) {
	GSList *links_to_remove = NULL;
	GSList *current_link = a_list;
	int is_maximal = TRUE, diff_nb_links = 0;
	// Check whether data is a maximal element and if an element has to be removed
	while(current_link != NULL) {
		if(compare(data, current_link->data, (void*)compare2) == TRUE) {
			links_to_remove = g_slist_append(links_to_remove, current_link);
		}
		else if(compare(current_link->data, data, (void*)compare2) == TRUE) {
			is_maximal = FALSE;
			break;
		}
		current_link = current_link->next;
	}
	if(is_maximal == TRUE) {
		current_link = links_to_remove;
		while(current_link != NULL) {
			a_list = g_slist_delete_link(a_list, current_link->data);
			current_link = current_link->next;
			diff_nb_links--;
		}
		a_list = insert_sorted(a_list, data, (void*)compare3);
		diff_nb_links++;
	}

	g_slist_free(links_to_remove);
	return a_list;
}

/** \brief Function for the manipulation of sorted GSLists of incomparable data (called elements).
 *  \param a_list a sorted GSList containing incomparable elements
 *  \param data an element to add to a_list
 *  \param compare the function to compare the elements such that there can not be two comparable elements in the list
 *  \param compare2 the function needed by compare to execute (see explanations below)
 *  \param compare3 the function to compare the elements (the list is sorted according to this compare3 function)
 *  \param free_element the function to free the elements
 *  \return the new first link of a_list
 *
 *  Scans the GSList.
 *  Removes links which contain data d such that d <= data (according to compare).
 *  Function compare2 is used by compare (e.g. data type antichain: compare is compare_antichain and compare2 is the method used to compare the element stored by the antichain).
 *  Adds a link (at the right place according to compare3) containing data if there is no d in a_list such that data <= d.
 *  Returns the first link of the resulting GSList.
 *  Frees each element removed from a_list and data if it is not added to a_list.
 *  If you do not want those removed elements to be freed, use scan_add_or_remove_and_sort.
 */
GSList*
scan_add_or_remove_and_sort_and_free(GSList *a_list, void* data, char (*compare)(void*, void*, char (*)(void*, void*)), char (*compare2)(void*, void*), char (*compare3)(void*, void*), void (*free_element)(void*)) {
	GSList *links_to_remove = NULL;
	GSList *current_link = a_list;
	int is_maximal = TRUE, diff_nb_links = 0;
	// Check whether data is a maximal element and if an element has to be removed
	while(current_link != NULL) {
		if(compare(data, current_link->data, (void*)compare2) == TRUE) {
			links_to_remove = g_slist_append(links_to_remove, current_link);
		}
		else if(compare(current_link->data, data, (void*)compare2) == TRUE) {
			is_maximal = FALSE;
			break;
		}
		current_link = current_link->next;
	}
	if(is_maximal == TRUE) {
		current_link = links_to_remove;
		while(current_link != NULL) {
			free_element(((GSList*)(current_link->data))->data);
			a_list = g_slist_delete_link(a_list, current_link->data);
			current_link = current_link->next;
			diff_nb_links--;
		}
		a_list = insert_sorted(a_list, data, (void*)compare3);
		diff_nb_links++;
	}
	else {
		free_element(data);
	}

	g_slist_free(links_to_remove);
	return a_list;
}

/** \brief Inserts a data in a sorted GSList.
 *  \param list a sorted GSList
 *  \param data the data to insert
 *  \param compare the function to compare the data
 *  \return the new first link of list after insertion of data
 */
GSList*
insert_sorted(GSList *list, void* data, char (*compare)(void*, void*)) {
	GSList *cur_link = list;
	char insertion_done = FALSE;
	while(cur_link != NULL) { // find the right place to add the link
		if(compare(cur_link->data, data) == TRUE) { // current link contains a data greater than the new link -> add the new link just before it
			list = g_slist_insert_before(list, cur_link, data);
			insertion_done = TRUE;
			break;
		}
		cur_link = cur_link->next;
	}
	if(insertion_done == FALSE) { // if the link has to be added at the end of the list
		list = g_slist_append(list, data);
	}
	return list;
}

/** \brief Checks is a GSList contains a given data.
 *  \param list the GSList
 *  \param data the given data
 *  \param are_elements_equal the function to check equality of data
 *  \return TRUE if list contains data, FALSE otherwise
 */
char
linked_list_contains_element(GSList* list, void* data, char (*are_elements_equal)(void*, void*)) {
	while(list != NULL) {
		if(are_elements_equal(list->data, data) == TRUE) {
			return TRUE;
		}
		list = list->next;
	}
	return FALSE;
}

/** \brief Checks if a given GSList is NULL.
 *  \param a_link the GSList
 *  \return TRUE if a_link is NULL, FALSE otherwise
 */
char
is_link_null(GSList *a_link) {
	if(a_link == NULL) {
		return TRUE;
	}
	return FALSE;
}

/** \brief Returns the data of a given GSList (of the first link).
 *  \param a_link the GSList
 *  \return the data of a_link
 */
void*
get_link_data(GSList *a_link) {
	return a_link->data;
}

/** \brief Creates a new GSList which is the exact copy of list.
 *  \param list the GSList to clone
 *  \param clone_element the function to clone the data contained in list
 *  \return the copy of list
 *
 *  Note: use clone_linked_list_2 if the clone_element function needs a context to execute
 */
GSList*
clone_linked_list(GSList* list, void* (*clone_element)(void*)) {
	GSList* copy = NULL;
	GSList* curlink = list;
	while(curlink != NULL) {
		copy = g_slist_append(copy, clone_element(curlink->data));
		curlink = curlink->next;
	}
	return copy;
}

/** \brief Creates a new GSList which is the exact copy of list.
 *  \param list the GSList to clone
 *  \param clone_element the function to clone the data contained in list
 *  \param user_data the context needed by clone_element to execute
 *  \return the copy of list
 */
GSList*
clone_linked_list_2(GSList* list, void* (*clone_element)(void*, void*), void* (*user_data)(void*)) {
	GSList* copy = NULL;
	GSList* curlink = list;
	while(curlink != NULL) {
		copy = g_slist_append(copy, clone_element(curlink->data, (void*)user_data));
		curlink = curlink->next;
	}
	return copy;
}

/** \brief Prints a linked list.
 *  \param list a GSList
 *  \param print_element the function to print the data contained in list
 */
void
print_linked_list(GSList *list, void* (*print_element)(void*)) {
	printf("Linked List : {\n");
	GSList* curlink = list;
	while(curlink != NULL) {
		printf("  ");
		print_element(curlink->data);
		printf("\n");
		curlink = curlink->next;
	}
	printf("}\n");
}
