//  sudoku_io.c
//  Created by Lauren Kira Murray on 17/02/2014.
#include <stdio.h>
#include "sudoku_header.h"

/* method which reads in a sudoku and stores it in a struct */
void read_sudoku(struct sudoku* sudoku_struct) {
    for(int i = 0; i < 9; i++){
        //create sudoku row and add input to this!
        struct row row_struct;
        for(int j = 0; j < 9; j++){
        	char input;
        	scanf(" %c", &input);
        	if((input < '1') || (input > '9')){
        		input = '.';
        	}
        	row_struct.items[j] = (int)input;
        }
        sudoku_struct->row_struct_array[i] = row_struct;
    }
}

/* method which prints out a given sudoku */
void print_sudoku(struct sudoku* sudoku_struct) {
 	for(int i = 0; i < 9; i++){
 		for(int j = 0; j < 9; j++){
 			printf("%c", sudoku_struct->row_struct_array[i].items[j]);
 		}
 		printf("\n");
 	}

}

