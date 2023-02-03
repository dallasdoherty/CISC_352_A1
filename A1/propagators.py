# =============================
# Student Names: 
# Group ID: 50
# Date: January 31st, 2023
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) tuple_valss.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values tuple_valss are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple_vals(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value tuple_valss and return '''
    pruned = []
    constraints = []
    
    # If newVar is None, forward check all constraints
    if(newVar == None):
        constraints = csp.get_all_cons()
    # Otherwise only check constraints containing newVar
    else:
        constraints = csp.get_cons_with_var(newVar)
    for cons in constraints:
        # Only checking constraints that have one unassigned variable in their scope
        if cons.get_n_unasgn() == 1:
            var = cons.get_unasgn_vars()[0]
            # Iterate through the other variables that are connected to var (unassigned)
            for val in var.cur_domain():    
                # Check if a satisfying tuple_vals exists          
                if not cons.check_var_val(var, val):
                    tuple_vals = (var, val)
                    if(tuple_vals not in pruned):
                        pruned.append(tuple_vals)
                        var.prune_value(val)
            # No possible assignements, this is considered failure. Now have to backtrack
            if var.cur_domain_size() == 0:
                return False, pruned
    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    pruned = []
    GAC_queue = []
    
    if(newVar == None):
        constraints = csp.get_all_cons()
    else:
        constraints = csp.get_cons_with_var(newVar)
    
    for c in constraints:
        GAC_queue.append(c)
    
    while len(GAC_queue) != 0:
        c = GAC_queue.pop(0)
        for var in c.get_scope():
            for d in var.cur_domain():
                if not c.check_var_val(var, d):
                    tuple_vals = (var, d)
                    if(tuple_vals not in pruned):
                        pruned.append(tuple_vals)
                        var.prune_value(d)
                    if var.cur_domain_size() == 0:
                        GAC_queue.clear()
                        return False, pruned
                    else:
                        for cons in csp.get_cons_with_var(var):
                            if (cons not in GAC_queue):
                                GAC_queue.append(cons)
    return True, pruned
