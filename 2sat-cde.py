# backtrack-cde.py  :  tree evaluates sat
# Team          :  . . .
# Date          :  . . .


# Imports:
import sys
import os
import string
import time
import random

# Globals:
LIT_VALS = []
FILE_NAME = ''
BINARY = ''
INPUT = ''
WFF = ''
COMMENT_LINE = []    #  Array - ['c', prob. #, max # literals, (un)solvability]
PROBLEM_LINE = []    #  Array - ['p', file format, # variables, # clauses]
TOT_LITERALS = 0     #  Needed for output
START_TIME   = None  #  Needed for execution time
END_TIME     = None  #    "     "      "      "
NUM_S = 0
NUM_U = 0
NUM_ANSWERS = 0
NUM_CORRECT = 0

#one command line argument --> name of file to read wffs in from
#binary argument that turns on or off optional tracing 1 yes, 0 not


def usage(exit_status=0):
	print('''Usage: brute-cde.py [FILE_NAME] [BINARY]
		FILE_NAME			The file to be read that contains wffs.
		BINARY 				1 = Triggers Optional Tracing ; 0 = Suppress Intermediate Output''')
	sys.exit(exit_status)


#reads in the next wff from a specified input file
def readFile():
	f = open(FILE_NAME, 'r')
	global INPUT	
	INPUT = f.read()	


#generates the next possible assingment for the current wff you are working with
#def nextPossibleAssignment():


#takes a wff and an assignment and returns whether or not the assignment satisfied the wff
def verify():
	flag = False

	WFF_Clauses = WFF.split(',0')
	WFF_Clauses.remove('') 	
	global TOT_LITERALS
	TOT_LITERALS = len(WFF.split(',')) - int(PROBLEM_LINE[3])


	# Initialize two lists of -1's.
	lit_vals = [-1] * int(PROBLEM_LINE[2])
	clause_vals = [-1] * int(PROBLEM_LINE[3])
	stack = []

	next_lit = 1
	next_assign = 0
	while not all(vals == 1 for vals in lit_vals):
		lit_vals[next_lit - 1] = next_assign
		stack.append(next_lit)

		# Update clause_vals in prepartion for next_lit.
		clause_Index = 0
		for clause in WFF_Clauses:
			variables = clause.split(',')
			numTrue = 0;
			numFalse = 0;
			for var in variables:
				if var < 0:
					if lit_vals[abs(int(var))-1] == 0:
						numTrue = numTrue + 1
					elif lit_vals[abs(int(var))-1] == 1:
						numFalse = numFalse + 1
				else:
					if lit_vals[abs(int(var))-1] == 1:
						numTrue = numTrue + 1
					elif lit_vals[abs(int(var))-1] == 0:
						numFalse = numFalse + 1
			if numTrue > 0:
				clause_vals[clause_Index] = 1
			elif numFalse == 2:
				clause_vals[clause_Index] = 0
			else:
				clause_vals[clause_Index] = -1

			clause_Index = clause_Index + 1


		# Evaluate clause_vals.
		if all(vals == 1 for vals in clause_vals):
			flag = True
			break;
		elif 0 in clause_vals:
			next_lit = stack.pop()
			if lit_vals[next_lit - 1] == 1:
				flag = False
				break
			else:
				next_assign = 1
		elif -1 in clause_vals:
			clause_Index = 0
			found_next_assign = False
			for clause in WFF_Clauses:
				if clause_vals[clause_Index] == -1:   #  Clause is undetermined and . . .
					if str(next_lit) in clause:       #  lit is in the clause.
						lits = clause.split(',')
						if abs(int(lits[0])) == next_lit:
							next_lit = abs(int(lits[1]))
							if int(lits[1]) < 0:
								next_assign = 0
								break
							else:
								next_assign = 1
								break
						else:
							next_lit = abs(int(lits[0]))
							if int(lits[0]) < 0:
								next_assign = 0
								break
							else:
								next_assign = 1
								break
						found_next_assign = True

			if not found_next_assign:				  #  lit is not in the clause.
				for i in xrange(0, len(lit_vals)):
					if lit_vals[i] == -1:
						next_lit = i+1
						next_assign = 0
						break
	global LIT_VALS
	LIT_VALS = lit_vals

	return flag



#generates the output line for the wff in the desired format
def output(f, verified):
	global NUM_ANSWERS, NUM_CORRECT, NUM_S, NUM_U
	EXECUTION_TIME = (END_TIME - START_TIME)* 10**6
	
	# Predict SAT.
	COMPARE = '0'
	if COMMENT_LINE[3] != '?':
		NUM_ANSWERS = NUM_ANSWERS + 1
		# Compare SAT to Answer SAT.
		COMPARE = '-1'
		if SAT == COMMENT_LINE[3]:
			NUM_CORRECT = NUM_CORRECT + 1
			COMPARE = '1'

	if verified:
		NUM_S = NUM_S + 1
		bit_string = ''.join(str(val) for val in LIT_VALS)
		# Prob No., No. Var., No. Clauses, Max Lit., Tot. Lit., S/U, 1/-1, Exec. Time, 1/0 (SAT)
		f.write('{0},{1},{2},{3},{4},{5},{6},{7:.2f},{8}\n'.format(COMMENT_LINE[1], PROBLEM_LINE[2], PROBLEM_LINE[3], COMMENT_LINE[2], TOT_LITERALS, SAT, COMPARE, EXECUTION_TIME, bit_string))
	else:
		NUM_U = NUM_U + 1
		f.write('{0},{1},{2},{3},{4},{5},{6},{7:.2f}\n'.format(COMMENT_LINE[1], PROBLEM_LINE[2], PROBLEM_LINE[3], COMMENT_LINE[2], TOT_LITERALS, SAT, COMPARE, EXECUTION_TIME))

#should time the execution time take for each wff starting with the first call 
#to the assignment generator to the completion of the call to verify and avoid the
#time to read and parse the wff from the given file and the tiem to generate the output file
#this time should be in microseconds

#using package time; time.time(), gives current time in seconds.

num_wffs = 0
# Parse Command Line:
if len(sys.argv[1:]) != 2:
	usage(1)
FILE_NAME = sys.argv[1]
BINARY = sys.argv[2]

OUTPUT_FILE = FILE_NAME.split('/')[1]
OUTPUT_FILE = OUTPUT_FILE.split('.')[0]
f = open('2sat-'+OUTPUT_FILE+'.csv', 'w')

readFile() # INPUT contains raw file

lines = INPUT.split('\n')

for i in range(0, len(lines)):
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
		if int(PROBLEM_LINE[2]) <= 4:  #  FOR TESTING PURPOSES
			WFF = WFF + lines[i].strip('\r')
			# If the next character is a 'c', evaluate the current WFF
			if 'c' in lines[i+1]:
				num_wffs = num_wffs + 1

				# Verify the wff
				flag = False
				SAT = 'U'
				START_TIME = time.time()
				if(verify()):
					flag = True
					SAT = 'S'
				END_TIME = time.time()
				output(f, flag)
			if i+2 == len(lines):
				num_wffs = num_wffs + 1

				# Verify the wff
				flag = False
				SAT = 'U'
				START_TIME = time.time()
				if(verify()):
					flag = True
					SAT = 'S'
				END_TIME = time.time()
				output(f, flag)
				i = len(lines)
				break

f.write('{0},cde,{1},{2},{3},{4},{5}'.format(FILE_NAME, num_wffs, NUM_S, NUM_U, NUM_ANSWERS, NUM_CORRECT))
f.close()