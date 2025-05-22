from .expressions import Or, Not, And, Implication

def to_cnf(expr):
    """
    Transform function to cnf form using distributive law

    return function thar has conjunction normal form
    for example And(a, b) -> And(a, b) (It was already in CNF)
                Or(a, And(b, c)) -> And(Or(a, b), Or(c, a))
    """

    if isinstance(expr, And):
        # If it is And, we reduce each argument to a CNF
        return And(*[to_cnf(arg) for arg in expr.args])

    elif isinstance(expr, Or):
        # Check if there is at least one And inside Or
        for arg in expr.args:
            if isinstance(arg, And):
                # Distribution law: A ∨ (B ∧ C) → (A ∨ B) ∧ (A ∨ C)
                i = expr.args.index(arg)
                new_clauses = [Or(*[to_cnf(sub), *(expr.args[:i] + expr.args[i + 1:])]) for sub in arg.args]
                return to_cnf(And(*new_clauses))

        # Clear nested Ors before returning
        new_args = []
        for arg in expr.args:
            if isinstance(arg, Or):
                new_args.extend(arg.args)
            elif isinstance(arg, Implication):
                new_args.append(to_cnf(Or(Not(arg.left), arg.right)))
            else:
                new_args.append(arg)

        return Or(*new_args)
    if isinstance(expr, Implication):
        # A → B = ¬A ∨ B
        return to_cnf(Or(Not(expr.left), expr.right))

    # If it's just a literal, return it
    else:
        return expr



def to_cnf_set(expression):
    """
        Transform expression to cnf set

        return set of disjunctions like [[A, B], [C, D]] which is equivalent to And(Or(A, B), Or(C, D))
    """
    cnf_set = []

    def extract_literals(expr):
        if isinstance(expr, Or):
            return [lit for sub in expr.args for lit in extract_literals(sub)]
        elif isinstance(expr, And):
            flattened = []
            for sub in expr.args:
                sub_literals = extract_literals(sub)
                if isinstance(sub_literals[0], list):  # If the list is nested, expand
                    flattened.extend(sub_literals)
                else:
                    flattened.append(sub_literals)
            return flattened
        else:
            return [expr]

    if isinstance(expression, And):
        for sub_expr in expression.args:
            # Extract literals from sub_expression
            # Return a list with literals
            literals = extract_literals(sub_expr)
            if isinstance(literals[0], list):  # Avoid additional nesting
                cnf_set.extend(literals)
            else:
                cnf_set.append(literals)

    elif isinstance(expression, Or):
        for sub_expr in expression.args:
            # Extract literals from sub_expression
            # Return a list with literals
            literals = extract_literals(sub_expr)
            if isinstance(literals[0], list):  # Avoid additional nesting
                cnf_set.extend(literals)
            else:
                cnf_set.append(literals)
    else:
        cnf_set.append([expression])

    return cnf_set




def resolve(clause1, clause2):
    """
    Performs a resolution between the two clauses clause1 and clause2.
    Returns a new disjunction with pairs of negative literals or None if resolution is not possible.
    Handles cases when a clause has 2 literals, when more will not work:(
    """

    # Find contradictory literals (for example, Rain and ¬Rain)

    new_clause = []

    for lit1 in clause1:
        for lit2 in clause2:
            if lit1 == Not(lit2) or Not(lit1) == lit2:

                if new_clause:
                    tmp = new_clause
                    new_clause = []
                    new_clause.append(tmp)
                    new_clause.append([lit1, lit2])
                else:
                    new_clause.append(lit1)
                    new_clause.append(lit2)
    if new_clause:
        return new_clause
    return None