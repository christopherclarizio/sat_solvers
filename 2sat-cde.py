The third program, to be called 2sat-team, where where team is your team name, determines
satisfiability by observing that for 2SAT, if a value is assigned to a variable then any
clause that has a literal that requires the negation of that vale to be true will automatically
force an additional assignment to the variable associated with the second literal in the clause.
For example in (∼ x1 ∨ ∼ x2), if you tentatively assign a value of 1 to x1 then you must
assign “0” to x2 to make the second literal true. This new assignment can then make other
clauses true, and also force additional assignments to other variables. In many wffs the result
is like a long string of dominos arranged in tree-like structures - drop one and others fall,
perhaps on multiple branches.
If in the process of making such chained assignments, you ever find a case where you
are trying to assign both true and false to the same variable, then you have reached a
contradiction, and you must erase all these intermediate assignments and restart the process
3
with a different value to the original variable. If there are no alternatives to look at then it
is unsatisfiable. This is essentially the same as the backtracking in the prior program.
If these chained assignments do not result in a conflict, then you know you have a satisfying
assignment for the set of clauses that have been made true so far, and that all remaining
clauses do not depend on any of the variables assigned so far. You can thus freeze the
assignment and start working on the clauses that have not yet been affected as essentially a
separate, and smaller, problem.
An interesting observation is that you can actually build this trick into the prior backtrack
program. During the testing of an assignment, if you reach a clause where all but one literal
is false, and the final literal’s value does not have a value yet, you can force a new assignment
to make the literal true