import random

from GeneticAlgorithms.Classical import Classical
from baseLogic.Task import Task
from baseLogic.Unit import Unit

queue = Unit([Task(0, 15, 0, 30),
              Task(1, 10, 15, 25),
              Task(2, 5, 0, 30),
              Task(3, 15, 0, 50),
              Task(4, 20, 80, 100),
              Task(5, 5, 40, 100),
              Task(6, 12, 60, 120),
              Task(7, 100, 70, 250),
              Task(8, 22, 10, 80),
              Task(9, 10, 30, 150)])
# queue2 = queue.__copy__()
# queue2.shuffle()
#
# child1, child2 = queue.order_two_point_crossover(queue2)
# print(child1)
# print(child2)
gen = Classical(10, queue)

print(gen)
