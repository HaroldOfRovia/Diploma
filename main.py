import random

from GeneticAlgorithms.Classical import Classical
from baseLogic.Task import Task
from baseLogic.Unit import Unit
a0 = Task(0, 15, 0, 30)
a1 = Task(1, 10, 15, 25)
a2 = Task(2, 5, 0, 30)
a3 = Task(3, 15, 0, 50)
queue = Unit([a0,
              Task(1, 10, 15, 25),
              Task(2, 5, 0, 30),
              Task(3, 15, 0, 50),
              Task(4, 20, 80, 100),
              Task(5, 5, 40, 100),
              Task(6, 12, 60, 120),
              Task(7, 100, 70, 250),
              Task(8, 22, 10, 80),
              Task(9, 10, 30, 150)])
# queue = Unit([a0,
#               Task(1, 10, 15, 25),
#               Task(2, 5, 0, 30),
#               Task(3, 15, 0, 50),
#               Task(4, 20, 80, 100)])
# queue.__contains__(a)
queue0 = Unit([a3, a0, a1, a2])
queue1 = Unit([a3, a0, a2, a1])
queue2 = Unit([a2, a1, a0, a3])
queue3 = Unit([a3, a2, a0, a1])

gen = Classical(100, queue)
solved = False
while not solved:
    solved = gen.one_step(1, 2, 0.5, 1)
