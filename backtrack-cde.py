#determines satifiability by building an assignment piecemeal
#chose a variable to guess a value and record the variable name and value on a stack
#along with whether or not there is another value to try for that variable
#you then see which clauses have now been satisfied, if all clauses have been satisfied
#then you can declare the wff is satisfiable

#if in the checkin you can't satisfy all clauses but no clause has been unsatisfied then
#you need to make another choice for a different variable. You can use any heuristic
#such as try a value for the next variable but a particularly good one is to try a 
#variable that is part of one of the clauses that you haven't satisfied

#if in the checking you find a clause that has all its literal with values that are all
#false then you can erase the last assignment as specified on top of the stack and if
#the flag associated with that entry says that the other value has not been tried then you
#can flip the assignment for the variable and try again. If both values have been tried then
#pop the stack and repeat on the prior one. If you empty the stack declare unsatisfiable

#Again you should time from the start of the first push to the response

#the verify function may be handy here when debuggin test cases that do not include the answer

# brute-cde.py  :  brute forces sat
# Team          :  . . .
# Date          :  . . .


# Imports:
import sys
import os
import string
import time

# Globals:
BIT_ASSIGNMENT_S = ''
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
def verify(assignment):
	global BIT_ASSIGNMENT_S
	bit_assignment = bin(assignment)
	variable_assignments = []
	BIT_ASSIGNMENT_S = (str(bit_assignment))[2:].zfill(int(PROBLEM_LINE[2]))

	WFF_Clauses = WFF.split(',0')
	WFF_Clauses.remove('')

	TOT_LITERALS = len(WFF.split(',')) - int(PROBLEM_LINE[3])

	flag = True  #  Switch flag if assignment fails the clause.

	# Evaluate assignment against WFF where literals are OR'd in clauses and clauses are AND'd in WFF's.
	for clause in WFF_Clauses:
		clause = clause.split(',')  #  '-1,2,3'  --> ['-1', '2', '3']
		clauseFlag = False
		
		for i in xrange(0, len(clause)):
			if int(clause[i]) < 0 and int(BIT_ASSIGNMENT_S[abs(int(clause[i])) - 1]) == 0:
				clauseFlag = True
			elif int(clause[i]) > 0 and int(BIT_ASSIGNMENT_S[abs(int(clause[i])) - 1]) == 1:
				clauseFlag = True
		if clauseFlag == False:
			flag = False
			break

	return flag



#generates the output line for the wff in the desired format
def output(verified):
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
		bit_list = list(BIT_ASSIGNMENT_S)
		bit_string = ','.join(bit_list)
		# Prob No., No. Var., No. Clauses, Max Lit., Tot. Lit., S/U, 1/-1, Exec. Time, 1/0 (SAT)
		print('{0},{1},{2},{3},{4},{5},{6},{7:.2f},{8}'.format(COMMENT_LINE[1], PROBLEM_LINE[2], PROBLEM_LINE[3], COMMENT_LINE[2], TOT_LITERALS, SAT, COMPARE, EXECUTION_TIME, bit_string))
	else:
		NUM_U = NUM_U + 1
		print('{0},{1},{2},{3},{4},{5},{6},{7:.2f}'.format(COMMENT_LINE[1], PROBLEM_LINE[2], PROBLEM_LINE[3], COMMENT_LINE[2], TOT_LITERALS, SAT, COMPARE, EXECUTION_TIME))



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
					output(flag)

print('{0},cde,{1},{2},{3},{4},{5}'.format(FILE_NAME, num_wffs, NUM_S, NUM_U, NUM_ANSWERS, NUM_CORRECT))