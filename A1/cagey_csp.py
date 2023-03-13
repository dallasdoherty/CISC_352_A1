

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.
For example, after these three lines of code
    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)
var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).
1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.
2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.
3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.
Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+
Boards are given in the following format:
(n, [cages])
n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.
each cage has the following structure
(v, [c1, c2, ..., cm], op)
v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given
An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])
'''

import itertools
from cspbase import *
from itertools import permutations, combinations



def binary_ne_grid(cagey_grid):
    domain_arr = [] # Create domain array for varaiables
    array_of_variables = [] # array containing vars
    sizeOf = cagey_grid[0] # Size of the cagey grid  
    for i in range(1, sizeOf+1): # Add all values between 1 - n to the domain array
        domain_arr.append(i)
    array_of_variables = []
    var_list = [[0]*sizeOf for i in range(sizeOf)]
    for i in range(sizeOf):
        for j in range(sizeOf):
            tmp = Variable("cell(" + str(i+1) + "," + str(j+1) + ")", domain_arr)
            var_list[i][j] = tmp
            array_of_variables.append(tmp)

    csp_binary = CSP("binary CSP", array_of_variables)
    row = []
    tuples= []
    for i in range(sizeOf): 
            row.clear()
            for j in range(sizeOf):
                row.append(var_list[i][j])
            # constraints only between two vars(binary)
            for t in itertools.combinations(row, 2):
                constraint = Constraint("col" + str(i), row)
                tuples.clear()
                for t in itertools.permutations(domain_arr, 2):
                    tuples.append(t)
                constraint.add_satisfying_tuples(tuples)
                csp_binary.add_constraint(constraint)
    column = []
    for i in range(sizeOf):
            column.clear()
            for j in range(sizeOf): 
                column.append(var_list[j][i])
                # constraints only between two vars(binary)
            for t in itertools.combinations(column, 2):
                constraint = Constraint("col" + str(i), column)
                tuples.clear()
                for t in itertools.permutations(domain_arr, 2):
                    tuples.append(t)
                constraint.add_satisfying_tuples(tuples)
                csp_binary.add_constraint(constraint)

    return csp_binary, var_list

def nary_ad_grid(cagey_grid):
    domain_arr = [] # Create domain array for varaiables
    array_of_variables = [] # array containing vars
    sizeOf = cagey_grid[0] # Size of the cagey grid  
    for i in range(1, sizeOf+1): # Add all values between 1 - n to the domain array
        domain_arr.append(i)

    var_list = [[0]*sizeOf for i in range(sizeOf)]
    for i in range(sizeOf):
        for j in range(sizeOf):
            tmp = Variable("cell(" + str(i+1) + "," + str(j+1) + ")", domain_arr)
            var_list[i][j] = tmp
            array_of_variables.append(tmp)

    csp_nary = CSP("nary CSP", array_of_variables)
    row = []
    tuples = []
    for i in range(sizeOf):
        row.clear()
        for j in range(sizeOf):
            row.append(var_list[i][j])
        constraint = Constraint("row" + str(i+1), row)
        tuples.clear()
        for t in itertools.permutations(domain_arr):
            tuples.append(t)
        constraint.add_satisfying_tuples(tuples)
        csp_nary.add_constraint(constraint)
    column = []
    for i in range(sizeOf):
        column.clear()
        for j in range(sizeOf):
            column.append(var_list[j][i])
        constraint = Constraint("col" + str(i), column)
        tuples.clear()
        for t in itertools.permutations(domain_arr):
            tuples.append(t)
        constraint.add_satisfying_tuples(tuples)
        csp_nary.add_constraint(constraint)

    return csp_nary, array_of_variables

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    pass
