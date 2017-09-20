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
COMMENT_LINE = []  #  Array - ['c', prob. no., max # literals, (un)solvability]
PROBLEM_LINE = []  #  Array - ['p', file format, # variables, # clauses]



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
	#print(INPUT)


#generates the next possible assingment for the current wff you are working with
#def nextPossibleAssignment():


#takes a wff and an assignment and returns whether or not the assignment satisfied the wff
def verify(assignment):
	bit_assignment = bin(assignment)
	# print bit_assignment
	variable_assignments = []

	bit_assignment_s = (str(bit_assignment))[2:].zfill(int(PROBLEM_LINE[2]))
	#print(bit_assignment_s)

	#print(WFF)

	WFF_Clauses = WFF.split(',0')
	WFF_Clauses.remove('')
	#print(WFF_Clauses)
	for clause in WFF_Clauses:
		clause = clause.split(',')
		#print(clause)

	# Iterate through 
	# for i in range(0, int(PROBLEM_LINE[2])):
	# 	variable_assignments[i] = int(bit_assignment_s[i])



#generates the output line for the wff in the desire format
def output():
	print('lol')

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

for i in range(0, len(lines)):
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
		WFF = WFF + lines[i].strip('\r')

		# If the next character is a 'c', evaluate the current WFF
		if i < (len(lines) - 2):
			if 'c' in lines[i+1]:
				#print("Found new clause")

				# Iterate through each possible character and verify check it
				assignment = 0
				for x in xrange(2**int(PROBLEM_LINE[2])):
					if(verify(assignment)):
						output();
						break
					assignment = assignment + 1