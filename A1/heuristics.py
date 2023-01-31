# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


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
    count = {}

    vars = csp.get_all_unasgn_vars()
    for v in vars:

        #add v to dictionary as key
        count[v] = 0

        #loop through list of all constraints in the CSP w/h v
        for c in csp.get_all_cons_with_var(v):
            if c.get_n_unasgn() != 0:
                for uv in c.get_unasgn_vars():
                    if uv != v:
                        count[v] += 1
    val = list(count.values())

    key = list(count.keys())
    dh_var = key[val.index(max(val))]

    return dh_var   

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    md = -1
    mv = None

    for v in csp.get_all_unasgn_vars():
        if md < 0:
            md = v.cur_domain_size()
            mv = v
        elif v.cur_domain_size() < md:
            md = v.cur_domain_size()
            mv = v
    csp.get_all_unasgn_vars().remove(mv)
    return mv
