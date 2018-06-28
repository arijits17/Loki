import os
import re
import time
from to_file import *

"""
This function takes a C code. and Daikon invariants generated on it. Puts those back at 
place on main function as assertion.

Intended to use as checking soundness of the Daikon invariants.

TODO: works faulty if not well indented. 
TODO: all invariants are not parsed actually.

Uses some functions defined in to_file. 
"""


def put_invariants_as_assert(c_code_orig_file, target_file, daikon_result_file):
	daikon_text = [daikon_output.rstrip('\n') for daikon_output in open(daikon_result_file)]
	c_code_lines = [c_code.rstrip('\n') for c_code in open(c_code_orig_file)]
	instrmented_code = open(target_file, "w+")
	instrmented_lines = []
	code_w_assert = list(c_code_lines)

	line_it = 4
	runcount = 0
	insert_loc = 0



	while line_it < len(daikon_text) :
		line = daikon_text[line_it]
		if line.startswith(".."):
			
			print "[DEBUG OUT] Current Function name : " + line
			
			if ("ENTER" in line):		
				
				func_name = line[2:].rstrip("):::ENTER")

				for inv_file_num, inv_file_line in enumerate(code_w_assert):
					if((func_name in inv_file_line)  and (";}" not in inv_file_line)):
						insert_loc = inv_file_num+2
						# print "[DEBUG ] Insertion Loc : " + str(insert_loc)
						print "[DEBUG] "+func_name + " starts at "+str(inv_file_num + 1)



			else:
				
				func_name = line[2:].rstrip("):::EXIT")


				it = 0

				while not ((func_name in code_w_assert[it]) and (";}" not in code_w_assert[it])):
					it += 1
				
				function_running = True
				parenthesis_balance = 0

				while function_running:
					it += 1
					if ((parenthesis_balance + code_w_assert[it].count('{') - code_w_assert[it].count('}'))>0):
						print "[DEBUG ]parenthesis_balance  at line" + str(it+1) + "is" + str(parenthesis_balance) 
						it += 1
					else:
						function_running = False  			#ASSURE CODE INDENTED WELL OR DO SOMETHING TO BREAK INTO }-s
						print "[DEBUG] "+func_name + " ends at "+str(it+ 1)

				insert_loc = it -1
				
				# print  Insertion Loc : " + str(insert_loc) 






				
			line_it += 1
			line = daikon_text[line_it]
			
			# asserts_here = set([])

			while not (line.startswith("====")):

				assert_st = invariant_to_assert(line)


				if (assert_st != ""):
					print "[DEBUG IN] Current Function name : " + func_name 

					code_w_assert.insert(insert_loc, assert_st)
					print "[ASSERT INSERTED] "+ assert_st
					break

				line_it += 1
				line = daikon_text[line_it]


		line_it += 1

	print_invariants_to_file(code_w_assert, target_file)



put_invariants_as_assert("c_code.c","new_c_code.c","daikon_result")
start_time = time.time()
os.system("cbmc --all-properties new_c_code.c > cbmc_output.txt")
print "CBMC took "+ str(time.time() - start_time) + " seconds."


