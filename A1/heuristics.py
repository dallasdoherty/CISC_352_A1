

#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''
    # IMPLEMENT
    # get list of unassigned variables, iterate through each one getting list of variables in constraint
    # for each value in constraint, update corresponding value and dictionary
    # return max value of dict (variable that appears the most in constraints of other variables)
    all_vars = csp.get_all_unasgn_vars()
    # if everything is assigned except for the last variable, return that variable
    if len(all_vars) == 1:
        return all_vars[0]
    var_dict = {}
    # Iterate through all constraints
    for cons in csp.get_all_cons():
        # Iterate through unassigned variables in these constraints
        for var in cons.get_unasgn_vars():
            # Add the variable to var_dict when it appears
            if var in var_dict:
                var_dict[var] += 1
            else:
                var_dict[var] = 0
    # Return the most constrained variable
    max_key = max(var_dict, key=var_dict.get)
    return max_key
    

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    # return the variable with the fewest legal values remaining
    # iterate through variables and call curr_domain on each one, if less than max, set as new lowest and return lowest at the end
    all_vars = csp.get_all_unasgn_vars()
    # Set the min value as infinity so anything smaller will take its place
    min_cur_domain = float('inf')
    return_var = None
    # Iterate through all unassigned variables
    for var in all_vars:
        # If the current variable has fewer legal values, set it as the new min
        if var.cur_domain_size() < min_cur_domain:
            min_cur_domain = var.cur_domain_size()
            return_var = var
    return return_var



