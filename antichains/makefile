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

OS = $(shell uname)
CC=gcc
ifeq ($(OS), Darwin)
	ARCHFLAG=
	TARGET=game_solver.dylib
endif
ifeq ($(OS), Linux)
	ARCHFLAG=
	TARGET=game_solver.so
endif
	
LFLAGS=`pkg-config --cflags --libs glib-2.0`
CFLAGS=$(LFLAGS) -fpic
EXEC=game_solver
OBJS=antichain.o backward_algorithm.o linked_list.o vector.o tuple.o graph.o

game_solver.dylib: $(OBJS)
	$(CC) $(ARCHFLAG) -dynamiclib -o $@ $^ $(LFLAGS)
	
game_solver.so: $(OBJS)
	$(CC) $(ARCHFLAG) -shared -o $@ $^ $(LFLAGS)

antichain.o: linked_list.h

backward_algorithm.o: antichain.h linked_list.h tuple.h

tuple.o: vector.h


%.o: %.c
	$(CC) $(ARCHFLAG) -o $@ $(CFLAGS) -c $< 

clean:
	rm -f *.o
	
mrproper: clean
	rm -f *.dylib *.so
	
install: $(TARGET) clean	