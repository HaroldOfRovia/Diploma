import random

from baseLogic.Unit import Unit


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
        self.generation = self.init_generation()

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
        return random.randint(0, self.len)

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
        Устанавливает новое поколение
        :param instances: Набор особей состоящий из родителей и потомков.
        """
        self.generation = self.truncation_selection_with_count(instances, self.len)

    def elite_selection(self, instances):
        """
        Элитарный набор. 10% - лучшие особи, остальные 90% - случайные новые особи.
        Устанавливает новое поколение
        :param instances: Набор особей состоящий из родителей и потомков.
        :return: Новое поколение.
        """
        cut = round(0.1 * self.len)
        new_generation = self.truncation_selection_with_count(instances, cut)
        for i in range(cut, self.len):
            new_generation.append(self.origin.shuffle())
        self.generation = new_generation
