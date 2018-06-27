import os
import re
from to_file import *


def put_invariants_as_assert(c_code_orig_file, target_file, daikon_result_file):
	daikon_text = [daikon_output.rstrip('\n') for daikon_output in open(daikon_result_file)]
	c_code_lines = [c_code.rstrip('\n') for c_code in open(c_code_orig_file)]
	instrmented_code = open(target_file, "w+")
	instrmented_lines = []
	code_w_assert = list(c_code_lines)


	line_it = 4
	runcount = 0


	while line_it < len(daikon_text) :
		line = daikon_text[line_it]
		print "[DEBUG] " + str(line_it) + " " + daikon_text[line_it] 
		if line.startswith(".."):
			if line.startswith("..udon_dummy_"):		#take_care of other functions too	
				func_name = line[2:]
				func_name = func_name.rstrip("):::ENTER")
				func_name = func_name.rstrip("):::EXIT")
				print "[DEBUG] Current Function name : " + func_name 

				while not line.startswith("===="):
					assert_st = invariant_to_assert(line)
					# print "[DEBUG] Why it loops here? A"
					print code_w_assert
					print assert_st
					for inv_file_num, inv_file_line in enumerate(code_w_assert):
						# print "[DEBUG] Why it loops here? B"
						print code_w_assert

						if((func_name in inv_file_line) and (");" in inv_file_line)) :
							# print "[DEBUG] Why it loops here? C" 

							code_w_assert.insert(inv_file_num+1, assert_st)
							print "[ASSERT INSERTED] "+ assert_st
							break


					if(line_it < len(daikon_text)) :
						line_it += 1
					else:
						break

		if(line_it < len(daikon_text)) :
			line_it += 1
		else:
			break

	print_invariants_to_file(code_w_assert)



put_invariants_as_assert("c_code.c","new_c_code.c","daikon_result")