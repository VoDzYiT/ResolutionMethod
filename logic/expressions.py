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

            yield arg



class Or:
    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return f"({' ∨ '.join(map(str, self.args))})"

    def __iter__(self):
        for arg in self.args:
            if isinstance(arg, Or):
                yield from arg
            else:
                yield arg
