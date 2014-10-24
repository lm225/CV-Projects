all: program

program: simple_solver.o sudoku_check.o sudoku_io.o sudoku_header.h simple_checker.o
	clang simple_solver.o sudoku_check.o sudoku_io.o simple_checker.o -o program -Wall -Wextra -g