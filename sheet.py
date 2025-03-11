from Main import *


rain = Literal('Rain', False)
work = Literal('Work', True)
sleep = Literal("Sleep", False)

and1 = And(rain, work)

resolve = Resolution(and1, sleep)

print(resolve)

formula = Formula(and1)
