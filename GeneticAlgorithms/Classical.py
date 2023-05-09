import random

from baseLogic.Unit import Unit


def sort(instances: list[Unit]) -> list[Unit]:
    """
    Сортирует последовательность особей сначала по вовремя выполненным задачам, затем по времени выполнения.
    :param instances: Массив особей.
    :return: Отсортированный массив.
    """
    arr = []
    while 0 < len(instances):
        best = instances[0]
        index = 0
        for j in range(0, len(instances)):
            if instances[j].compare(best) == 1:
                best = instances[j]
                index = j
        instances.pop(index)
        arr.append(best)
    return arr


class Classical:
    """
    Описывает классический генетический алгоритм.
    """

    def __init__(self, count: int, origin: Unit,
                 parent_selection_type=1, crossover_type=2, mutation=0.5, selection_type=1):
        """
        :param count: Количество особей в поколении
        :param origin: Исходное расписание
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
        self.origin = origin
        self.len = count
        self.parent_selection_type = parent_selection_type
        self.crossover_type = crossover_type
        self.mutation = mutation
        self.selection_type = selection_type
        """
        Текущее поколение.
        """
        self.generation = self.init_generation()
        self.generation = sort(self.generation)
        """
        Номер поколения.
        """
        self.generation_number = 1
        self.not_changed = 0
        self.best_unit = self[0]

    def init_generation(self) -> list[Unit]:
        """
        :return: Первое случайное поколение
        """
        arr = []
        for i in range(0, self.len):
            arr.append(self.origin.shuffle())
        return arr

    def __str__(self) -> str:
        string = ''
        for i in range(0, self.len):
            string += f'{self[i]}\n'
        return string

    def __getitem__(self, item: int):
        return self.generation[item]

    def update_stat(self):
        if self.best_unit.compare(self[0]) != 0:
            self.best_unit = self[0]
            self.not_changed = 0

    def sort(self):
        """
        Сортирует текущее поколение.
        """
        self.generation = sort(self.generation)

    def panmixia(self) -> int:
        """
        Панмикися.
        :return: Случайно выбранный номер второго родителя.
        """
        return random.randint(0, self.len - 1)

    def inbreeding(self, curr_index: int) -> Unit:
        """
        Инбридинг.
        :param curr_index:
        :return: Возвращает особь для скрещивания с самым маленьким Хемминговым расстоянием.
        Самая близкая особь.
        """
        distance = self.len + 1
        unit = Unit([])
        for i in range(0, self.len):
            if i == curr_index:
                continue
            tmp = self[curr_index].hamming_distance(self[i])
            if tmp < distance:
                unit = self[i]
                distance = tmp
            if distance == 0:
                break
        return unit

    def outcrossing(self, curr_index: int) -> Unit:
        """
        Аутбридинг.
        :param curr_index:
        :return: Возвращает особь для скрещивания с самым большим Хемминговым расстоянием.
        Самая дальня особь.
        """
        distance = -1
        unit = Unit([])
        for i in range(0, self.len):
            if i == curr_index:
                continue
            tmp = self[curr_index].hamming_distance(self[i])
            if tmp > distance:
                unit = self[i]
                distance = tmp
            if distance == 0:
                break
        return unit

    def truncation_selection(self, instances: list[Unit]):
        """
        Отбор усечением. Сортирует набор особей (родители и потомки) по пригодности.
        Устанавливает новое поколение
        :param instances: Набор особей состоящий из родителей и потомков.я.
        """
        self.generation = sort(instances)[:self.len]

    def elite_selection(self, instances: list[Unit]):
        """
        Элитарный отбор. 10% - лучшие особи, остальные 90% - случайные новые особи.
        Устанавливает новое поколение
        :param instances: Набор особей состоящий из родителей и потомков.
        :return: Новое поколение.
        """
        cut = round(0.1 * self.len)
        new_generation = sort(instances)[:cut]
        for i in range(cut, self.len):
            new_generation.append(self.origin.shuffle())
        self.generation = sort(new_generation)

    def exclusion_selection(self, instances: list[Unit]):
        """
        Отбор вытеснением. Сначала выбираются уникальные особи в порядке пригодности, затем оставшиеся лучшие.
        Устанавливает новое поколение.
        """
        instances = sort(instances)
        new_generation = [instances.pop(0)]
        for distance in range(instances[0].len, 0, -1):  # Перебор всех расстояний, от максимального, до минимума.
            i = 0
            while i < len(instances):
                good = True
                for j in range(0, len(new_generation)):
                    if instances[i].hamming_distance(new_generation[j]) < distance:
                        good = False
                        break
                if good:
                    new_generation.append(instances.pop(i))
                    i -= 1
                    if len(new_generation) == self.len:
                        break
                i += 1
            if len(new_generation) >= self.len:
                break
        if len(new_generation) != self.len:
            new_generation += instances[:self.len - len(new_generation)]
        self.generation = new_generation[:self.len]

    def solved(self, count=100) -> bool:
        """
        Проверяет, решен ли алгоритм.
        :param count: Количество поколений. Если за данное количество не будет найдена более хорошая особь,
        то алгоритм завершен.
        :return: True, если решение завершено.
        """
        new_best = self[0]
        if new_best.compare(self.best_unit) == 0:
            self.not_changed += 1
            if self.not_changed >= count:
                return True
        else:
            self.not_changed = 0
            self.best_unit = new_best
            return False

    def one_step(self) -> bool:
        """
        Один шаг генетического алгоритма.
        :return: True, если алгоритм завершил работу.
        """
        new_generation = [] + self.generation
        for i in range(0, self.len):
            if self.parent_selection_type == 1:
                second_p_num = self.panmixia()
                if second_p_num == i:
                    continue
                second_p = self[second_p_num]
            elif self.parent_selection_type == 2:
                second_p = self.inbreeding(i)
            else:
                second_p = self.outcrossing(i)

            if self.crossover_type == 1:
                children = self[i].discrete_recombination(second_p)
            elif self.crossover_type == 2:
                children = self[i].order_single_point_crossover(second_p)
            else:
                children = self[i].order_two_point_crossover(second_p)

            for j in range(0, len(children)):
                children[j].mutation(self.mutation)
            new_generation += children

        if self.selection_type == 1:
            self.truncation_selection(new_generation)
        elif self.selection_type == 2:
            self.elite_selection(new_generation)
        else:
            self.exclusion_selection(new_generation)

        self.generation_number += 1

        if self.solved(1000):
            return True
        return False

    def solve(self):
        """
        Полностью решает генетический алгоритм.
        """
        solved = False
        print(f'Поколение {self.generation_number}: {self.best_unit}')
        while not solved:
            solved = self.one_step()
            print(f'Поколение {self.generation_number}: {self.best_unit}')
