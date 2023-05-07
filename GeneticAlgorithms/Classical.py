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
        self.count = count
        self.generation = self.init_generation()

    def init_generation(self):
        """
        :return: Первое случайное поколение
        """
        arr = []
        for i in range(0, self.count):
            arr.append(self.origin.shuffle())
        return arr

    def __str__(self):
        string = ''
        for i in range(0, self.count):
            string += f'{self.generation[i]}\n'
        return string
