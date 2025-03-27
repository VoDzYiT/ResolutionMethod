class Literal:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Literal) and self.name == other.name
        # return isinstance(other, Not) and self.name == other.literal

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.name)


class Not:
    def __init__(self, literal):
        self.literal = literal

        # if isinstance(literal, Not):
        #     self.literal = literal.literal
        # else:
        #     self.literal = literal

    def __str__(self):
        return f"¬{self.literal}"

    def __eq__(self, other):
        if isinstance(other, Not):
            return self.literal == other.literal

        return isinstance(other, Not) and self.literal.name == other.literal.name
        # return isinstance(other, Literal) and self.literal == other.name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(("¬", self.literal))


class And:
    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return f"({' ∧ '.join(map(str, self.args))})"

    def __iter__(self):
        for arg in self.args:
            if isinstance(arg, (And, Or)):
                yield from arg
            else:
                yield arg



class Or:
    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return f"({' ∨ '.join(map(str, self.args))})"

    def __iter__(self):
        for arg in self.args:
            if isinstance(arg, (And, Or)):
                yield from arg
            else:
                yield arg


class Resolution:
    def __init__(self, formula):
        self.formula = formula
        # self.theorem = Or(*[Not(literal) for literal in (theorem if isinstance(theorem, (list, tuple)) else [theorem])])
        # self.theorem = Or(*[Not(literal) for literal in ([theorem] if isinstance(theorem, Literal) or isinstance(theorem, Not) else theorem)])
        # self.formula.append(self.theorem)

    def resolve(self):
        formula = to_cnf(self.formula)
        disjunction_set = to_disjunction_set(formula)
        print(disjunction_set)
        while True:
            new = set()

            for i, clause1 in enumerate(disjunction_set):
                for j, clause2 in enumerate(disjunction_set):
                    if i >= j:
                        continue

                    resolvent = resolve(clause1, clause2)
                    if resolvent is not None:
                        new.add(tuple(resolvent))

            print(new)
            filtered_disjunction_set = [
                [item for item in sublist if all(item not in pair for pair in new)]
                for sublist in disjunction_set
            ]

            print(filtered_disjunction_set)

            for item in filtered_disjunction_set:
                if item != []:
                    return False

            return True

    def __str__(self):
        return f'({self.formula})'


def to_cnf(expr):
    if isinstance(expr, And):
        # Якщо це And, зводимо кожен аргумент до КНФ
        return And(*[to_cnf(arg) for arg in expr.args])

    elif isinstance(expr, Or):
        # Перевіряємо, чи є всередині Or хоча б один And
        for arg in expr.args:
            if isinstance(arg, And):
                # Дистрибутивний закон: A ∨ (B ∧ C) → (A ∨ B) ∧ (A ∨ C)
                i = expr.args.index(arg)
                new_clauses = [Or(*[to_cnf(sub), *(expr.args[:i] + expr.args[i + 1:])]) for sub in arg.args]
                return to_cnf(And(*new_clauses))

        # 🔹 Очищуємо вкладені Or перед поверненням
        new_args = []
        for arg in expr.args:
            if isinstance(arg, Or):  # Якщо це Or(A, B), то розгортаємо
                new_args.extend(arg.args)
            else:
                new_args.append(arg)

        return Or(*new_args)

    # Якщо це просто літерал, повертаємо його
    else:
        return expr



def to_disjunction_set(expression):
    disjunction_set = []

    def extract_literals(expr):
        if isinstance(expr, Or):
            return [lit for sub in expr.args for lit in extract_literals(sub)]
        elif isinstance(expr, And):
            flattened = []
            for sub in expr.args:
                sub_literals = extract_literals(sub)
                if isinstance(sub_literals[0], list):  # Якщо вкладений список, розгортаємо
                    flattened.extend(sub_literals)
                else:
                    flattened.append(sub_literals)
            return flattened
        else:
            return [expr]

    if isinstance(expression, And):
        for sub_expr in expression.args:
            literals = extract_literals(sub_expr)
            if isinstance(literals[0], list):  # Уникаємо додаткової вкладеності
                disjunction_set.extend(literals)
            else:
                disjunction_set.append(literals)
    elif isinstance(expression, Or):
        disjunction_set.append(extract_literals(expression))
    else:
        disjunction_set.append([expression])

    return disjunction_set




def resolve(clause1, clause2):
    """
    Виконує резолюцію між двома диз'юнктами clause1 та clause2.
    Повертає новий диз'юнкт або None, якщо резолюція неможлива.
    """

    # Перетворюємо аргументи на списки, якщо вони не є ітерабельними
    clause1 = clause1 if isinstance(clause1, (list, set)) else [clause1]
    clause2 = clause2 if isinstance(clause2, (list, set)) else [clause2]

    # Знаходимо суперечливі літерали (наприклад, Rain та ¬Rain)

    new_clause = []
    resolved = False

    for lit1 in clause1:
        for lit2 in clause2:
            if lit1 == Not(lit2) or Not(lit1) == lit2:
                return [lit1, lit2]
            else:
                new_clause.append(lit1)  # Додаємо літерали без суперечностей

    return None  # Якщо не знайшли суперечливих пар, резолюція неможлива