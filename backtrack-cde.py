# backtrack-cde.py  :  tree evaluates sat
# Team          :  CDE: Chris-Donny-Emily
# Date          :  9-26-17


# Imports:
import sys
import os
import string
import time
import random

# Globals:
VALUE_STACK = []
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
	value_stack = [] # Stack with values for variables ex) [0, 1, 1, 0, 0]
	wff_stack = [] # Stack with wffs in characterronological order, each one in gets more reduced
	tried_stack = [] # Keeps track of variables for which both values were tried
	flag = False
	evaluating = True
	backtrack = False

	WFF_Clauses = WFF.split(',0')
	WFF_Clauses.remove('') 	

	wff_stack.append(WFF_Clauses)

	global TOT_LITERALS
	TOT_LITERALS = len(WFF_Clauses) * len(WFF_Clauses[2].split(','))

	while evaluating:
		num_trues = 0
		for var in tried_stack: # Count the number of trues
			if var == True:
				num_trues = num_trues + 1

		num_trues_row  = 0
		for rev in reversed(tried_stack): # Count the number of trues in a row from the bottom
			if rev == True:
				num_trues_row = num_trues_row + 1
			else:
				break

		if num_trues == PROBLEM_LINE[2]: # If the number of trues is equal to the number of variables, all variables have tried all possibilities and the wff is unsatisfiable
			evaluating = False
			break
		
		

		if len(tried_stack) == 0 and len(value_stack) != 0: # If the number of trues is equal to the number of variables, all variables have tried all possibilities and the wff is unsatisfiable
			evaluating = False
			break

		num_clauses = 0
		for c in wff_stack[-1]:
			if c != '':
				num_clauses = num_clauses + 1

		if num_clauses == 0: # If the most recent wff is empty, then the wff is satisfiable
			flag = True
			evaluating = False
			break
		elif len(value_stack) == int(PROBLEM_LINE[2]): # If we have reached the end of a branch (we have all variables assigned to something) backtrack and reassign that value
			tried_value = value_stack.pop()
			wff_stack.pop()
			if tried_value == 0: # If the current variable is being reassigned, then it has tried both options and cannot be tried again
				value_stack.append(1)
				tried_stack.pop()
				tried_stack.append(True)
			else:
				value_stack.append(0)
				tried_stack.pop()
				tried_stack.append(True)
		elif backtrack == True: # Backtrack if any of the clauses in the previous wff were false
			tried_value = value_stack.pop()
			wff_stack.pop()
			if tried_value == 0: # If the current variable is being reassigned, then it has tried both options and cannot be tried again
				value_stack.append(1)
				tried_stack.pop()
				tried_stack.append(True)
			else:
				value_stack.append(0)
				tried_stack.pop()
				tried_stack.append(True)
		else: # Go down the tree and assign randomly the next variable value
			value_stack.append(random.randint(0,1))
			tried_stack.append(False)


		if len(tried_stack) > 1 and tried_stack[-1] == True: # If both values were tried for the current variable, backtrack twice and reassign variable from above
			for i in xrange(0, num_trues_row):
				value_stack.pop()
				if len(wff_stack) != 1:
					wff_stack.pop()
				tried_stack.pop()
			if len(tried_stack) == 0:	
				break
			tried_stack.pop()
			tried_value = value_stack.pop()
			if tried_value == 0: # If the current variable is being reassigned, then it has tried both options and cannot be tried again
				value_stack.append(1)
				tried_stack.append(True)
			else:
				value_stack.append(0)
				tried_stack.append(True)
		
		backtrack = False
		Clauses_Next = wff_stack[-1][:] # Initialize the next wff as the current wff
		remove_clauses = [] # List of clauses to be removed from current wff
		index_count = 0

		for clause in Clauses_Next: # Here, we go through the current wff and edit it to create the next wff
			variables = clause.split(',')  #  '-1,2,3'  --> ['-1', '2', '3']
			remove_variables = []
			variable_count = 0
			for variable in variables: # Go through each variable in the clause
				all_same = False
				if len(variables) > 1:
					all_same = True
					temp = variable
					for x in range(0, len(variables)): # Flag for if all variables in clause are the exact same variable
						if variables[x] == temp:
							temp = variables[x]
						else:
							all_same = False
							break
				if variable != '' and abs(int(variable)) == len(value_stack):
					if int(variable) < 0:
						if value_stack[-1] == 0: # If the variable is 1, this clause returns true and move on to next clause
							remove_clauses.append(index_count) # Add this clause to clauses to be removed
							break
						else: # If the variable is 0, it is removed and the rest of the clause moves on down the branch
							if not all_same and len(variables) != 1:
								remove_variables.append(variable_count)
					else:
						if value_stack[-1] == 1: # If the variable is 1, this clause returns true and move on to next clause
							remove_clauses.append(index_count) # Add this clause to clauses to be removed
							break
						else:  # If the variable is 0, it is removed and the rest of the clause moves on down the branch
							if not all_same and len(variables) != 1:
								remove_variables.append(variable_count)
				variable_count = variable_count + 1
			
			for ind in remove_variables:
				variables[ind] = ''

			Clauses_Next[index_count] = ','.join(variables)

				
			if Clauses_Next[index_count] != '' and Clauses_Next[index_count][0] == ',': # Remove leading comma
				Clauses_Next[index_count] = Clauses_Next[index_count][1:]

			if Clauses_Next[index_count] != '' and Clauses_Next[index_count][-1] == ',': # Remove trailing comma
				Clauses_Next[index_count] = Clauses_Next[index_count][:-1]

			commas = 0
			for char in Clauses_Next[index_count]:
				if char == ',':
					commas = commas + 1

			if commas == len(Clauses_Next[index_count]): # Remove clauses of just commas
				Clauses_Next[index_count] = ''
			
			length = 0
			for var in variables:
				if var != '':
					length = length + 1

			if length == 1 and variables[0] != '': # If a clause only has one variable and that variable evaluates 0, the entire wff is false so we backtrack
				if abs(int(variables[0])) == len(value_stack):
					if int(variables[0]) < 0:
						if value_stack[-1] == 1:
							backtrack = True
							break
					else:
						if value_stack[-1] == 0:
							backtrack = True
							break
			index_count = index_count + 1

		for i in remove_clauses: # where i is the indices of Clauses_Next to be removed
			Clauses_Next[i] = ''
		wff_stack.append(Clauses_Next) # Add the newly edited current wff to the stack

	global VALUE_STACK
	VALUE_STACK = value_stack
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
		bit_string = ','.join(str(val) for val in VALUE_STACK)
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
f = open('backtrack-'+OUTPUT_FILE+'.csv', 'w')

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