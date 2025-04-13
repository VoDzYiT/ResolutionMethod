from logic import *


rain = Literal('Rain')
work = Literal('Work')
sleep = Literal("Sleep")

print(Not(Not(work)))


formula = And(Or(rain, sleep), Or(sleep, work), rain, Not(sleep))

# class1 = Resolution(formula, work)
# class2 = Resolution(rain, rain)
# class3 = Resolution(rain, work)

# print(class2.resolve())

A = Literal('A')
B = Literal('B')
C = Literal('C')
D = Literal('D')
E = Literal('E')

def tests():
    print('===Test1: True ===')
    formula1 = And(A, Not(A))
    resolve1 = Resolution(formula1)
    print(resolve1.resolve())

    print('===Test2: False ===')
    formula2 = And(Or(A, B), Or(Not(A), C))
    resolve2 = Resolution(formula2)
    print(resolve2.resolve())

    print('===Test3: True ===')
    formula3 = And(Or(A, B), Or(Not(A), C), Not(B), Not(C))
    resolve3 = Resolution(formula3)
    print(resolve3.resolve())

    print('===Test4: False ===')
    formula3 = And(Or(And(A, B), And(C, D)))
    resolve3 = Resolution(formula3)
    print(resolve3.resolve())



tests()
print('===Test5: False ===')
formula4 = Or(And(
    Or(
        And(A, B),
        And(C, D)),
    Or(Not(A), Not(C)),
    Or(Not(A), Not(D)),
    Or(Not(B), Not(C)),
    Or(Not(B), Not(D))
))
resolve4 = Resolution(formula4)
print(resolve4.resolve())

a = Literal("a")
b = Literal("b")
expr = And(a, Or(a, b))
expr2 = Or(a, And(a, b))
expected = [[a, b], [Not(a), b]]
result = to_cnf(expr)
print(to_cnf(Or(And(a, b), And(a, b))))
print(to_cnf(Or(And(a, b), a)))
