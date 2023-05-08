from __future__ import annotations

import random

from baseLogic.Task import Task


class Unit:
    """
    Класс описывающий 1 вариант решения.
    """

    def __init__(self, queue):
        """
        :param queue: очередь решения задач
        :param duration: время выполнения всех задач
        :param task_in_time: количество задач уложившихся в директивный срок
        """
        self.queue = queue
        self.len = len(queue)
        self.duration = 0
        self.task_in_time = 0
        self.set_statistics()

    def __str__(self) -> str:
        arr = []
        for task in self.queue:
            arr.append(f'{task}')
        return f'{arr}, duration: {self.duration}, task in time: {self.task_in_time}'

    def clone(self) -> Unit:
        """
        Отличается от __copy__() тем, что не производит глубокого копирования. Сохраняет ссылки оригинальных задач.
        :return: Поверхностную копию объекта.
        """
        clone = []
        for task in self.queue:
            clone.append(task)
        return Unit(clone)

    def __contains__(self, task: Task) -> bool:
        for item in self.queue:
            if task.__eq__(item):
                return True
        return False

    def __getitem__(self, item: int):
        return self.queue[item]

    def __setitem__(self, key: int, value: Task) -> None:
        self.queue[key] = value

    def shuffle(self) -> Unit:
        """
        :return: Новую особь с перемешанной очередью задач и обновленной статистикой.
        """
        clone = self.clone()
        random.shuffle(clone.queue)
        clone.set_statistics()
        return clone

    def append(self, task) -> None:
        """
        Добавляет задачу в очередь. НЕ ПЕРЕСЧИТЫВАЕТ СТАТИСТИКУ!!!
        :param task: Задача
        """
        self.queue.append(task)
        self.len += 1

    def set_statistics(self) -> None:
        """
        Устанавливает актуальное время выполнения задачи и количество задач уложившихся в директивный срок.
        """
        self.duration = 0
        self.task_in_time = 0
        for i in range(0, self.len):
            if self[i].start > self.duration:
                self.duration += self[i].start - self.duration
            self.duration += self[i].length
            if self.duration <= self[i].end:
                self.task_in_time += 1

    def choose_gen(self, num: int, parent1: Unit, parent2: Unit) -> None:
        """
        Добавляет в очередь задачу (ген) одного из родителя или -1,
        если обе задачи (гена) уже присутствуют в генах ребенка
        :param num: номер гена
        :param parent1: родитель 1
        :param parent2: родитель 2
        """
        if random.randint(0, 1) == 0:
            if not self.__contains__(parent1[num]):
                self.append(parent1[num])
            elif not self.__contains__(parent2[num]):
                self.append(parent2[num])
            else:
                self.append(-1)
        else:
            if not self.__contains__(parent2[num]):
                self.append(parent2[num])
            elif not self.__contains__(parent1[num]):
                self.append(parent1[num])
            else:
                self.append(-1)

    def set_free_task(self, num: int, pos: int, parent: Unit) -> int:
        """
        Вставляет первую задачу из родительской особи, что не содержится в дочерней очереди в выбранной позиции.
        :param num: Место замены.
        :param pos: Позиция с которой начинается поиск в родительской особи.
        :param parent: Родительская особь.
        """
        for i in range(pos, parent.len):
            if not self.__contains__(parent[i]):
                self[num] = parent[i]
                return i

    def discrete_recombination(self, second_p: Unit) -> list[Unit]:
        """
        Модифицированная дискретная рекомбинация.
        Скрещивает текущую особь с особью переданной в параметры.
        1. Случайно выбирается родитель из которого будет браться i ген.
        2. Если у потомка уже имеется ген от первого родителя, то берется ген второго родителя.
        3. Если у потомка в наличии оба гена, то временно ставится -1 и скрещивание идет дальше.
        4. Повторным прохождением по потомкам, заменяем -1 на недостающие гены соответствующего родителя.
            Т.е. для первого потомка берутся гены из первого родителя, второго из второго. В том же порядке,
            что и в родителях.
        :param second_p: Вторая особь.
        :return: Два потомка.
        """
        child1, child2 = Unit([]), Unit([])
        for i in range(0, self.len):
            child1.choose_gen(i, self, second_p)
            child2.choose_gen(i, self, second_p)

        for i in range(0, self.len):
            if child1[i] == -1:
                child1.set_free_task(i, 0, self)
            if child2[i] == -1:
                child2.set_free_task(i, 0, second_p)

        child1.set_statistics()
        child2.set_statistics()
        return [child1, child2]

    def order_single_point_crossover_with_cut(self, second_p: Unit, cut: int) -> list[Unit]:
        """
        Упорядочивающий одноточечный кроссинговер.
        Скрещивает текущую особь с особью переданной в параметры.
        1. Выбирается случайное место разреза (0 < n < len(parent)).
        2. Первая половина новой особи - начало одного из родителя.
        3. Вторая половина новой особи - недостающие задачи идущие в том же порядке, что и у другого родителя.
        :param second_p: Вторая особь.
        :param cut: После данной особи будет сделан разрез.
        :return: Два потомка.
        """
        child1, child2 = Unit([]), Unit([])
        for i in range(0, cut):
            child1.append(self[i])
            child2.append(second_p[i])

        for j in range(0, second_p.len):
            if not child1.__contains__(second_p[j]):
                child1.append(second_p[j])

        for j in range(0, self.len):
            if not child2.__contains__(self[j]):
                child2.append(self[j])

        child1.set_statistics()
        child2.set_statistics()
        return [child1, child2]

    def order_single_point_crossover(self, second_p: Unit) -> list[Unit]:
        """
        Упорядочивающий одноточечный кроссинговер. Место разреза задается случайно.
        Скрещивает текущую особь с особью переданной в параметры.
        :param second_p: Вторая особь.
        :return: Два потомка.
        """
        return self.order_single_point_crossover_with_cut(second_p, random.randint(1, self.len - 1))

    def order_two_point_crossover(self, second_p: Unit) -> list[Unit]:
        """
        Упорядочивающий двухточечный кроссинговер. Место разреза задается случайно.
        Скрещивает текущую особь с особью переданной в параметры.
        1. Выбираются 2 случайных места разреза (0 < n < k < len(parent)).
        2. Первая половина новой особи - начало одного из родителя.
        3. Вторая половина новой особи - недостающие задачи идущие в том же порядке, что и у другого родителя.
        4. Третья половина новой особи - недостающие задачи идущие в том же порядке, что и у первого родителя.
        :param second_p: Вторая особь.
        :return: Два потомка.
        """
        cut1 = random.randint(1, self.len - 2)
        cut2 = random.randint(cut1 + 1, self.len - 1)
        child1, child2 = Unit(self[:cut1]), Unit(second_p[:cut1])
        pos1, pos2 = 0, 0
        for i in range(cut1, cut2):
            child1.append(-1)
            child2.append(-1)
            pos1 = child1.set_free_task(i, pos1, second_p)
            pos2 = child2.set_free_task(i, pos2, self)
        pos1, pos2 = 0, 0
        for i in range(cut2, self.len):
            child1.append(-1)
            child2.append(-1)
            pos1 = child1.set_free_task(i, pos1, self)
            pos2 = child2.set_free_task(i, pos2, second_p)
        child1.set_statistics()
        child2.set_statistics()
        return [child1, child2]

    def mutation(self, probability: float) -> bool:
        """
        Мутация текущей особи. С вероятностью меняет 2 гена местами.
        :param probability: Шанс мутации, чем выше значение, тем выше шанс (0 <= n <= 1).
        :return: Произошла ли мутация или нет.
        """
        if random.random() > probability:
            return False
        else:
            gen = random.randint(0, self.len - 1)  # Ген для перемещения
            pos = random.randint(0, self.len - 1)  # Место второго гена для обмена
            while pos == gen:
                pos = random.randint(0, self.len - 1)
            tmp = self[pos]
            self[pos] = self[gen]
            self[gen] = tmp
            self.set_statistics()
            return True

    def compare(self, other: Unit) -> int:
        """
        Сравнивает 2 особи сначала по количеству задач уложившихся в директивный срок (чем больше, тем лучше).
        Если количество задач равно, то сравнивает по времени выполнения (чем меньше, тем лучше).
        :param other: Вторая особь с которой будет происходить сравнение.
        :return: Возвращает 1, если лучше, чем вторая. 0, если одинаковые. -1, если хуже.
        """
        if self.task_in_time > other.task_in_time:
            return 1
        elif self.task_in_time == other.task_in_time:
            if self.duration < other.duration:
                return 1
            elif self.duration == other.duration:
                return 0
        else:
            return -1

    def hamming_distance(self, other: Unit) -> int:
        """
        Реализует Хеммингово расстояние.
        :param other: Вторая особь.
        :return: Значение Хеммингово расстояния.
        """
        distance = 0
        for i in range(0, self.len):
            if self[i].id != other[i].id:
                distance += 1
        return distance
