import os
import re


def print_to_file(lines_of_file, new_file_name):
	c_code_with_inv  = open("new_c_code.c", "w+")


	for line in lines_of_file:
		print "[CPRINT ] " + line
		print>>c_code_with_inv, line

	c_code_with_inv.close()

	# c_code_name = "c_code_00"

	os.system("cp new_c_code.c ./ccode/"+ new_file_name)


# c_code_new = [daikon_output.rstrip('\n') for daikon_output in open("daikon_result")]
# print_to_file(c_code_new,"c_code_000")




def print_invariants_to_file(lines_of_file):
	code_with_sound_invarint = open("c_code_w_inv.c","w+")

	for line in lines_of_file:
		if "udon_dummy" not in line:
			print "[INVARIANT PRINT ] " + line
			print>>code_with_sound_invarint, line

	code_with_sound_invarint.close()




def invariant_to_assert(line):
	if ("orig" not in line ):							
		assert_st = "assert(" + line[2:] + ");"
	else:
		assert_st = ""

	return assert_st

"""

def instrument_to_retain_orig_variable(orig_filename, new_filename):
	c_code_lines = [c_code.rstrip('\n') for c_code in open(orig_filename)]
	instrmented_code = open(new_filename, "w+")

	instrmented_lines = []

	datatypes = ["int","char", "float", "long"]

	for line_num, line in enumerate(c_code_lines):
		type = list(set(datatypes).intersection(re.split(';|,| ',line)))
		if(type != []):
			print "[DEBUG] Type found "+ type[0]








	for line in instrumented_lines:
		print "[CPRINT ] " + line
		print>>instrmented_code, line

	instrmented_code.close()








def instrument_to_block(orig_filename, new_filename):
	c_code_lines = [c_code.rstrip('\n') for c_code in open(orig_filename)]
	instrmented_code = open(new_filename, "w+")

	instrmented_lines = []










	for line in instrumented_lines:
		print "[CPRINT ] " + line
		print>>instrmented_code, line

	instrmented_code.close()
"""

