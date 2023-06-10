import math
from datetime import datetime

from baseLogic.Unit import Unit


class Cellular:
    """
    Ячеистый генетический алгоритм.
    """

    def __init__(self, count: int, origin: Unit,
                 crossover_type=2, mutation=0.5):
        """
        :param count: Количество особей в поколении
        :param origin: Исходное расписание
        :param crossover_type: Тип скрещивания особей.
        1 - Дискретная рекомбинация.
        2 - Упорядочивающий одноточечный кроссинговер.
        3 - Упорядочивающий двухточечный кроссинговер.
        :param mutation: Шанс мутации потомка от 0 до 1
        """
        self.origin = origin
        self.crossover_type = crossover_type
        self.mutation = mutation
        """
        Размер квадратной площади.
        """
        self.size = round(math.sqrt(count))
        self.best_unit = None
        self.field = self.init_field()
        self.generation_number = 1
        self.not_changed = 0
        self.select_best_partner(0, 0)

    def __getitem__(self, item):
        return self.field[item]

    def init_field(self):
        """
        Инициализирует поле случайными особями и инициализирует лучшую особь.
        :return: Поле, которое заполнено особями генетического алгоритма.
        """
        field = []
        for i in range(0, self.size):
            field.append([])
            for j in range(0, self.size):
                unit = self.origin.shuffle()
                field[i].append(unit)
                if i == 0 and j == 0:
                    self.best_unit = unit
                elif unit.compare(self.best_unit) == 1:
                    self.best_unit = unit
        return field

    def select_best_partner(self, i, j):
        """
        :param i: Положение особи для которой производится поиск пары на оси OX.
        :param j: Положение особи для которой производится поиск пары на оси OY.
        :return: Возвращает лучшего партнера для текущей особи.
        """
        best = self[i][j - 1]
        if self[i - 1][j].compare(best) == 1:
            best = self[i - 1][j]
        if self[i][(j + 1) % self.size].compare(best) == 1:
            best = self[i][(j + 1) % self.size]
        if self[(i + 1) % self.size][j].compare(best) == 1:
            best = self[(i + 1) % self.size][j]
        return best

    def one_step(self):
        """
        (Выбирается лучший из детей)
        :return:
        """
        self.generation_number += 1
        tmp_field = []
        for i in range(0, self.size):
            tmp_field.append([])
            for j in range(0, self.size):
                partner = self.select_best_partner(i, j)
                children = []
                if self.crossover_type == 1:
                    children += self[i][j].discrete_recombination(partner)
                elif self.crossover_type == 2:
                    children += self[i][j].order_single_point_crossover(partner)
                else:
                    children += self[i][j].order_two_point_crossover(partner)
                for k in range(0, len(children)):
                    children[k].mutation(self.mutation)
                best_c = children[0]
                children.append(self[i][j])
                for k in range(1, 3):
                    if children[k].compare(best_c) == 1:
                        best_c = children[k]
                if best_c.compare(self.best_unit) == 1:
                    self.best_unit = best_c
                    self.not_changed = 0
                tmp_field[i].append(best_c)
        self.field = tmp_field
        self.not_changed += 1
        if self.not_changed > 1000:
            return True
        return False

    def solve(self):
        """
        Полностью решает генетический алгоритм.
        """
        time = datetime.now()
        solved = False
        print(f'Поколение {self.generation_number}: {self.best_unit}')
        special_log = ''
        standard_log = f'CELLULAR; UNIT_COUNT: {self.size * self.size}; CROSSOVER_TYPE: {self.crossover_type}; ' \
              f'MUTATION: {self.mutation}\n' \
              f'QUEUE NUMBER DURATION/TASK_IN_TIME\n'
        standard_log += f'{self.best_unit.get_queue_string()} {self.generation_number} ' \
               f'{self.best_unit.duration}/{self.best_unit.task_in_time}\n'
        while not solved:
            solved = self.one_step()
            print(f'Поколение {self.generation_number}: {self.best_unit}')
            standard_log += f'{self.best_unit.get_queue_string()} {self.generation_number} ' \
                   f'{self.best_unit.duration}/{self.best_unit.task_in_time}\n'
            for i in range(0, self.size):
                for j in range(0, self.size):
                    special_log += f'{self[i][j].task_in_time}'
                    if i != self.size - 1 or j != self.size - 1:
                        special_log += ' '
            special_log += '\n'

        print(datetime.now() - time)
        return [standard_log, special_log]

