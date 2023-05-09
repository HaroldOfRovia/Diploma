import math
import random

from GeneticAlgorithms.Classical import Classical
from baseLogic.Unit import Unit


class IslandModel:
    """
    Островная модель генетического алгоритма.
    """

    def __init__(self, unit_count: int, island_count: int, exchange_step: int, origin: Unit,
                 random_param=False,
                 parent_selection_type=1, crossover_type=1, mutation=0.5, selection_type=1):
        """
        :param unit_count: Суммарное количество особей.
        :param island_count: Количество островов.
        :param exchange_step: Частота обмена особями.
        :param origin: Исходная задача.
        :param random_param: Если True, то следующие параметры выбираются случайно для каждого острова.
        :param parent_selection_type: Тип отбора родителей.
        1 - Панмиксия.
        2 - Инбридинг.
        3 - Аутбридинг.
        :param crossover_type: Тип скрещивания особей.
        1 - Дискретная рекомбинация.
        2 - Упорядочивающий одноточечный кроссинговер.
        3 - Упорядочивающий двухточечный кроссинговер.
        :param mutation: Шанс мутации потомка от 0 до 1
        :param selection_type: Тип отбора особей в новое поколение.
        1 - Отбор усечением.
        2 - Элитарный отбор.
        3 - Отбор вытеснением.
        """
        self.island_population = math.floor(unit_count / island_count)
        self.island_count = island_count
        self.exchange_step = exchange_step
        self.origin = origin
        self.random_param = random_param
        self.parent_selection_type = parent_selection_type
        self.crossover_type = crossover_type
        self.mutation = mutation
        self.selection_type = selection_type
        self.islands = self.init_islands()
        self.generation_number = 1
        self.best_unit = self.find_best()

    def init_islands(self) -> list[Classical]:
        islands = []
        if self.random_param:
            for i in range(0, self.island_count):
                islands.append(Classical(self.island_population, self.origin,
                                         random.randint(1, 3), random.randint(1, 3),
                                         random.random(), random.randint(1, 3)))
        else:
            for i in range(0, self.island_count):
                islands.append(Classical(self.island_population, self.origin,
                                         self.parent_selection_type, self.crossover_type,
                                         self.mutation, self.selection_type))
        return islands

    def __getitem__(self, item):
        return self.islands[item]

    def get_cur_population(self) -> str:
        """
        :return: Возвращает текущее поколение в виде строки.
        """
        string = f'Поколение {self.generation_number}:\n'
        for i in range(0, self.island_count):
            string += f'd: {self[i].best_unit.duration}, t: {self[i].best_unit.task_in_time}; \n'
        return string

    def find_best(self) -> Unit:
        """
        :return: Лучшая особь среди всех островов.
        """
        best = self[0][0]
        for i in range(0, self.island_count):
            if self[i][0].compare(best):
                best = self[i][0]
        return best

    def one_step(self):
        """
        Один шаг для всех островов.
        :return:
        """
        solved = True
        self.generation_number += 1
        for i in range(0, self.island_count):
            if not self[i].one_step():
                solved = False
        if self.generation_number % self.exchange_step == 0 and self.generation_number != 0:
            self.exchange()
        return solved

    def exchange(self):
        """
        Передает следующему острову 10% лучших хромосом
        """
        tmp_best = []
        cut = math.floor(self.island_population * 0.1)
        for i in range(0, self.island_count):
            tmp = []
            for j in range(0, cut):
                tmp.append(self[i].generation.pop(0))
            tmp_best.append(tmp)
        for i in range(1, self.island_count):
            self[i].generation += tmp_best[i - 1]
            self[i].sort()
            self[i].update_stat()
        self[0].generation += tmp_best[-1]
        self[0].sort()
        self[0].update_stat()

    def solve(self):
        """
        Полностью решает генетический алгоритм.
        """
        solved = False
        print(self.get_cur_population())
        while not solved:
            solved = self.one_step()
            print(self.get_cur_population())
