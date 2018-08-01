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

# C Booleans
FALSE = 0
TRUE = 1

# Maximal strategy size for label simplification and drawing
MAX_STRAT_SIZE = 20

# Players
P_I = 1
P_O = 2

# Optimizations
NO_OPT = "none"
OPT1 = "1"
OPT2 = "2"
OPT12 = "12"
ON = "on"
OFF = "off"

# Display
NONE = 0
RECAP = 1
MINTEXT = 2
ALLTEXT = 3

# LTL to Buchi translation and LTL synthesis method
MONO = "mono"
COMP = "comp"

# LTL to Buchi tools
LTL2BA = "ltl2ba"
LTL3BA = "ltl3ba"
WRING = "wring"
SPOT = "spot"

# Set of strategies
ARBITRARY = "arbitrary"
OPTIMAL = "optimal"
MAX = "max"
ALL = "all"

# Parenthesizing
FLAT = "FLAT"
BINARY = "BINARY"

# Algorithm
FORWARD = "forward"
BACKWARD = "backward"

# Check
REAL = "real"
UNREAL = "unreal"
BOTH = "both"

# main dir 
MAIN_DIR_PATH = "./"

# tmp directory for wring files path
TMP_PATH = MAIN_DIR_PATH+"tmp/"

# external tools directories
LTL2BA_PATH = MAIN_DIR_PATH+"tools/ltl2ba-1.1/"
LTL3BA_PATH = MAIN_DIR_PATH+"tools/ltl3ba-1.0.2/" # To set when installed
SPOT_PATH = MAIN_DIR_PATH+"tools/spot-1.0/" # To set when installed