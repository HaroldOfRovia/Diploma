import math
import random
from datetime import datetime

from geneticAlgorithms.Classical import Classical
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
        self.not_changed = 1
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
        best = self[0].best_unit
        for i in range(0, self.island_count):
            if self[i].best_unit.compare(best) == 1:
                best = self[i].best_unit
        return best

    def one_step(self):
        """
        Один шаг для всех островов.
        :return:
        """
        self.generation_number += 1
        for i in range(0, self.island_count):
            self[i].one_step()
        if self.generation_number % self.exchange_step == 0 and self.generation_number != 0:
            self.exchange()
        local_best = self.find_best()
        if self.best_unit.compare(local_best) == 0:
            self.not_changed += 1
        else:
            self.not_changed = 0
        self.best_unit = local_best
        if self.not_changed >= 1000:
            return True
        return False

    def exchange(self):
        """
        Передает следующему острову 10% лучших хромосом
        """
        tmp_best = []
        cut = math.ceil(self.island_population * 0.1)
        for i in range(0, self.island_count):
            tmp = []
            for j in range(0, cut):
                tmp.append(self[i].generation.pop(0))
            tmp_best.append(tmp)
        for i in range(0, self.island_count):
            self[i].generation += tmp_best[i - 1]
            self[i].sort()
            self[i].update_stat()

    def solve(self):
        """
        Полностью решает генетический алгоритм.
        """
        time = datetime.now()
        solved = False
        print(self.get_cur_population())
        log = f'ISLAND_MODEL; ISLAND_COUNT: {self.island_count}; ISLAND_POPULATION: {self.island_population}; ' \
              f'EXCHANGE_CHANGE: {self.exchange_step}; RANDOM: {self.random_param}; ' \
              f'PARENT_SELECTION_TYPE: {self.parent_selection_type}; CROSSOVER_TYPE: {self.crossover_type}; ' \
              f'MUTATION: {self.mutation}; SELECTION_TYPE: {self.selection_type}\n' \
              f'QUEUE NUMBER DURATION/TASK_IN_TIME\n'
        log += f'{self.best_unit.get_queue_string()} {self.generation_number} ' \
               f'{self.best_unit.duration}/{self.best_unit.task_in_time}\n'
        while not solved:
            solved = self.one_step()
            print(self.get_cur_population())
            log += f'{self.best_unit.get_queue_string()} {self.generation_number} ' \
                   f'{self.best_unit.duration}/{self.best_unit.task_in_time}\n'
        print(datetime.now() - time)
        return [log, None]
