//  sudoku_check.c
//  Created by Lauren Kira Murray on 17/02/2014.
#include <stdio.h>
#include "sudoku_header.h"

/* method which takes in an array and returns its state (invalid, incomplete or complete) */
enum tag check_array(int array[]) {
    
    //flag to keep track of incomplete arrays
    int flag = 0;
    for (int i = 0; i < 9; i++) {
    	for (int j = i + 1; j < 9; j++) {
    		if(array[j] == '.' || array[i] == '.'){
        		flag = 1;
        	}else if (array[i] == array[j]) {
				return INVALID;
        	}
    	}
	}
	if (flag == 1){
		return INCOMPLETE;
	}
	else{
		return COMPLETE;
	}

}

/* method which checks if a sudoku is invalid, incomplete or complete by calling the check_array method on different rows, columns and boxes */
enum tag check_sudoku(struct sudoku* sudoku_struct) {
    
    // 0 = complete, 1 = incomplete
    int check = 0;

    //check row
    for(int i = 0; i < 9; i++){
    	enum tag result = check_array(sudoku_struct->row_struct_array[i].items);
    	if (result == INVALID){
            return result;
    	}
    	else if (result == INCOMPLETE){
                check = 1;
    	}
    }

    //check columns
    //9 times (for each column)
    for(int i = 0; i < 9; i++){
        int array[9];
        //9 times (for each row)
        for(int j = 0; j < 9; j++){
            array[j] = sudoku_struct->row_struct_array[j].items[i];
        }
        enum tag result = check_array(array);
        if (result == INVALID){
            return result; 
        }
        else if (result == INCOMPLETE){
                check = 1;
        }
    }
    
    //check boxes
    //9 times (for each box)
    for(int i = 0; i < 9; i++){
        int array[9];
        int outer_row = (i/3)*3;
        int outer_col = (i%3)*3;
        //9 times (for each cell in the box)
        for(int j = 0; j < 9; j++){
            int inner_row = j/3;
            int inner_col = j%3;
            int row = outer_row + inner_row;
            int col = outer_col + inner_col;
            array[j] = sudoku_struct->row_struct_array[row].items[col];
        }
        enum tag result = check_array(array);
         if (result == INVALID){
            return result;
        }
        else if (result == INCOMPLETE){
                check = 1;
        }

        
    }
    if(check == 0){
        return COMPLETE;
    }
    else{
        return INCOMPLETE;
    }

}