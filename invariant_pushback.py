import os

# daikon_output = 
daikon_text = [daikon_output.rstrip('\n') for daikon_output in open("daikon_result")]
c_code_orig = [c_code.rstrip('\n') for c_code in open("c_code.c")]
c_code_with_inv  = open("new_c_code.c", "w+")
code_with_sound_invarint = open("c_code_w_inv.c","w+")
c_code_new = []

line_it = 4
runcount = 0
while line_it < len(daikon_text):
	# line_it += 1
	line = daikon_text[line_it]
	print "[DEBUG] " + str(line_it) + " " + daikon_text[line_it] 
	if line.startswith(".."):
		if line.startswith("..udon_dummy_"):
			func_name = line[2:]
			func_name = func_name.rstrip("):::ENTER")
			func_name = func_name.rstrip("):::EXIT")
			print "[DEBUG] Current Function name : " + func_name 
			while not line.startswith("===="):
				c_code_new = []
				c_code_with_inv.close()
				os.system("rm new_c_code.c")
				print "**************************************************[NEW FILE GENERATED]************************************************"

				c_code_with_inv  = open("new_c_code.c", "w+")

				# line_it += 1
				line = daikon_text[line_it]
				if ("orig" not in line ):							#consider this case later
					assert_st = "assert(" + line[2:] + ");"
					for num, c_line in enumerate(c_code_orig):
						# print "[CCODE] " + c_line
						if func_name in c_line and ");" in c_line:
							print "[DEBUG LINE ALTER ] Original line : " + c_line
							c_code_new.append(assert_st)
							print "[CCODE] " + str(c_code_new[-1])
							print "[DEBUG LINE ALTER ] Changed  line : " + c_code_new[num]


							for it in range(num+1, len(c_code_orig)-1 ):
								c_code_new.append(c_code_orig[it])
								print "[CCODE] " + str(c_code_new[-1])

							c_code_with_inv.close()
						 	c_code_with_inv  = open("new_c_code.c", "w+")


							for line in c_code_new:
								print "[CPRINT ] " + line
								print>>c_code_with_inv, line

							runcount += 1
							cbmc_name = "cbmc"+str(runcount)
							c_code_name = "c_code"+str(runcount)









							os.system("cbmc new_c_code.c > cbmc_output.txt")
							os.system("cp cbmc_output.txt ./cbmc/"+ cbmc_name)
							os.system("cp new_c_code.c ./ccode/"+ c_code_name)
							cbmc_output = open("cbmc_output.txt")
							cbmc_text = cbmc_output.read().strip().split()
							print "[DEBUG] CBMC RAN ONCE  " 


							if ("SUCCESSFUL" in cbmc_text):
								print("[CBMC REPORTS] Cool, Here is a correct assert")
								print "************************************************[   VOILA        ]***********************************************************"
								print("[CBMC REPORTS] " + assert_st)
							else:
								print("[CBMC REPORTS] This too, failed.")

						else:
							c_code_new.append(c_code_orig[num])
							print "[CCODE] " + str(c_code_new[-1])


					print assert_st
				line_it += 1
	line_it += 1






print "*********************************************************************************************************************************"
