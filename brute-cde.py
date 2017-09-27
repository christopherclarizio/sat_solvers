# brute-cde.py  :  brute forces sat
# Team          :  . . .
# Date          :  . . .


# Imports:
import sys
import os
import string
import time

# Globals:
FILE_NAME = ''
BINARY = ''
INPUT = ''
WFF = ''
COMMENT_LINE = []    #  Array - ['c', prob. #, max # literals, (un)solvability]
PROBLEM_LINE = []    #  Array - ['p', file format, # variables, # clauses]
TOT_LITERALS = 0     #  Needed for output
START_TIME   = None  #  Needed for execution time
END_TIME     = None  #    "     "      "      "

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
	bit_assignment = bin(assignment)
	variable_assignments = []
	bit_assignment_s = (str(bit_assignment))[2:].zfill(int(PROBLEM_LINE[2]))

	WFF_Clauses = WFF.split(',0')
	WFF_Clauses.remove('')

	TOT_LITERALS = len(WFF.split(',')) - int(PROBLEM_LINE[3])

	flag = True  #  Switch flag if assignment fails the clause.
	
	for clause in WFF_Clauses:
		clause = clause.split(',')  #  '-1,2,3'  --> ['-1', '2', '3']
		clauseFlag = False
		for i in xrange(0, len(clause)):
			if int(clause[i]) < 0 and int(bit_assignment_s[i]) == 0:
				clauseFlag = True
				break
			elif int(bit_assignment_s[i]) == 1:
				clauseFlag = True
				break
		if clauseFlag == False:
			flag = False
			break

	return flag

	# Iterate through 
	# for i in range(0, int(PROBLEM_LINE[2])):
	# 	variable_assignments[i] = int(bit_assignment_s[i])



#generates the output line for the wff in the desired format
def output(verified):
	# Predict SAT.
	SAT = 'U'
	if verified:
		SAT = 'S'

	# Compare SAT to Answer SAT.
	COMPARE = '0'
	if SAT == COMMENT_LINE[3]:
		COMPARE = '1'

	# Prob No., No. Var., No. Clauses, Max Lit., Tot. Lit., S/U, 1/-1, Exec. Time, 1/0 (SAT)
	print('{0},{1},{2},{3},{4},{5},{6},{7:.2f},{8}'.format(COMMENT_LINE[1], PROBLEM_LINE[2], PROBLEM_LINE[3], COMMENT_LINE[2], TOT_LITERALS, SAT, COMPARE, (END_TIME-START_TIME)* 10**6, ))

#should time the execution time take for each wff starting with the first call 
#to the assignment generator to the completion of the call to verify and avoid the
#time to read and parse the wff from the given file and the tiem to generate the output file
#this time should be in microseconds

#using package time; time.time(), gives current time in seconds.


# Parse Command Line:
if len(sys.argv[1:]) != 2:
	usage(1)
FILE_NAME = sys.argv[1]
BINARY = sys.argv[2]

readFile() # INPUT contains raw file

lines = INPUT.split('\n')

count = 0
for i in range(0, len(lines)):
	if count == 1:
		break
	# Check for 'p' Lines:
	if 'p' in lines[i]:
		#print("Found 'p'")
		strippedLine = lines[i].strip('\r')
		PROBLEM_LINE = strippedLine.split(' ')
	
	# Check For 'c' Lines:
	elif 'c' in lines[i]:
		#print("Found 'c'")
		COMMENT_LINE = []
		PROBLEM_LINE = []

		strippedLine = lines[i].strip('\r')
		COMMENT_LINE = strippedLine.split(' ')
	
	# Add WFF lines to WFF string
	else:
		if int(PROBLEM_LINE[2]) <= 10:  #  FOR TESTING PURPOSES
			WFF = WFF + lines[i].strip('\r')
			print(WFF)
			count = count + 1
			# If the next character is a 'c', evaluate the current WFF
			if i < (len(lines) - 2):
				if 'c' in lines[i+1]:
					#print("Found new clause")

					# Iterate through each possible character and verify check it
					assignment = 0
					flag = False
					START_TIME = time.time()
					for x in xrange(2**int(PROBLEM_LINE[2])):
						if(verify(assignment)):
							flag = True
							break
						assignment = assignment + 1
					END_TIME = time.time()
					output(flag)