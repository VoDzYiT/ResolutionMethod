from .expressions import Literal
from .transformations import resolve, to_cnf, to_cnf_set



class Resolution:
    def __init__(self, formula):
        self.formula = formula

    def resolve(self):
        formula = to_cnf(self.formula)
        cnf_set = to_cnf_set(formula)

        changed = True
        while changed:
            changed = False
            i = 0

            while i < len(cnf_set):
                j = i + 1
                while j < len(cnf_set):
                    clause1 = cnf_set[i]
                    clause2 = cnf_set[j]

                    conflicting = resolve(clause1, clause2)
                    if conflicting is not None:
                        lit1, lit2 = conflicting

                        # Simplify clauses depending on the length and conflict type
                        if isinstance(lit1, list) or (len(clause1) == 1 and isinstance(lit1, Literal)):
                            cnf_set.pop(max(i, j))
                            cnf_set.pop(min(i, j))
                        elif len(clause1) == 1:
                            cnf_set.pop(i)
                            clause2.remove(lit2)
                        elif len(clause2) == 1:
                            cnf_set.pop(j)
                            clause1.remove(lit1)
                        else:
                            clause1.remove(lit1)
                            clause2.remove(lit2)

                        changed = True
                        break

                    j += 1

                if changed:
                    break
                i += 1

        return len(cnf_set) == 0

    def __str__(self):
        return f'({self.formula})'
