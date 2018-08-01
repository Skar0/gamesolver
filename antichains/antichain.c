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
 * \file antichain.c
 * \brief Functions for the manipulation of antichains
 * \author Aaron Bohy
 * \version 1.1
 */

#include "antichain.h"
#include "tuple.h"

/** \brief Creates a new empty antichain.
 *  \return the new empty antichain
 */
antichain*
new_antichain() {
	antichain* a = (antichain*)malloc(sizeof(antichain));

	a->size = 0;
	GSList *list = NULL;
	a->incomparable_elements = list;

	return a;
}

/** \brief Adds an element to the antichain and frees discarded elements.
 *	\param a the antichain in which the element has to be added
 *	\param element the element to add
 *	\param compare_elements the function to compare the elements
 *	\param free_element the function to free the elements
 *
 *	If element is incomparable to any element contained in a, element is added to a.
 *	If there exists x in a such that x > element (according to compare_elements function), element is not added to a and is freed.
 *	Otherwise, all x in a such that element > x are removed from a and freed.
 */
void
add_element_to_antichain_and_free(antichain* a, void *element, char (*compare_elements)(void*, void*), void (*free_element)(void*)) {
	GSList *cur_link = a->incomparable_elements;
	GSList *elements_to_remove = NULL;
	char incomparable = TRUE;
	while(cur_link != NULL) {
		if(compare_elements(element, cur_link->data) == TRUE) {
			incomparable = FALSE;
			break;
		}
		else if(compare_elements(cur_link->data, element) == TRUE) {
			elements_to_remove = g_slist_append(elements_to_remove, cur_link);
		}
		cur_link = cur_link->next;
	}
	if(incomparable == TRUE) {
		cur_link = elements_to_remove;
		while(cur_link != NULL) {
			free_element(((GSList*)(cur_link->data))->data);
			a->incomparable_elements = g_slist_delete_link(a->incomparable_elements, cur_link->data);
			cur_link = cur_link->next;
			a->size--;
		}
		a->incomparable_elements = g_slist_append(a->incomparable_elements, element);
		a->size++;
	}
	else {
		free_element(element);
	}
	g_slist_free(elements_to_remove);
}

/** \brief Adds an element to the antichain.
 *
 *	\param a the antichain in which the element has to be added
 *	\param element the element to add
 *	\param compare_elements the function to compare the elements
 *
 *	If element is incomparable to any element contained in a, element is added to a.
 *	If there exists x in a such that x > element (according to compare_elements function), do nothing.
 *	Otherwise, all x in a such that element > x are removed from a.
 *	Warning: any discarded element is not freed. If this is not what you want, use add_element_to_antichain_and_free.
 */
void
add_element_to_antichain(antichain* a, void *element, char (*compare_elements)(void*, void*)) {
	GSList *cur_link = a->incomparable_elements;
	GSList *elements_to_remove = NULL;
	char incomparable = TRUE;
	while(cur_link != NULL) {
		if(compare_elements(element, cur_link->data) == TRUE) {
			incomparable = FALSE;
			break;
		}
		else if(compare_elements(cur_link->data, element) == TRUE) {
			elements_to_remove = g_slist_append(elements_to_remove, cur_link);
		}
		cur_link = cur_link->next;
	}
	if(incomparable == TRUE) {
		cur_link = elements_to_remove;
		while(cur_link != NULL) {
			a->incomparable_elements = g_slist_delete_link(a->incomparable_elements, cur_link->data);
			cur_link = cur_link->next;
			a->size--;
		}
		a->incomparable_elements = g_slist_append(a->incomparable_elements, element);
		a->size++;
	}
	g_slist_free(elements_to_remove);
}

/** \brief Computes the intersection between the closure of 2 antichains.
 *	\param antichain1 the first antichain
 *	\param antichain2 the second antichain
 *	\param compare_elements the function to compare the elements
 *	\param intersection the function to compute the intersection between two elements
 *	\param clone_element the function to clone the elements
 *	\param free_element the function to free the elements
 *	\return the antichain representing the intersection of antichain1 and antichain2 closures
 *
 *	First checks whether antichain1 < antichain2 (resp. antichain2 < antichain1). If so, returns antichain1 (resp. antichain2).
 *	While checking antichain1 < antichain2, remembers all f1 in antichain1 s.t. there exists a f2 in antichain2 s.t. f1 < f2
 *		(and do the same for antichain2 < antichain1).
 *	Use that information to accelerate the intersection computation (those f1 and f2 will always be in the intersection,
 *		so we can add them immediatly and skip all computation about them.
 *	Warning: Does NOT free antichain1 and antichain2 after the intersection has been computed.

antichain*
compute_antichains_intersection(antichain *antichain1, antichain *antichain2, char (*compare_elements)(void*, void*), void* (*intersection)(void*, void*), void* (*clone_element)(void*), void (*free_element)(void*)) {
	//Check whether antichain1 < antichain2 or antichain2 < antichain1 (goal: to prevent a useless intersection computation (because the result is antichain1 or antichain2)
    //en gros verifie linclusion des antichaines avec compare element un par 1 vs tous les elements de la deyxueme antichaine
	int* compare_ext_1 = compare_antichains_extended(antichain1, antichain2, (void*)compare_elements);
	int* compare_ext_2 = compare_antichains_extended(antichain2, antichain1, (void*)compare_elements);
	if(compare_ext_1[0] == TRUE) {
		free(compare_ext_1);
		free(compare_ext_2);

		return clone_antichain(antichain1, (void*)clone_element); //antichain1 < antichain2 -> the intersection is antichain1
	}
	else if(compare_ext_2[0] == TRUE) {
		free(compare_ext_1);
		free(compare_ext_2);

		return clone_antichain(antichain2, (void*)clone_element); //antichain2 < antichain1 -> the intersection is antichain2
	}
	else {
		antichain *antichains_intersection = new_antichain();

		//Optimize the way to compute the intersection: antichain1 (inters) antichain2 or antichain2 (inters) antichain1 (to minimize the number of iterations)
		int a1_size = antichain1->size-compare_ext_1[1]; //a1_size is the number of elements f1 in antichain1 s.t. there is no element f2 in antichain2 s.t. f1 < f2
		int a2_size = antichain2->size-compare_ext_2[1]; //a2_size is the number of elements f2 in antichain2 s.t. there is no element f1 in antichain1 s.t. f2 < f1
		int x = a1_size*antichain2->size;
		int y = a2_size*antichain2->size;
		if(y>x) { //swap the two antichains to minimize the number of iterations
			antichain* temp = antichain1;
			antichain1 = antichain2;
			antichain2 = temp;
			int* temp2 = compare_ext_1;
			compare_ext_1 = compare_ext_2;
			compare_ext_2 = temp2;
		}

		//Compute the intersection
		void *current_element_computed;
		GSList *curlink_list1 = antichain1->incomparable_elements;
		GSList *curlink_list2;
		int i = 2, j;
		char first_loop = TRUE;
		while(curlink_list1 != NULL) { //for each f1
			if(compare_ext_1[i] == FALSE) { //if there is no f in antichain2 s.t. f1 < f, compute all intersections for f1
				curlink_list2 = antichain2->incomparable_elements;
				j = 2;
				while(curlink_list2 != NULL) { //for each f2
					if(compare_ext_2[j] == FALSE) { //if there is no f in antichain1 s.t. f2 < f, compute the intersection between f2 and f1
						//Computes the intersection of a pair (f1, f2) where f1 (resp. f2) is a maximal element of antichain1 (resp. antichain2)

						//printf("Trying to max_elem between\n");
						//print_tuple(curlink_list1->data);
						//printf("\n");
						//print_tuple(curlink_list2->data);
						//printf("~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");

						current_element_computed = intersection(curlink_list1->data, curlink_list2->data);
						add_element_to_antichain_and_free(antichains_intersection, current_element_computed, (void*)compare_elements, (void*)free_element);
					}
					else { //there is a f in antichain1 s.t. f2 < f -> f2 will always be in the intersection -> add it once
						if(first_loop == TRUE) {
							add_element_to_antichain_and_free(antichains_intersection, clone_element(curlink_list2->data), (void*)compare_elements, (void*)free_element);
						}
					}
					//Move to next link in list2
					curlink_list2 = curlink_list2->next;
					j++;
				}
				first_loop = FALSE;
			}
			else { //there is a f in antichain2 s.t. f1 < f -> f1 will always be in the intersection -> add it and skip to the next f1
				add_element_to_antichain_and_free(antichains_intersection, clone_element(curlink_list1->data), (void*)compare_elements, (void*)free_element);
			}
			//Move to next link in list1
			curlink_list1 = curlink_list1->next;
			i++;
		}

		free(compare_ext_1);
		free(compare_ext_2);

		return antichains_intersection;
	}
}
**/

antichain*
compute_antichains_intersection(antichain *antichain1, antichain *antichain2, char (*compare_elements)(void*, void*), void* (*intersection)(void*, void*), void* (*clone_element)(void*), void (*free_element)(void*)) {

    //Check whether antichain1 < antichain2 or antichain2 < antichain1 (goal: to prevent a useless intersection computation (because the result is antichain1 or antichain2)
    //en gros verifie linclusion des antichaines avec compare element un par 1 vs tous les elements de la deyxueme antichaine
    int* compare_ext_1 = compare_antichains_extended(antichain1, antichain2, (void*)compare_elements);
    int* compare_ext_2 = compare_antichains_extended(antichain2, antichain1, (void*)compare_elements);
    if(compare_ext_1[0] == TRUE) {
        free(compare_ext_1);
        free(compare_ext_2);

        return clone_antichain(antichain1, (void*)clone_element); //antichain1 < antichain2 -> the intersection is antichain1
    }
    else if(compare_ext_2[0] == TRUE) {
        free(compare_ext_1);
        free(compare_ext_2);

        return clone_antichain(antichain2, (void*)clone_element); //antichain2 < antichain1 -> the intersection is antichain2
    }
    else {
        antichain *antichains_intersection = new_antichain();

        //Optimize the way to compute the intersection: antichain1 (inters) antichain2 or antichain2 (inters) antichain1 (to minimize the number of iterations)
        int a1_size = antichain1->size-compare_ext_1[1]; //a1_size is the number of elements f1 in antichain1 s.t. there is no element f2 in antichain2 s.t. f1 < f2
        int a2_size = antichain2->size-compare_ext_2[1]; //a2_size is the number of elements f2 in antichain2 s.t. there is no element f1 in antichain1 s.t. f2 < f1
        int x = a1_size*antichain2->size;
        int y = a2_size*antichain2->size;
        if(y>x) { //swap the two antichains to minimize the number of iterations
            antichain* temp = antichain1;
            antichain1 = antichain2;
            antichain2 = temp;
            int* temp2 = compare_ext_1;
            compare_ext_1 = compare_ext_2;
            compare_ext_2 = temp2;
        }

        //Compute the intersection
        void *current_element_computed;
        GSList *curlink_list1 = antichain1->incomparable_elements;
        GSList *curlink_list2;
        int i = 2, j;
        char first_loop = TRUE;
        while(curlink_list1 != NULL) { //for each f1
            if(compare_ext_1[i] == FALSE) { //if there is no f in antichain2 s.t. f1 < f, compute all intersections for f1
                curlink_list2 = antichain2->incomparable_elements;
                j = 2;
                while(curlink_list2 != NULL) { //for each f2
                    if(compare_ext_2[j] == FALSE) { //if there is no f in antichain1 s.t. f2 < f, compute the intersection between f2 and f1
                        //Computes the intersection of a pair (f1, f2) where f1 (resp. f2) is a maximal element of antichain1 (resp. antichain2)
                        //seulement si ils sont comparables pour la closure cad les (v,m) (v',m'- v =v'
                        /**
						printf("Trying to max_elem between\n");
						print_tuple(curlink_list1->data);
						printf("\n");
						print_tuple(curlink_list2->data);
						printf("~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
                        **/
                        current_element_computed = intersection(curlink_list1->data, curlink_list2->data);
                        if(current_element_computed != NOT_DEFINED) {
                            add_element_to_antichain_and_free(antichains_intersection, current_element_computed, (void*)compare_elements, (void*)free_element);
                        }
                    }
                    else { //there is a f in antichain1 s.t. f2 < f -> f2 will always be in the intersection -> add it once
                        if(first_loop == TRUE) {
                            add_element_to_antichain_and_free(antichains_intersection, clone_element(curlink_list2->data), (void*)compare_elements, (void*)free_element);
                        }
                    }
                    //Move to next link in list2
                    curlink_list2 = curlink_list2->next;
                    j++;
                }
                first_loop = FALSE;
            }
            else { //there is a f in antichain2 s.t. f1 < f -> f1 will always be in the intersection -> add it and skip to the next f1
                add_element_to_antichain_and_free(antichains_intersection, clone_element(curlink_list1->data), (void*)compare_elements, (void*)free_element);
            }
            //Move to next link in list1
            curlink_list1 = curlink_list1->next;
            i++;
        }

        free(compare_ext_1);
        free(compare_ext_2);

        return antichains_intersection;
    }
}


antichain*
compute_antichains_intersection2(antichain *antichain1, antichain *antichain2) {
    return compute_antichains_intersection(antichain1, antichain2, (void*)compare_tuples, (void*)compute_tuples_intersection, (void*)clone_tuple, (void*)free_tuple_full);
}
/** \brief Computes the union of closure of 2 antichains.
 *  \param antichain1 the first antichain
 *  \param antichain2 the second antichain
 *	\param compare_elements the function to compare the elements
 *	\param free_element the function to free the elements
 *  \return the antichain representing the union of antichain1 and antichain2 closures
 *
 *  Warning: after computation, elements of antichain1 and antichain2 have been modified, and antichain1 and antichain2 are freed
 */
antichain*
compute_antichains_union(antichain *antichain1, antichain *antichain2, char (*compare_elements)(void*, void*), void (*free_element)(void*)) {
	GSList *curlink = antichain2->incomparable_elements;

	//For each element of antichain2, scan the union list to find < or > elements
	while(curlink != NULL) {
		// Add curlink to the union if it is maximal and remove all links from the union smaller than curlink
		add_element_to_antichain_and_free(antichain1, curlink->data, (void*)compare_elements, (void*)free_element);
		curlink = curlink->next;
	}

	free_antichain(antichain2);

	return antichain1;
}


antichain*
compute_antichains_union2(antichain *antichain1, antichain *antichain2) {
    return compute_antichains_union(antichain1,antichain2,(void*)compare_tuples, (void*)free_tuple_full);
}


/** \brief Compares two antichains.
 *  \param antichain1 the first antichain
 *  \param antichain2 the second antichain
 *	\param compare_elements the function to compare the elements
 *  \return TRUE if for all incomparable element e1 of antichain1, there exists a incomparable element e2 of antichain 2, such that e2 is greater than e1, FALSE otherwise
 */
char
compare_antichains(antichain *antichain1, antichain *antichain2, char (*compare_elements)(void*, void*)) {
	GSList *curlink_list1 = antichain1->incomparable_elements;
	while(curlink_list1 != NULL) {
		if(contains_element(antichain2, curlink_list1->data, compare_elements) == FALSE) {
			return FALSE;
		}
		curlink_list1 = curlink_list1->next;
	}

	return TRUE;
}

/** \brief Compares two antichains (returns more information than compare_antichains).
 *  \param antichain1 the first antichain
 *  \param antichain2 the second antichain
 *	\param compare_elements the function to compare the elements
 *  \return an integers array such that:
 *		tthe first element is TRUE (resp. FALSE) if antichain1 is smaller (resp. not smaller) than antichain2;
 *		the second element is the number of maximal elements f1 of antichain1 s.t. there exists a maximal elements f2 in antichain2
 *			s.t. f1 < f2 (according to compare_elements func);
 *		the rest of the array contains boolean values (TRUE in the ith position if for the (i-2)th maximal element of antichain1, there exists
 *			a maximal f2 in antichain2 s.t. f1 < f2 (according to compare_elements func), FALSE otherwise
 */
static int*
compare_antichains_extended(antichain *antichain1, antichain *antichain2, char (*compare_elements)(void*, void*)) {
	int* result_array = (int*)malloc((2+antichain1->size)*sizeof(int));
	GSList *curlink_list1 = antichain1->incomparable_elements;
	char found, compare = TRUE;
	int count = 0, i = 2;
	while(curlink_list1 != NULL) { //for each f1 in antichain1
		found = FALSE;
		if(contains_element(antichain2, curlink_list1->data, compare_elements) == TRUE) {
			found = TRUE; //found a f2 s.t. f1 < f2
			count++; //increment the number of f1 in antichain1 s.t. there exists an f2 in antichain2 s.t. f1 < f2
		}
		else {
			compare = FALSE; //there is no f2 s.t. f1 < f2
		}
		result_array[i] = found; //set the boolean value for f1
		i++;
		curlink_list1 = curlink_list1->next;
	}
	result_array[0] = compare; //set the compare variable (TRUE if antichain1 < antichain2, FALSE otherwise)
	result_array[1] = count; //set the number of f1 in antichain1 s.t. there exists an f2 in antichain2 s.t. f1 < f2

	return result_array;
}

/** \brief Compares the size of two antichains.
 *  \param antichain1 the first antichain
 *  \param antichain2 the second antichain
 *
 *  \return TRUE is antichain1 has more elements than antichain2, FALSE otherwise
 */
char
compare_antichains_size(antichain *antichain1, antichain *antichain2) {
	if(antichain1->size >= antichain2->size) {
		return TRUE;
	}
	return FALSE;
}

/** \brief Checks if an element is contained in an antichain closure.
 *  \param a the antichain
 *  \param element the element
 *  \param compare_elements the function
 *
 *  \return TRUE if element is in the antichain closure, FALSE otherwise
 */
char
contains_element(antichain *a, void *element, char (*compare_elements)(void*, void*)) {
	GSList *curlink = a->incomparable_elements;
	while(curlink != NULL) {
		if(compare_elements(element, curlink->data)) {
			return TRUE;
		}
		curlink = curlink->next;
	}

	return FALSE;
}


/** \brief Checks if the antichain is empty.
 *  \param a the antichain
 *  \param is_empty a function that returns TRUE iff the element on which it is called is empty
 *  \return TRUE if the antichain is empty (or reduced to the empty element), FALSE otherwise
 *
 *  Note: the is_empty function may be useful when there is a particular element in the data manipulated which is considered as being the empty element.
 */
char
is_antichain_empty(antichain *a, char (*is_empty)(void*)) {
	if(a->incomparable_elements == NULL) {
		return TRUE;
	}
	else if(a->size == 1) {
		if(is_empty(a->incomparable_elements->data)) {
			return TRUE;
		}
	}
	return FALSE;
}

/** \brief Computes the number of elements symbolically represented by an antichain a, that is, the size of the closure of a.
 *  \param a the antichain
 *  \param compute_element_closure_size the function to compute the size of the closure of an element
 *  \param compute_elements_intersection the function to compute the intersection of two elements
 *  \param compare_elements the function to compare the elements
 *	\param free_element the function to free the elements
 *  \return the size of the closure of the antichain
 */
unsigned long compute_antichain_closure_size(antichain *a, int (*compute_element_closure_size)(void*), void* (*compute_elements_intersection)(void*, void*), char (*compare_elements)(void*, void*), void (*free_element)(void*)) {
	if(a->size == 1) { // Basic case: antichain of 1 element -> return the size of the closure of the unique element
		return compute_element_closure_size(a->incomparable_elements->data);
	}
	else { // General case
		unsigned long size = 0;
		antichain *inters;
		GSList *curlink = a->incomparable_elements, *curlink2;
		while(curlink != NULL) {
			// Count the closure of the current element
			size += compute_element_closure_size(curlink->data);

			// Compute the antichain of intersections between previously computed elements and current element
			inters = new_antichain();
			curlink2 = a->incomparable_elements;
			while(curlink2 != curlink) {
				add_element_to_antichain_and_free(inters, compute_elements_intersection(curlink2->data, curlink->data), (void*)compare_elements, (void*)free_element);
				curlink2 = curlink2->next;
			}

			// Remove from the sum the size of the closure of antichain inters (i.e. the states that have already been counted)
			size -= compute_antichain_closure_size(inters, (void*)compute_element_closure_size, (void*)compute_elements_intersection, (void*)compare_elements, (void*)free_element);

			// Free inters
			free_antichain_full(inters, (void*)free_element);

			curlink = curlink->next;
		}
		return size;
	}
}

/** \brief Prints an antichain.
 *  \param antichain the antichain
 *  \param print_element the function to print the elements
 */
void
print_antichain(antichain *antichain, void (*print_element)(void*)) {
	GSList *curlink = antichain->incomparable_elements;
	printf("{");
	while(curlink != NULL) {
		print_element(curlink->data);
		if(curlink->next != NULL) {
			printf(", ");
		}

		curlink = curlink->next;
	}
	printf("}");
}

/** \brief Prints an antichain.
 *  \param antichain the antichain
 *  \param print_element the function to print the elements (this function needs some context to execute)
 *  \param context the required data of the print_element function
 */
void
print_antichain_custom(antichain *antichain, void (*print_element)(void*, void*), void* context) {
	GSList *curlink = antichain->incomparable_elements;
	printf("{");
	while(curlink != NULL) {
		print_element(curlink->data, context);
		if(curlink->next != NULL) {
			printf(", ");
		}

		curlink = curlink->next;
	}
	printf("}");
}


/** \brief Creates a new antichain which is the exact copy of a.
 *  \param a the antichain
 *  \param clone_element the function to clone the elements
 *  \return a copy of a
 */
antichain*
clone_antichain(antichain* a, void* (*clone_element)(void*)) {
	antichain* copy = (antichain*)malloc(sizeof(antichain));

	copy->size = a->size;
	copy->incomparable_elements = clone_linked_list(a->incomparable_elements, (void*)clone_element);

	return copy;
}


/** \brief Frees the memory allocated to an antichain a without freeing the elements contained in a.
 *  \param a the antichain to free
 */
void
free_antichain(antichain* a) {
	g_slist_free(a->incomparable_elements);
	free(a);
}

/** \brief Frees the memory allocated to an antichain a and frees all elements contained in a (using the free_element function).
 *  \param a the antichain to free
 *  \free_element the function to free elements
 */
void
free_antichain_full(antichain* a, void (*free_element)(void*)) {
	g_slist_foreach(a->incomparable_elements, (GFunc)free_element, NULL);
	free_antichain(a);
}
