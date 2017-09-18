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

#def nextPossibleAssignment():
#generates the next possible assingment for the current wff you are working with

def verify():
	print('lol')
#takes a wff and an assignment and returns whether or not the assignment satisfied the wff

def output():
	print('lol')
#generates the output line for the wff in the desire format

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

readFile()
#INPUT contains raw file

count = 0

lines = INPUT.split('\n')

for line in lines:
	print(line)
	# Check For 'c' Lines:
	if 'c' in line:
		strippedLine = line.strip('\r')
		COMMENT_LINE = strippedLine.split(' ')
		count = count + 1
		#print(COMMENT_LINE)
		#time.sleep(5)
	# Check for 'p' Lines:
	elif 'p' in line:
		strippedLine = line.strip('\r')
		PROBLEM_LINE = strippedLine.split(' ')
	# Add WFF lines to WFF string
	else:
		WFF.append(line.strip('\r'))
	# If the next character is a 'c', evaluate the current WFF
	if(lines):
		# Iterate through each possible character and verify check it
		assignment = 0
		for x in xrange(2**PROBLEM_LINE[2]):
			assignment = assignment + 1
			if(verify(assignment)):
				output();
				break

	if count >= 2:
		count = 0
		COMMENT_LINE = ''
		PROBLEM_LINE = ''
		break