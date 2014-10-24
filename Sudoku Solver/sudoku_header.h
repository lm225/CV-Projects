//  sudoku_header.h
//  Created by Lauren Kira Murray on 19/02/2014.

//define structs
struct row {
    int items[9];
};
struct sudoku {
    struct row row_struct_array[9];
};

//function prototypes
void read_sudoku(struct sudoku* sudoku_struct);
void print_sudoku(struct sudoku* sudoku_struct);
enum tag check_array(int array[]);
enum tag check_sudoku(struct sudoku* sudoku_struct);
enum tag solver(struct sudoku sudoku_struct);
void print_two(struct sudoku* sudoku_struct);

//create an enum variable (tag) which can be set to either invalid, incomplete or complete
enum tag {INVALID, INCOMPLETE, COMPLETE};