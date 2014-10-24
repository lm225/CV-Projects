# teststudent.s

# sample small test suite for funcall code

       .data

       .align 2  # above bytes not going align what follows

        # going to allocate some space to store function calls in 

spacebot: .asciiz ""
         .align 2  # above bytes not going align what follows

        .space 1000

       .align 2  # above bytes not going align what follows
spacetop: .asciiz ""


        .align 2    
        
        # Some strings for messages

newline: 
        .asciiz "\n"
teststring: 
        .asciiz "Test about to be called:\n"
resultstring: 
        .asciiz "Result of test as integer is: "

        .align 2

        .globl main
        .globl plus
        .globl negate
        .globl constant42

        .text

        # some sample simple functions
    
plus:                    # plus takes two arguments and returns their sum
                        # without worrying about overflow
        addu $v0,$a0,$a1
        jr $ra
        
negate:                 # negate takes one argument and returns the negative value
        sub $v0,$zero,$a0
        jr $ra

constant42:             # takes zero arguments and returns 42
        li $v0,42
        jr $ra
        
add5args:                   # takes 5 arguments and returns the sum
        addu    $v0, $a0, $a1
        addu    $v0, $v0, $a2
        addu    $v0, $v0, $a3
        lw      $t0, 16($sp)
        addu    $v0, $v0, $t0
        jr      $ra

        # a simple test case

test1:  # we will compute the function plus 12 7

        addiu $sp,$sp,-24   # just need space for $ra plus 8 octet alignment
        sw $ra,16($sp)     # store ra above argument space

        la $a0,spacebot
        la $t1,plus
        
                        # first fes is 3/&plus
        li $t2,3        # add has two arguments, plus one is 3
        sw $t2,0($a0)
        sw $t1,4($a0)
                        # second fes is 0/12
        sw $zero,8($a0)
        li $t2,12       
        sw $t2,12($a0)

                        # third fes is 0/7
        sw $zero,16($a0)
        li $t2,7       
        sw $t2,20($a0)

                        # call funcall and return
        jal funcall1

        lw $ra,16($sp)     # restore ra
        addiu $sp,$sp,24   # restore sp 

        jr $ra

test2:  # we will compute the function plus constant42 plus negate 19 12
        # result should be 42 + (-19) + 12 = 35

        addiu $sp,$sp,-24   # just need space for $ra plus 8 octet alignment
        sw $ra,16($sp)     # store ra above argument space

        la $a0,spacebot
        la $t1,plus
        la $t4,negate
        la $t5,constant42

                        # first fes is 3/&plus
        li $t2,3        # add has two arguments, plus one is 3
        sw $t2,0($a0)
        sw $t1,4($a0)
                        # second fes is 1/&constant42
        li $t2,1
        sw $t2,8($a0)
        sw $t5,12($a0)
                        # third fes is 3/&plus
        li $t2,3        # add has two arguments, plus one is 3
        sw $t2,16($a0)
        sw $t1,20($a0)
                        # fourth fes is 2/&negate 
        li $t2,2       
        sw $t2,24($a0)
        sw $t4,28($a0)
                        # fifth fes is 0/19
        sw $zero,32($a0)
        li $t2,19       
        sw $t2,36($a0)
                        # sixth fes is 0/12
        sw $zero,40($a0)
        li $t2,12       
        sw $t2,44($a0)

                        # call funcall and return
        jal funcall2

        lw $ra,16($sp)     # restore ra
        addiu $sp,$sp,24   # restore sp 

        jr $ra

test3:  # we will compute the function add5args 10 9 8 7 6 
        # result should be 40
        
        addiu    $sp, $sp, -24   # increase stack
        sw      $ra, 20($sp)    # save return address to stack

        la      $a0, spacebot 
        la      $t0, add5args 
                                 # first fes is 6/&plus
        li      $t1, 6
        sw      $t1, 0($a0)
        sw      $t0, 4($a0)

        li      $t0, 10          # second fes is 0/10
        sw      $zero, 8($a0)   
        sw      $t0, 12($a0)

        li      $t0, 9          # third fes is 0/9
        sw      $zero, 16($a0)  
        sw      $t0, 20($a0)

        li      $t0, 8          # fourth fes is 0/8
        sw      $zero, 24($a0)  
        sw      $t0, 28($a0)

        li      $t0, 7          # fifth fes is 0/7
        sw      $zero, 32($a0)  
        sw      $t0, 36($a0)

        li      $t0, 6          # sixth fes is 0/6
        sw      $zero, 40($a0)  
        sw      $t0, 44($a0)

        jal funcall2            # call funcall and return

        lw      $ra, 20($sp)    # restore ra
        addiu   $sp, $sp, 24    # restore sp

        jr      $ra

testandprint:   # run test and print the result
                # argument $a0 is address of test function to call

        addiu $sp,$sp,-24  # just need space for $ra plus result 
        sw $ra,16($sp)     # store ra above argument space

        sw $a0,20($sp)     # will store a0 for a moment

        li $v0, 4          # syscall 4 (print_str)
        la $a0, teststring # argument
        syscall            # print the string

        lw $a0,20($sp)     # and now restore $a0

        jalr $ra,$a0       # call function at $a0, store return address in $ra

        sw $v0,20($sp)     # store result while we print some strings

        li $v0, 4          # syscall 4 (print_str)
        la $a0, resultstring # argument
        syscall            # print the string

        lw $a0, 20($sp)     # reload result
        li $v0, 1          # syscall 1 (print_int)
        syscall            # print the result as integer

        li $v0, 4          # syscall 4 (print_str)
        la $a0, newline    # tidy up with newline
        syscall            # print the string

        lw $ra,16($sp)     # restore ra
        addiu $sp,$sp,24   # restore sp 
        jr $ra             # return to caller
                        
main:   

        addiu $sp,$sp,-24   # just need space for $ra plus 8 octet alignment
        sw $ra,16($sp)     # store ra above argument space
        
        la $a0,test1           # load test1 
        jal testandprint       # call it and print result

        la $a0,test2           # load test2 
        jal testandprint       # call it and print result

        la $a0,test3           # load test3 
        jal testandprint       # call it and print result

        lw $ra,16($sp)     # restore ra
        addiu $sp,$sp,24   # restore sp 

        jr $ra          # return to caller
