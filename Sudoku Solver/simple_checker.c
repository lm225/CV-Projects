//  simple_checker.c
//  Created by Lauren Kira Murray on 19/02/2014.

#include <stdio.h>
#include "sudoku_header.h"

//sudoku struct to store the solved sudoku
extern struct sudoku solved_sudoku;

int main(){

	//create a struct to store the sudoku 
	struct sudoku sudoku_struct;

	read_sudoku(&sudoku_struct);
	printf("Here is the sudoku you input:\n");
	print_sudoku(&sudoku_struct);

	enum tag result = solver(sudoku_struct);
	if(result == INVALID){
		printf("Sorry the sudoku you entered is invalid.\n");
	}
	else if(result == COMPLETE){
		printf("Here is the solved sudoku:\n");
		print_sudoku(&solved_sudoku);
	}
	return 0;
}