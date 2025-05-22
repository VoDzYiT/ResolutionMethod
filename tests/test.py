import unittest
from src.logic import *


class TestResolutionMethod(unittest.TestCase):
    def setUp(self):
        self.a = Literal('A')
        self.b = Literal('B')
        self.c = Literal('C')
        self.d = Literal('D')
        self.e = Literal('E')

    def test_to_cnf_set(self):
        a = self.a
        b = self.b

        self.assertEqual(to_cnf_set(And(a, b)), [[a], [b]])
        self.assertEqual(to_cnf_set(And(Or(a, b))), [[a, b]])
        self.assertEqual(to_cnf_set(And(Or(a, b), Or(Not(a), b))), [[a, b], [Not(a), b]])

    def test_to_cnf(self):
        a = self.a
        b = self.b
        # Distributive law
        self.assertEqual(to_cnf(Or(And(a, b), And(a, b))).__str__(), "(((A ∨ A) ∧ (B ∨ A)) ∧ ((A ∨ B) ∧ (B ∨ B)))")
        self.assertEqual(to_cnf(Or(a, And(a, b))).__str__(), "((A ∨ A) ∧ (B ∨ A))")

    def test_resolve(self):
        a = self.a
        b = self.b
        c = self.c
        d = self.d

        function_true_1 = And(Or(a, b), Or(Not(a), Not(b)))
        resolve = Resolution(function_true_1)
        self.assertEqual(resolve.resolve(), True)

        function_false_1 = And(Or(a, b), Or(Not(a), b))
        resolve = Resolution(function_false_1)
        self.assertEqual(resolve.resolve(), False)

        function_true_2 = And(a, Not(a))
        resolve = Resolution(function_true_2)
        self.assertEqual(resolve.resolve(), True)

        function_true_3 = And(Or(a, b), Or(Not(a), c), Not(b), Not(c))
        resolve = Resolution(function_true_3)
        self.assertEqual(resolve.resolve(), True)

        function_true_4 = Or(And(
            Or(
                And(a, b),
                And(c, d)),
            Or(Not(a), Not(c)),
            Or(Not(a), Not(d)),
            Or(Not(b), Not(c)),
            Or(Not(b), Not(d))
        ))
        resolve = Resolution(function_true_4)
        self.assertEqual(resolve.resolve(), True)


    def test_resolve_case1(self):
        a = Literal("a")
        b = Literal("b")
        clause1 = [a, b]
        clause2 = [Not(a), Not(b)]
        expected = [[a, Not(a)], [b, Not(b)]]
        result = resolve(clause1, clause2)
        self.assertEqual(expected, result)

    def test_resolve_case2(self):
        a = Literal("a")
        b = Literal("b")
        clause1 = [a, b]
        clause2 = [a, Not(b)]
        expected = [b, Not(b)]
        result = resolve(clause1, clause2)
        self.assertEqual(expected, result)

    def test_resolve_case3(self):
        a = Literal("a")
        b = Literal("b")
        clause1 = [a, b]
        clause2 = [a, b]
        expected = None
        result = resolve(clause1, clause2)
        self.assertEqual(expected, result)





if __name__ == '__main__':
    unittest.main()
