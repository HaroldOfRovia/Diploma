import os
import random
import sys
from os import path

from baseLogic.Task import Task
from baseLogic.Unit import Unit


class TaskHelper:
    """
    Генерирует случайные задачи
    Чтение задач из файлов
    Сохранение задач в файл
    """

    def __init__(self):
        """
        Последняя сгенерированная задача.
        """
        if not path.exists('./tasksFiles'):
            os.mkdir('tasksFiles')
        if not path.exists('./tasksFiles/saves'):
            os.mkdir('./tasksFiles/saves')
        if not path.exists('./tasksFiles/logs'):
            os.mkdir('./tasksFiles/logs')
        self.last_generate_unit = None
        self.last_read_unit = None

    def generate_unit(self, count: int, start_period: int, max_duration: int, max_overtime: int):
        """
        Генерирует случайное расписание случайных задач
        :param count: количество задач
        :param start_period: диапазон начала задач
        :param max_duration: максимальное время исполнения
        :param max_overtime: максимальное дополнительное время для выполнения задачи
        :return:
        """
        arr = []
        for i in range(0, count):
            start = random.randint(0, start_period)
            duration = random.randint(0, max_duration)
            arr.append(Task(i, duration, start, random.randint(start + duration, start + duration + max_overtime)))
        self.last_generate_unit = Unit(arr)
        return self.last_generate_unit

    @staticmethod
    def save_unit(unit: Unit):
        """
        Сохраняет текущий юнит в файл.
        """
        num = ''
        for i in range(0, sys.maxsize):
            if i == 0:
                if not path.exists(f'./tasksFiles/saves/task.txt'):
                    break
            elif not path.exists(f'./tasksFiles/saves/task({i}).txt'):
                num += f'({i})'
                break
        text_file = open(f'./tasksFiles/saves/task{num}.txt', "w")
        text_file.write('ID START LENGTH END\n')
        for i in range(0, unit.len):
            text_file.write(unit[i].get_full_data_str())

    def read_task(self, url: str) -> Unit:
        """
        Считывает задачу из файла
        :param url:
        :return: Задачу в формате юнита.
        """
        unit = Unit([])
        text_file = open(url, "r")
        lines = text_file.readlines()
        for i in range(1, len(lines)):
            string = lines[i]
            string = string.split(" ")
            unit.append(Task(int(string[0]), int(string[2]), int(string[1]), int(string[3])))
        unit.set_statistics()
        self.last_read_unit = unit
        return unit

    @staticmethod
    def save_log(log: str):
        """
        Сохраняет логи решения. Записывает номер поколения и лучшую особь текущего поколения.
        """
        num = ''
        for i in range(0, sys.maxsize):
            if i == 0:
                if not path.exists(f'./tasksFiles/logs/log.txt'):
                    break
            elif not path.exists(f'./tasksFiles/logs/log({i}).txt'):
                num += f'({i})'
                break
        text_file = open(f'./tasksFiles/logs/log{num}.txt', "w")
        text_file.write(log)
