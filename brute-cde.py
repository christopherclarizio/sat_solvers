# brute-cde.py  :  brute forces sat
# Team          :  CDE: Chris-Donny-Emily
# Date          :  9-26-17


# Imports:
import sys
import os
import string
import time

# Globals:
BIT_ASSIGNMENT_S = ''	# String, will contian the bit assignment i.e. 01001
FILE_NAME = ''			# String, will contain the name of the file we are reading from
BINARY = ''				# String, will contain 0 or 1 to indicate whether to display tracing or not
INPUT = ''				# String, will contain the raw information read in from the file
WFF = ''				# String, will contain the lines describing a single WFF
COMMENT_LINE = []		# Array, will contain information about WFF i.e. ['c', prob. #, max # literals, (un)solvability]
PROBLEM_LINE = []		# Array, will contain information about WFF i.e. ['p', file format, # variables, # clauses]
TOT_LITERALS = 0		# Integer, will contain the total number of literals in the WFF; needed for output
START_TIME   = None		# Time, will contain time describing the start of execution; needed for execution time
END_TIME     = None		# Time, will contain time descriibng the end of execution; needed for execution
NUM_S = 0				# Integer, will contain the number of WFF's that you found to be satisfiable
NUM_U = 0				# Integer, will contain the number of WFF's that you found to be unsatisfiable
NUM_ANSWERS = 0			# Integer, will contain the number of WFF's that you provided answers for
NUM_CORRECT = 0			# Integer, will contain the number of WFF's that you provided correctly

# Usage message to be displayed if necessarry
def usage(exit_status=0):
	print('''Usage: brute-cde.py [FILE_NAME] [BINARY]
		FILE_NAME			The file to be read that contains wffs.
		BINARY 				1 = Triggers Optional Tracing ; 0 = Suppress Intermediate Output''')
	sys.exit(exit_status)

	
	
# Reads in raw input from specified file into "INPUT"
def readFile():
	f = open(FILE_NAME, 'r')	# Open file specified by "FILE_NAME"
	global INPUT				# Declare "INPUT" as global; allows us to edit its value
	INPUT = f.read()			# Set "INPUT" to contain the raw information from the file

	
	
# Returns whether the assignment sent satisfies the WFF, currently in WFF
def verify(assignment):
	global BIT_ASSIGNMENT_S														# Declare "BIT_ASSIGNMENT_S" as global; allows us to edit its value
	bit_assignment = bin(assignment)											# Use bin() to convert "assignment" to binary and store in "bit_assignment"
	variable_assignments = []													# Array, will store the assignments for each variable in a clause
	BIT_ASSIGNMENT_S = (str(bit_assignment))[2:].zfill(int(PROBLEM_LINE[2]))	# Convert "bit_assignment" to a string with necessary number of leading zeros

	WFF_Clauses = WFF.split(',0')												# Split "WFF" into clauses using split() and store into "WFF_Clauses"
	WFF_Clauses.remove('')														# Remove unecessary characters from "WFF_Clauses" using remove()

	TOT_LITERALS = len(WFF.split(',')) - int(PROBLEM_LINE[3])					# calculate the number of literals in "WFF" and store into "TOT_LITERALS"

	flag = True  																# Boolean, stores whether the "assignment" satisfies the WFF; default to true

	# Evaluate assignment against WFF
	# literals joined by OR in clauses and clauses are joined by AND
	for clause in WFF_Clauses:													# Iterate over all clauses in "WFF_Clauses"
		clause = clause.split(',')												# Convert a string of comma separated integers to a list of those integers; '-1,2,3'  --> ['-1', '2', '3']
		clauseFlag = False														# Boolean, stores whether the "assignment" satisfies the current clause
		
		for i in xrange(0, len(clause)):														# Iterate over the number of literals in the current clause
			if int(clause[i]) < 0 and int(BIT_ASSIGNMENT_S[abs(int(clause[i])) - 1]) == 0:		# If the literal is negated and the assignment is zero
				clauseFlag = True																# Set "clauseFlag" to true since literals are joined by OR
			elif int(clause[i]) > 0 and int(BIT_ASSIGNMENT_S[abs(int(clause[i])) - 1]) == 1:	# If the literal is not negated and the assignment is one
				clauseFlag = True																# Set "clauseFlag" to true since literals are joined by OR
		if clauseFlag == False:																	# If "clauseFlag" is false, i.e. none of the literals were true
			flag = False																		# Set "flag" to false since clauses are joined by AND
			break																				# Break out of the iteration over the clauses; only need to find one false clause

	return flag																	# Return the value of the flag



# Generates the output line for the WFF in the required format
def output(f, verified):
	global NUM_ANSWERS, NUM_CORRECT, NUM_S, NUM_U		# Declare "NUM_ANSWERS", "NUM_CORRECT" ... to global; allows us to edit their values
	EXECUTION_TIME = (END_TIME - START_TIME)* 10**6		# Calculate "EXECUTION_TIME" using "END_TIME" and "START_TIME"
	
	# Predict SAT.
	COMPARE = '0'										# String, will contain result of our prediction; to be used in output line; 0 by defualt (no prediction)
	if COMMENT_LINE[3] != '?':							# If it is specified whether the WFF is satisfiable or not
		NUM_ANSWERS = NUM_ANSWERS + 1					# Increment "NUM_ANSWERS" by one 
		# Compare SAT to Answer SAT.
		COMPARE = '-1'									# Set "COMPARE" to -1 (incorrect prediction)
		if SAT == COMMENT_LINE[3]:						# If our prediction on whether the WFF is satisfiable matches the given answer
			NUM_CORRECT = NUM_CORRECT + 1				# Increment "NUM_CORRECT" by one
			COMPARE = '1'								# Set "COMPARE" to 1 (correct prediction)

	
	if verified:										# If an assignment was verified for a WFF
		NUM_S = NUM_S + 1								# Increment "NUM_S" by one; we found one more that is satisfiable
		bit_list = list(BIT_ASSIGNMENT_S)				# List, will contain the assigment that was verifed for a WFF
		bit_string = ','.join(bit_list)					# String, will contain the string representing the assigment that was verifed for a WFF

		# Write to the file the required output line
		# Prob No., No. Var., No. Clauses, Max Lit., Tot. Lit., S/U, 1/-1, Exec. Time, 1/0 (SAT)
		f.write('{0},{1},{2},{3},{4},{5},{6},{7:.2f},{8}\n'.format(COMMENT_LINE[1], PROBLEM_LINE[2], PROBLEM_LINE[3], COMMENT_LINE[2], TOT_LITERALS, SAT, COMPARE, EXECUTION_TIME, bit_string))
		
	else:												# If an assigment was not verifed for a WFF
		NUM_U = NUM_U + 1								# Increment "NUM_U" by one; we found one more that is not satisfiable
		
		# Wrtie to the file the required output line
		# Prob No., No. Var., No. Clauses, Max Lit., Tot. Lit., S/U, 1/-1, Exec. Time, 1/0 (SAT)
		f.write('{0},{1},{2},{3},{4},{5},{6},{7:.2f}\n'.format(COMMENT_LINE[1], PROBLEM_LINE[2], PROBLEM_LINE[3], COMMENT_LINE[2], TOT_LITERALS, SAT, COMPARE, EXECUTION_TIME))



#should time the execution time take for each wff starting with the first call 
#to the assignment generator to the completion of the call to verify and avoid the
#time to read and parse the wff from the given file and the tiem to generate the output file
#this time should be in microseconds

#using package time; time.time(), gives current time in seconds.

# Main Execution 
num_wffs = 0										# Integer, will store the number WFFs to test

# Parse Command Line:
if len(sys.argv[1:]) != 2:
	usage(1)
FILE_NAME = sys.argv[1]								# sets "FILE_NAME" to whatever was sent
BINARY = sys.argv[2]								# sets "BINARY" to the option of whether to trace or not

OUTPUT_FILE = FILE_NAME.split('/')[1]
OUTPUT_FILE = OUTPUT_FILE.split('.')[0]				# creates the "OUTPUT_FILE" from the "FILE_NAME" that was sent

f = open(OUTPUT_FILE+'.csv', 'w')					# Opens the "OUTPUT_FILE" to write to in write mode

readFile() # INPUT contains raw file

lines = INPUT.split('\n')							# Splits the input into lines

for i in range(0, len(lines)):						# Iterates over all the lines
	# Check for 'p' Lines:
	if 'p' in lines[i]:
		strippedLine = lines[i].strip('\r')
		PROBLEM_LINE = strippedLine.split(' ')
	
	# Check For 'c' Lines:
	elif 'c' in lines[i]:
		WFF = ''
		BIT_ASSIGNMENT_S = ''
		COMMENT_LINE = []
		PROBLEM_LINE = []

		strippedLine = lines[i].strip('\r')
		COMMENT_LINE = strippedLine.split(' ')
	
	# Add WFF lines to WFF string
	else:
		if int(PROBLEM_LINE[2]) <= 10:  #  FOR TESTING PURPOSES
			WFF = WFF + lines[i].strip('\r')
			# If the next character is a 'c', evaluate the current WFF
			if i < (len(lines) - 2):
				if 'c' in lines[i+1]:
					num_wffs = num_wffs + 1

					# Iterate through each possible character and verify check it
					assignment = 0
					flag = False
					SAT = 'U'
					START_TIME = time.time()
					for x in xrange(2**int(PROBLEM_LINE[2])):
						if(verify(assignment)):
							flag = True
							SAT = 'S'
							break
						assignment = assignment + 1
					END_TIME = time.time()
					output(f, flag)

f.write('{0},cde,{1},{2},{3},{4},{5}'.format(FILE_NAME, num_wffs, NUM_S, NUM_U, NUM_ANSWERS, NUM_CORRECT))
f.close()