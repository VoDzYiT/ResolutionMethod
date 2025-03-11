class Literal:
    def __init__(self, value, negated ):
        self.value = value
        self.negated = negated
    def __str__(self):
        return f'{"¬" + self.value if self.negated else self.value}'

class And:
    def __init__(self, Literal1, Literal2):
        self.Literal1 = Literal1
        self.Literal2 = Literal2
    def __str__(self):
        return f'({self.Literal1} ∧ {self.Literal2})'

class Or:
    def __init__(self, Literal1, Literal2):
        self.Literal1 = Literal1
        self.Literal2 = Literal2
    def __str__(self):
        return f'({self.Literal1} V {self.Literal2})'

class Formula:
    def __init__(self, information):
        self.clauses = information

class Resolution:
    def __init__(self, formula, theorem):
        self.formula = formula
        self.theorem = theorem

    def resolve(self):

        pass

    def __str__(self):
        return f'({self.formula} ⇒ {self.theorem})'
