class Task:
    """
    Класс описывающий 1 задачу
    """

    def __init__(self, num, length, start, end):
        """
        :param num: порядковый номер задачи в оригинальном условии
        :param length: длительность выполнения
        :param start: начало поступления задачи
        :param end: директивный срок
        """
        self.id = num
        self.length = length
        self.start = start
        self.end = end

    def __str__(self):
        return f'{self.id}'

    def __copy__(self):
        return Task(self.id, self.length, self.start, self.end)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.id != other.id:
            return False
        if self.end != other.end:
            return False
        if self.start != other.start:
            return False
        if self.length != other.length:
            return False
        return True
