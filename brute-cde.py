#brute forces sat
#one command line argument --> name of file to read wffs in from
#binary argument that turns on or off optional tracing 1 yes, 0 not

def readFile():
#reads in the next wff from a specified input file

def nextPossibleAssignment():
#generates the next possible assingment for the current wff you are working with

def verify():
#takes a wff and an assignment and returns whether or not the assignment satisfied the wff

def output():
#generates the output line for the wff in the desire format

#should time the execution time take for each wff starting with the first call 
#to the assignment generator to the completion of the call to verify and avoid the
#time to read and parse the wff from the given file and the tiem to generate the output file
#this time should be in microseconds

#using package time; time.time(), gives current time in seconds.
