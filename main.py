import random

from geneticAlgorithms.Cellular import Cellular
from geneticAlgorithms.Classical import Classical
from geneticAlgorithms.IslandModel import IslandModel
from qualityOfLife.TaskHelper import TaskHelper
from windows.MainWindow import MainWindow


def main():
    MainWindow()
    # helper = TaskHelper()
    # helper.save_graph('./tasksFiles/logs/log(1).txt')

    # for i in range(1, 4):
    #     for j in range(1, 4):
    #         for k in range(1, 4):
    #             for p in [0.3, 0.5, 0.8]:
    #                 cl = Classical(30, helper.read_task('./tasksFiles/saves/test_100.txt'), i, j, p, k)
    #                 log = cl.solve()
    #                 text_file = open(f'./tasksFiles/logs/cl/test_100_cl_{i}_{j}_{k}_{p}.txt', "w")
    #                 text_file.write(log[0])
    #                 helper.save_graph(f'./tasksFiles/logs/cl/test_100_cl_{i}_{j}_{k}_{p}.txt',
    #                                   f'./tasksFiles/graphs/cl/graph_100_cl_{i}_{j}_{k}_{p}.png')
    #
    # for a in range(1, 4):
    #     for i in range(1, 4):
    #         for j in [0.3, 0.5, 0.8]:
    #             ce = Cellular(36, helper.read_task('./tasksFiles/saves/test_100.txt'), i, j)
    #             log = ce.solve()
    #             text_file = open(f'./tasksFiles/logs/ce/try{a}_test_100_ce_{i}_{j}.txt', "w")
    #             text_file.write(log[0])
    #             helper.save_graph(f'./tasksFiles/logs/ce/try{a}_test_100_ce_{i}_{j}.txt',
    #                               f'./tasksFiles/graphs/ce/try{a}_graph_100_ce_{i}_{j}.png')
    #
    # for a in range(1, 10):
    #     island = IslandModel(32, 4, 5, helper.read_task('./tasksFiles/saves/test_100.txt'), True)
    #     log = island.solve()
    #     text_file = open(f'./tasksFiles/logs/is/try{a}_test_100_is.txt', "w")
    #     text_file.write(log[0])
    #     helper.save_graph(f'./tasksFiles/logs/is/try{a}_test_100_is.txt',
    #                       f'./tasksFiles/graphs/is/try{a}_graph_100_is.png')

if __name__ == '__main__':
    main()
