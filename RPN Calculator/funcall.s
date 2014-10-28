# funcall.s

# CS 2002 Assembler Practical Week 10
# School of Computer Science
# University of St Andrews
# Ian Gent April 2014
#
# Write two function handling programs for Polish notation, 
# respecting respecting function calling stack conventions
#
#

# You must provide two global labels funcall1 and funcall2
# 
# Each takes one argument $a0 which is the address of the FET to evaluate.
# 
# Note that by definition funcall2 correctly implements funcall1, so if funcall2 is perfect
# you can get full marks by using label funcall1 for the same address.  But you can also 
# submit separate programs (e.g. if you are not confident that funcall2 is fully working, 
# or just want to show how your code developed from the easier to the harder function.)
#
# For full details of requirements consult the practical specification on studres 

        	.data

        	.globl funcall1
        	.globl funcall2
       

        	.text
funcall2:
funcall1:
			# callee saves
			addi  $sp, $sp, -48 	# increase stack
			sw    $fp, 16($sp)	 	# saving frame pointer
			addi  $fp, $sp, 48		# set new frame pointer
			sw    $ra, 20($sp) 		# saving return address
			sw 	  $s0, 24($sp)		# saving s0
			sw 	  $s1, 28($sp)		# saving s1
			sw 	  $s2, 32($sp)		# saving s2
			sw 	  $s3, 36($sp)		# saving s3
			sw 	  $s4, 40($sp)		# saving s4
			sw 	  $s5, 44($sp)		# saving s5


			# variable allocation
			# $s0 = first word of a0 (number of args + 1), becomes number of agrs
			# $s1 = iterator for loop
			# $s2 = function address (from second word)
			# $s3 = value of $a0 (s5 = pointer to current read location of x(a0) - incement by value of v1)
			# $s4 = v1 total - increase by value of v1 when seen
			# $s6 = number of args (greater than 4) - overspill args

			# $t0 - stores result of mflo
			# $t1 - used for calculating offset (stores n-1 where n is iterator)
			# $t2 - stores result of mflo
			# $t3 - stores copy of $sp
			# $t4 = temp used for multiplying

			lw	  $s0, 0($a0)		# fetch value of FET pointer (number of arguments + 1)
			beq	  $s0, $zero, basecase	# branch to basecase if $s0 = 0 
	
 			lw 	  $s2  4($a0)		# fetch the function address (from the second word)
 			addi  $s0, $s0, -1 		# calculate and store number of arguments	
 			move  $s3, $a0 			# store value of $a0 in $s3
 			addi  $s3, 8			# Shift pointer along 8 bytes

 			li    $s1, 0 			# set $s1 to 1(loop iterator)
 			li    $s4, 2			# set $s4 to 2 (as will be 2 or more since first 2 are accounted for)

 			li    $s5, 0			# set overflow args to 0 ($s5)
 			ble   $s0, 4, loop		# branch to loop if number of arguments <= 4
 			addi  $s5, $s0, -4 		# store number of arguments (greater than 4 - overspill args)
 			li    $t4, 4 			# store 4 in $t4 for multiplying
 			mult  $s5, $t4 			# multiply value of s6 by 4
 			mflo  $s5 				# move value of $LO to $s5
 			sub  $sp, $sp, $s5 		# increase stack

	loop:   
			beq   $s1, $s0, executefunction	
			move  $a0, $s3			# copy $s3 into $a0
			jal funcall1 			# call function

			add   $s4, $s4, $v1		# add value of v1 to s4 (total)
			li 	  $t4, 4 			# store 4 in t4 for multiplying
			mult  $v1, $t4 			# temporarily store value of v1*4
			mflo  $t0 				# move value of $LO to $t0
			add   $s3, $s3, $t0		# increment pointer (s3) by v1*4

			addi  $s1, $s1, 1 		# increment $s1

			# calculate offset
			sub   $t1, $s1, 1 		# store (n - 1) in $t1 
			li    $t4, 4            # store 4 in t4 for multiplying
			mult  $t1, $t4 			# multiply t1 by 4
			mflo  $t2				# move value from mflo into t2 (t2 is now offset)
			move  $t3, $sp 			# copy $sp into $t3
			add   $t3, $t3, $t2		# $t3 refers to correct memory location (inc. offset)
			sw    $v0, 0($t3)		# save in correct position
			b loop					# goto loop

executefunction:
		    lw    $a0, 0($sp)		# load $a0 from stack
		    lw    $a1, 4($sp)		# load $a1 from stack
		    lw    $a2, 8($sp)		# load $a2 from stack
		    lw    $a3, 12($sp)		# load $a3 from stack
		    jal   $s2				# call function address
		    move  $v1, $s4			# copy s4 into v1
		    add   $sp, $sp, $s5 	# decrease stack
			b returnbranch			# go to returnbranch

basecase:
 			# base case
 			lw 	  $v0, 4($a0)		# fetch value of second word
  			li 	  $v1, 2 			# put number of words into v1
  			b returnbranch			# go to returnbranch

returnbranch:
			# callee restores

 			lw 	  $s5, 44($sp)		# load s5 from stack
 			lw 	  $s4, 40($sp)		# load s4 from stack
 			lw	  $s3, 36($sp)		# load s3 from stack
 			lw 	  $s2, 32($sp)		# load s2 from stack
 			lw 	  $s1, 28($sp)		# load s1 from stack
 			lw 	  $s0, 24($sp)		# load s0 from stack
			lw    $ra, 20($sp) 		# load return address from stack
			sw    $fp, 16($sp)	 	# restore frame pointer
			addi $sp, $sp, 48		# decrease stack 

			jr $ra           # return
