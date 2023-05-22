from __future__ import annotations


class Task:
    """
    Класс описывающий 1 задачу
    """

    def __init__(self, num: int, length: int, start: int, end: int):
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

    def __str__(self) -> str:
        return f'{self.id}'

    def __copy__(self) -> Task:
        return Task(self.id, self.length, self.start, self.end)

    def __eq__(self, other: Task) -> bool:
        if not isinstance(other, Task):
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

    def get_full_data_str(self):
        return f'{self.id} {self.start} {self.length} {self.end}\n'
