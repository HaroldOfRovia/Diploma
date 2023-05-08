import random

from baseLogic.Unit import Unit


def sort(instances):
    arr = []
    for i in range(0, len(instances)):
        best = instances[0]
        for j in range(0, len(instances)):
            if instances[j].compare(best) == 1:
                best = instances[j]
        arr.append(best)
    return arr


class Classical:
    """
    Описывает классический генетический алгоритм.
    """

    def __init__(self, count, origin: Unit):
        """
        :param count: Количество особей в поколении
        :param origin: Исходное расписание
        """
        self.origin = origin
        self.len = count
        """
        Текущее поколение.
        """
        self.generation = self.init_generation()
        """
        Номер поколения.
        """
        self.generation_number = 0
        self.not_changed = 0
        self.best_unit = self.best_count()

    def init_generation(self):
        """
        :return: Первое случайное поколение
        """
        arr = []
        for i in range(0, self.len):
            arr.append(self.origin.shuffle())
        return arr

    def __str__(self):
        string = ''
        for i in range(0, self.len):
            string += f'{self[i]}\n'
        return string

    def __getitem__(self, item):
        return self.generation[item]

    def panmixia(self):
        """
        Панмикися.
        :return: Случайно выбранный номер второго родителя.
        """
        return self[random.randint(0, self.len - 1)]

    def inbreeding(self, curr_index):
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

    def outcrossing(self, curr_index):
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

    @staticmethod
    def truncation_selection_with_count(instances, count):
        """
        Отбор усечением. Сортирует набор особей (родители и потомки) по пригодности.
        :param instances: Набор особей состоящий из родителей и потомков.
        :param count: Размер возвращаемого поколения.
        :return: Новое поколение лучших особей.
        """
        new_generation = []
        while len(new_generation) < count:
            tmp = []
            best = instances[0]
            for item in instances:
                result = best.compare(item)
                if result == 1:
                    continue
                elif result == 0:
                    tmp.append(item)
                else:
                    best = item
                    tmp.clear()
                    tmp.append(best)
            new_generation += tmp[:count - len(new_generation)]
            i = 0
            while i < len(instances):
                if best.compare(instances[i]) == 0:
                    instances.pop(i)
                    i -= 1
                i += 1
        return new_generation

    def truncation_selection(self, instances):
        """
        Отбор усечением.
        Устанавливает новое поколение
        :param instances: Набор особей состоящий из родителей и потомков.
        """
        self.generation = self.truncation_selection_with_count(instances, self.len)

    def elite_selection(self, instances):
        """
        Элитарный отбор. 10% - лучшие особи, остальные 90% - случайные новые особи.
        Устанавливает новое поколение
        :param instances: Набор особей состоящий из родителей и потомков.
        :return: Новое поколение.
        """
        cut = round(0.1 * self.len)
        new_generation = self.truncation_selection_with_count(instances, cut)
        for i in range(cut, self.len):
            new_generation.append(self.origin.shuffle())
        self.generation = new_generation

    def exclusion_selection(self, instances):
        """
        Отбор вытеснением. Сначала выбираются уникальные особи, затем лучшие.
        Устанавливает новое поколение.
        """
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
            if len(new_generation) == self.len:
                break
        if len(new_generation) != self.len:
            new_generation += self.truncation_selection_with_count(instances, self.len - len(new_generation))
        self.generation = new_generation

    def best_count(self):
        """
        :return: Лучшая особь в поколении
        """
        best = self[0]
        for i in range(1, self.len):
            if self[i].compare(best):
                best = self[i]
        return best

    def solved(self, count=100):
        """
        Проверяет, решен ли алгоритм.
        :param count: Количество поколений. Если за данное количество не будет найдена более хорошая особь,
        то алгоритм завершен.
        :return: True, если решение завершено.
        """
        new_best = self.best_count()
        if new_best.compare(self.best_unit) == 0:
            self.not_changed += 1
            if self.not_changed == count:
                return True
        else:
            self.not_changed = 0
            self.best_unit = new_best
            return False

    def one_step(self, parent_selection_type, crossover_type, mutation, selection_type):
        """
        Один шаг генетического алгоритма.
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
        :return: True, если алгоритм завершил работу.
        """
        new_generation = [] + self.generation
        for i in range(0, self.len):
            if parent_selection_type == 1:
                second_p = self.panmixia()
            elif parent_selection_type == 2:
                second_p = self.inbreeding(i)
            else:
                second_p = self.outcrossing(i)

            if crossover_type == 1:
                children = self[i].discrete_recombination(second_p)
            elif crossover_type == 2:
                children = self[i].order_single_point_crossover(second_p)
            else:
                children = self[i].order_two_point_crossover(second_p)

            children[0].mutation(mutation)
            children[1].mutation(mutation)
            new_generation += children

        if selection_type == 1:
            self.truncation_selection(new_generation)
        elif selection_type == 2:
            self.elite_selection(new_generation)
        else:
            self.exclusion_selection(new_generation)

        self.generation_number += 1

        if self.solved(1000):
            return True
        print(f'{self.generation_number} {self.best_unit}')
        return False
