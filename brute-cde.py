# brute-cde.py  :  brute forces sat
# Team          :  . . .
# Date          :  . . .


# Imports:
import sys
import os

# Globals:
FILE_NAME = ''
BINARY = ''

#one command line argument --> name of file to read wffs in from
#binary argument that turns on or off optional tracing 1 yes, 0 not

def usage(exit_status=0):
	print('''Usage: brute-cde.py [FILE_NAME] [BINARY]
		FILE_NAME			The file to be read that contains wffs.
		BINARY 				1 = Triggers Optional Tracing ; 0 = Suppress Intermediate Output''')
	sys.exit(exit_status)

def readFile():
	print('lol')
#reads in the next wff from a specified input file

def nextPossibleAssignment():
	print('lol')
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
if len(sys.argv[1:]) != 3:
	usage(1)
FILE_NAME = sys.argv[1]
BINARY = sys.argv[2]

with open(FILE_NAME) as f:
	lines = f.readlines()