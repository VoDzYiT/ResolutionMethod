from logic import *

# Firstly we need to create our literal
# Using the example from the README, we need to create 2 literals “Sunny” and “Play”
A = Literal("Sunny")
B = Literal("Play")

# After we need to connect them using implication
implication = Implication(A, B)

# Now we need to add knowledge and negation of goal
formula = And(Or(Not(A), B), A, Not(B))

# Now we apply resolution method to check if contradiction appears
# If we get True (an empty clause), it means our conclusion "Play" is logically valid
resolution = Resolution(formula)
print(resolution.resolve())
