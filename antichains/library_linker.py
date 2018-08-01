# This file is part of Acacia+, a tool for synthesis of reactive systems using antichain-based techniques
# Copyright (C) 2011-2013 UMONS-ULB
#
# This file was modified in july 2018 to allow the use of antichains in
# Game solver, a python implementation of game solving algorithms.
# Copyright (C) 2018 Clement Tamines
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from ctypes import *
import os

from constants import *

#### STRUCTURES ####
#### GList C structure
class GList(Structure):
    pass

GList._fields_ = [("data", c_void_p),
                ("next", POINTER(GList)),
                ("pred", POINTER(GList))]
    
#### GNode C structure
class GNode(Structure):
    pass

GNode._fields_ = [("data", POINTER(c_void_p)),
                  ("next", POINTER(GNode)),
                  ("pred", POINTER(GNode)),
                  ("parent", POINTER(GNode)),
                  ("children", POINTER(GNode))]

#### Graph C structure
class Adjlist_node(Structure):
    pass

Adjlist_node._fields_ = [("vertex", c_int),
                ("next", POINTER(Adjlist_node))]

#### Graph C structure
class Adjlist(Structure):
    _fields_ = [("num_members", c_int),
                ("head", POINTER(Adjlist_node))]


#### Graph C structure
class Graph(Structure):
    _fields_ = [("num_vertices", c_int),
                ("priorities", POINTER(c_int)),
                ("players", POINTER(c_int)),
                ("succ", POINTER(Adjlist)),
                ("pred", POINTER(Adjlist))]

#### Antichain C structure      
class Antichain(Structure):
    _fields_ = [("size", c_int),
                ("incomparable_elements", POINTER(GList))]

#### Vector C structure    
class Vector(Structure):
    _fields_ = [("dimension", c_int),
                ("max_value", POINTER(c_int)),
                ("values", POINTER(c_int))]

#### Tuple C structure
class Tuple(Structure):
    _fields_ = [("node", c_int),
                ("counters", POINTER(Vector))]

#### Prints an error and exits
def error_print(text):
    print text
    exit(0)

#### FUNCTIONS LOADING ####
if os.uname()[0] == "Darwin":
    lib = cdll.LoadLibrary(MAIN_DIR_PATH+"game_solver.dylib")
elif os.uname()[0] == "Linux":
    lib = cdll.LoadLibrary("../antichains/game_solver.so")
else:
    error_print("OS not supported")

##GList
is_link_null_c = lib.is_link_null
is_link_null_c.argtypes = [POINTER(GList)]
is_link_null_c.restype = c_byte

get_link_data_c = lib.get_link_data
get_link_data_c.argtypes = [POINTER(GList)]
get_link_data_c.restype = POINTER(Tuple)

##Graph
createGraph_c = lib.createGraph
createGraph_c.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]
createGraph_c.restype =  POINTER(Graph)

destroyGraph_c = lib.destroyGraph
destroyGraph_c.argtypes = [POINTER(Graph)]
destroyGraph_c.restype =  None

addEdge_c = lib.addEdge
addEdge_c.argtypes = [POINTER(Graph),c_int, c_int]
addEdge_c.restype =  None

maximal_counter_c = lib.maximal_counter
maximal_counter_c.argtypes = [POINTER(Graph)]
maximal_counter_c.restype = POINTER(c_int)

displayGraph_c = lib.displayGraph
displayGraph_c.argtypes = [POINTER(Graph)]
displayGraph_c.restype =  None

##Tuple
set_not_defined_tuple_c = lib.set_not_defined_tuple
set_not_defined_tuple_c.argtypes = None
set_not_defined_tuple_c.restype = None

compute_tuples_intersection_c = lib.compute_tuples_intersection
compute_tuples_intersection_c.argtypes = [POINTER(Tuple), POINTER(Tuple)]
compute_tuples_intersection_c.restype = POINTER(Tuple)

compare_tuples_c = lib.compare_tuples
compare_tuples_c.argtypes = [POINTER(Tuple), POINTER(Tuple)]
compare_tuples_c.restype = c_byte

clone_tuple_c = lib.clone_tuple
clone_tuple_c.argtypes = [POINTER(Tuple)]
clone_tuple_c.restype = c_void_p

print_tuple_c = lib.print_tuple
print_tuple_c.argtypes = [POINTER(Tuple)]
print_tuple_c.restype = None

free_tuple_full_c = lib.free_tuple_full
free_tuple_full_c.argtypes = [POINTER(Tuple)]
free_tuple_full_c.restype = None

free_not_defined_tuple_c = lib.free_not_defined_tuple
free_not_defined_tuple_c.argtypes = None
free_not_defined_tuple_c.restype = None

##Antichain
PRINT_ELEMENT_FUNC = CFUNCTYPE(None, c_void_p)
PRINT_TUPLE_FUNC = CFUNCTYPE(None, POINTER(Tuple))
COMPARE_TUPLES_FUNC = CFUNCTYPE(c_byte, POINTER(Tuple), POINTER(Tuple))
FREE_TUPLE_FULL_FUNC = CFUNCTYPE(None, POINTER(Tuple))
CLONE_TUPLE_FUNC = CFUNCTYPE(c_void_p, POINTER(Tuple))
COMPUTE_TUPLES_INTERSECTION_FUNC = CFUNCTYPE(POINTER(Tuple), POINTER(Tuple),POINTER(Tuple))

compute_antichains_union_c = lib.compute_antichains_union
compute_antichains_union_c.argtypes = [POINTER(Antichain), POINTER(Antichain), COMPARE_TUPLES_FUNC,FREE_TUPLE_FULL_FUNC]
compute_antichains_union_c.restype = POINTER(Antichain)

compute_antichains_intersection_c = lib.compute_antichains_intersection
compute_antichains_intersection_c.argtypes = [POINTER(Antichain), POINTER(Antichain), COMPARE_TUPLES_FUNC, COMPUTE_TUPLES_INTERSECTION_FUNC, CLONE_TUPLE_FUNC, FREE_TUPLE_FULL_FUNC]
compute_antichains_intersection_c.restype = POINTER(Antichain)

compute_antichains_union2_c = lib.compute_antichains_union2
compute_antichains_union2_c.argtypes = [POINTER(Antichain), POINTER(Antichain)]
compute_antichains_union2_c.restype = POINTER(Antichain)

compute_antichains_intersection2_c = lib.compute_antichains_intersection2
compute_antichains_intersection2_c.argtypes = [POINTER(Antichain), POINTER(Antichain)]
compute_antichains_intersection2_c.restype = POINTER(Antichain)

compare_antichains_c = lib.compare_antichains
compare_antichains_c.argtypes = [POINTER(Antichain), POINTER(Antichain), COMPARE_TUPLES_FUNC]
compare_antichains_c.restype = c_byte

contains_element_c = lib.contains_element
contains_element_c.argtypes = [POINTER(Antichain), c_void_p, COMPARE_TUPLES_FUNC]
contains_element_c.restype = c_byte

clone_antichain_c = lib.clone_antichain
clone_antichain_c.argtypes = [POINTER(Antichain), CLONE_TUPLE_FUNC]
clone_antichain_c.restype = POINTER(Antichain)

free_antichain_full_c = lib.free_antichain_full
free_antichain_full_c.argtypes = [POINTER(Antichain), FREE_TUPLE_FULL_FUNC]
free_antichain_full_c.restype = None

print_antichain_c = lib.print_antichain
print_antichain_c.argtypes = [POINTER(Antichain), PRINT_TUPLE_FUNC]
print_antichain_c.restype = None

##BackwardAlgorithm
build_start_antichain_c = lib.build_start_antichain
build_start_antichain_c.argtypes = [POINTER(Graph),c_int, POINTER(c_int)]
build_start_antichain_c.restype = POINTER(Antichain)

pre_c = lib.pre
pre_c.argtypes = [POINTER(Antichain), POINTER(Antichain), c_int, POINTER(Graph)]
pre_c.restype = POINTER(Antichain)

fixpoint_c = lib.fixpoint
fixpoint_c.argtypes = [POINTER(Graph)]
fixpoint_c.restype = POINTER(Antichain)

winning_region_c = lib.winning_regions
winning_region_c.argtypes = [POINTER(Graph)]
winning_region_c.restype = POINTER(c_int)