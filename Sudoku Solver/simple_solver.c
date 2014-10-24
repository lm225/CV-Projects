//  simple_solver.c
//  Created by Lauren Kira Murray on 19/02/2014.
#include <stdio.h>
#include "sudoku_header.h"
#include <stdlib.h>

//global variable used to test if multiple solutions have been found
int multiplesolutions = 0;
//sudoku struct to store the solved sudoku
struct sudoku solved_sudoku;

/* method which checks if the sudoku can be solved */
enum tag solver(struct sudoku sudoku_struct){

	enum tag result = check_sudoku(&sudoku_struct);
	if (result == INVALID){
        return INVALID;
	}
	else if (result == COMPLETE){
		solved_sudoku = sudoku_struct;
		return COMPLETE;
	}
	else{
		int i;
		int j;
		int counter = 0;
		for(i = 0; i < 9; i++){
			for(j = 0; j < 9; j++){
				/* break out of the current iteration if a gap in the sudoku is found */
				if(sudoku_struct.row_struct_array[i].items[j] == '.'){
					goto exitloops;
				}
			}
		}
		exitloops:
		for(int k = 1; k <10; k++){
			if(multiplesolutions == 1){
				return INVALID;
			}
			sudoku_struct.row_struct_array[i].items[j] = '0'+k;
			if(solver(sudoku_struct) == COMPLETE){
				counter++;
				if(counter > 1){
					multiplesolutions = 1;
					return INVALID;
				}
			}
		}
		return COMPLETE;
	}
			
	return INVALID;
}



