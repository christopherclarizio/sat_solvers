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

