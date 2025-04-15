from .expressions import Literal
from .transformations import resolve, to_cnf, to_cnf_set



class Resolution:
    def __init__(self, formula):
        self.formula = formula

    def resolve(self):
        formula = self.formula
        # print(formula)
        formula = to_cnf(self.formula)
        # print(formula)
        cnf_set = to_cnf_set(formula)
        # print(cnf_set)

        changed = True
        while changed:
            changed = False
            i = 0
            while i < len(cnf_set):
                j = i + 1
                while j < len(cnf_set):
                    clause1 = cnf_set[i]
                    clause2 = cnf_set[j]
                    controversial = resolve(clause1, clause2)
                    if controversial is not None:

                        lit1, lit2 = controversial

                        if isinstance(lit1, Literal) and len(clause1) == 1:
                            cnf_set.pop(j)
                            cnf_set.pop(i)
                            changed = True

                            break

                        if isinstance(lit1, list):
                            cnf_set.pop(j)
                            cnf_set.pop(i)
                            changed = True

                            break

                        if len(clause1) == 1 and len(clause2) != 1:
                            cnf_set.pop(i)
                            clause2.remove(lit2)
                            changed = True
                            break
                        if len(clause2) == 1 and len(clause1) != 1:
                            cnf_set.pop(j)
                            clause1.remove(lit1)
                            changed = True
                            break

                        clause1.remove(lit1)
                        clause2.remove(lit2)

                        changed = True
                        break

                    changed = False
                    j += 1

                    if changed:
                        break

                if not (changed):
                    i += 1

            if cnf_set:
                return False

            return True

    def __str__(self):
        return f'({self.formula})'
