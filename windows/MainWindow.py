from tkinter import *
from tkinter import filedialog

from geneticAlgorithms.Cellular import Cellular
from geneticAlgorithms.Classical import Classical
from geneticAlgorithms.IslandModel import IslandModel
from qualityOfLife.TaskHelper import TaskHelper


class MainWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title("Генетические алгоритмы")
        self.window.geometry("800x600")
        self.window.resizable(0, 0)

        choose_task_frame = Frame()
        choose_task = Button(choose_task_frame, text="Выбрать задачу", command=self.get_task)
        choose_task.pack(side=LEFT)
        self.task = None
        self.selected_task = Label(choose_task_frame)
        self.selected_task.pack(side=RIGHT)
        choose_task_frame.grid(column=0, row=0, pady=[10, 5], padx=[10, 5], sticky="w")

        self.selected_type = Label(text="Классический", font='Helvetica 20 bold')
        self.selected_type.grid(column=1, row=2, pady=5, padx=[10, 5], sticky="w")

        type_frame = Frame()
        type_frame.grid(column=0, row=2, pady=5, padx=[10, 5], sticky="w")
        header = Label(type_frame, text='Выберите тип генетического алгоритма:')
        header.pack(side=TOP)
        classical_btn = Button(type_frame, text="Классический", command=self.set_classical)
        classical_btn.pack(side=LEFT)
        island_btn = Button(type_frame, text="Островной", command=self.set_island)
        island_btn.pack(side=LEFT)
        cellular_btn = Button(type_frame, text="Ячеистый", command=self.set_cellular)
        cellular_btn.pack(side=LEFT)
        self.gen_type = 1  # 1 - классический, 2 - островной, 3 - ячеистый

        count_frame = Frame()
        count_frame.grid(column=0, row=3, pady=5, padx=[10, 5], sticky="w")
        count_header = Label(count_frame, text='Количество особей в поколении:')
        count_header.pack(side=TOP, anchor=W)
        self.count = Entry(count_frame)
        self.count.pack(side=LEFT, anchor=W)

        self.parent_selection_frame = Frame()
        self.parent_selection_frame.grid(column=0, row=4, pady=15, padx=[10, 5], sticky="w")
        parent_selection_header = Label(self.parent_selection_frame, text='Тип выбора родителей:')
        parent_selection_header.pack(side=TOP, anchor=W)
        self.parent_selection = IntVar()
        self.parent_selection.set(1)
        panmixia = Radiobutton(self.parent_selection_frame, text='Панмиксия', variable=self.parent_selection, value=1)
        inbreeding = Radiobutton(self.parent_selection_frame, text='Инбридинг', variable=self.parent_selection, value=2)
        outcrossing = Radiobutton(self.parent_selection_frame, text='Аутбридинг', variable=self.parent_selection,
                                  value=3)
        panmixia.pack(side=TOP, anchor=W)
        inbreeding.pack(side=TOP, anchor=W)
        outcrossing.pack(side=TOP, anchor=W)

        self.crossover_frame = Frame()
        self.crossover_frame.grid(column=0, row=5, pady=15, padx=[10, 5], sticky="w")
        crossover_header = Label(self.crossover_frame, text='Тип скрещивания:')
        crossover_header.pack(side=TOP, anchor=W)
        self.crossover = IntVar()
        self.crossover.set(1)
        discrete_recombination = Radiobutton(self.crossover_frame, text='Дискретная рекомбинация',
                                             variable=self.crossover, value=1)
        order_single_point_crossover = Radiobutton(self.crossover_frame,
                                                   text='Упорядочивающий одноточечный кроссинговер',
                                                   variable=self.crossover, value=2)
        order_two_point_crossover = Radiobutton(self.crossover_frame, text='Упорядочивающий двухточечный кроссинговер',
                                                variable=self.crossover, value=3)
        discrete_recombination.pack(side=TOP, anchor=W)
        order_single_point_crossover.pack(side=TOP, anchor=W)
        order_two_point_crossover.pack(side=TOP, anchor=W)

        self.mutation_frame = Frame()
        self.mutation_frame.grid(column=1, row=3, pady=5, padx=[10, 5], sticky="w")
        mutation_header = Label(self.mutation_frame, text='Шанс мутации:')
        mutation_header.pack(side=TOP, anchor=W)
        self.mutation = Entry(self.mutation_frame)
        self.mutation.pack(side=LEFT)

        self.selection_frame = Frame()
        self.selection_frame.grid(column=1, row=4, pady=15, padx=[10, 5], sticky="w")
        selection_header = Label(self.selection_frame, text='Тип отбора:')
        selection_header.pack(side=TOP, anchor=W)
        self.selection = IntVar()
        self.selection.set(1)
        truncation_selection = Radiobutton(self.selection_frame, text='Отбор усечением', variable=self.selection,
                                           value=1)
        elite_selection = Radiobutton(self.selection_frame, text='Элитарный отбор', variable=self.selection, value=2)
        exclusion_selection = Radiobutton(self.selection_frame, text='Отбор вытеснением', variable=self.selection,
                                          value=3)
        truncation_selection.pack(side=TOP, anchor=W)
        elite_selection.pack(side=TOP, anchor=W)
        exclusion_selection.pack(side=TOP, anchor=W)

        self.island_frame = Frame()
        island_count_header = Label(self.island_frame, text='Количество островов:')
        island_count_header.pack(side=TOP, anchor=W)
        self.island = Entry(self.island_frame)
        self.island.pack(side=LEFT, anchor=W)

        self.exchange_frame = Frame()
        exchange_header = Label(self.exchange_frame, text='Частота обмена:')
        exchange_header.pack(side=TOP, anchor=W)
        self.exchange = Entry(self.exchange_frame)
        self.exchange.pack(side=TOP, anchor=W)

        self.random_frame = Frame()
        random_header = Label(self.random_frame, text='Случайные параметры:')
        random_header.pack(side=TOP, anchor=W)
        self.random = BooleanVar()
        self.random.set(True)
        true = Radiobutton(self.random_frame, text='Да', variable=self.random, value=True)
        false = Radiobutton(self.random_frame, text='Нет', variable=self.random, value=False)
        true.pack(side=TOP, anchor=W)
        false.pack(side=TOP, anchor=W)

        start_btn = Button(self.window, text="Решить", command=self.start, font='Helvetica 20 bold')
        start_btn.grid(column=3, row=2, pady=15, padx=[10, 5], sticky="nw")

        self.err = Label(fg="red")
        self.err.grid(column=0, row=6, pady=5, padx=[10, 5], sticky="w")

        self.window.mainloop()

    def get_task(self):
        try:
            file = filedialog.askopenfilename(filetypes=[("задача", ".txt")])
            helper = TaskHelper()
            self.task = helper.read_task(file)
            self.selected_task['text'] = f'Файл задачи: {file.split("/")[-1]}'
        except:
            self.err['text'] = f'Проблема с файлом'

    def set_classical(self):
        self.selected_type['text'] = f'Классический'
        self.gen_type = 1
        self.parent_selection_frame.grid(column=0, row=4, pady=15, padx=[10, 5], sticky="w")
        self.selection_frame.grid(column=1, row=4, pady=15, padx=[10, 5], sticky="w")
        self.island_frame.grid_forget()
        self.exchange_frame.grid_forget()
        self.random_frame.grid_forget()

    def set_island(self):
        self.selected_type['text'] = f'Островной'
        self.gen_type = 2
        self.parent_selection_frame.grid(column=0, row=4, pady=15, padx=[10, 5], sticky="w")
        self.selection_frame.grid(column=1, row=4, pady=15, padx=[10, 5], sticky="w")
        self.island_frame.grid(column=2, row=3, pady=5, padx=[10, 5], sticky="w")
        self.exchange_frame.grid(column=3, row=3, pady=5, padx=[10, 5], sticky="nw")
        self.random_frame.grid(column=2, row=4, pady=5, padx=[10, 5], sticky="nw")

    def set_cellular(self):
        self.selected_type['text'] = f'Ячеистый'
        self.gen_type = 3
        self.parent_selection_frame.grid_forget()
        self.selection_frame.grid_forget()
        self.island_frame.grid_forget()
        self.exchange_frame.grid_forget()
        self.random_frame.grid_forget()

    def start(self):
        try:
            if self.task == None:
                raise TypeError
        except:
            self.err['text'] = f'Не выбран файл задачи'
            return

        count = 0
        mutation = 0
        island = 0
        exchange = 0
        try:
            count = int(self.count.get())
            if count < 1:
                raise KeyError
        except:
            self.err['text'] = f'Неправильный ввод размера поколения'
            return
        try:
            mutation = float(self.mutation.get())
            if mutation < 0 or mutation > 1:
                raise KeyError
        except:
            self.err['text'] = f'Неправильный ввод мутации'
            return
        if self.gen_type == 2:
            try:
                island = int(self.island.get())
                if island < 1:
                    raise KeyError
            except:
                self.err['text'] = f'Неправильный ввод кол-ва островов'
                return
            try:
                exchange = float(self.exchange.get())
                if exchange < 1:
                    raise KeyError
            except:
                self.err['text'] = f'Неправильный ввод частоты обмена'
                return
        self.err['text'] = ''

        alg = None
        if self.gen_type == 1:
            alg = Classical(count, self.task, self.parent_selection.get(),
                            self.crossover.get(), mutation, self.selection.get())
        elif self.gen_type == 2:
            alg = IslandModel(count, island, exchange, self.task, self.random.get(),
                              self.parent_selection.get(), self.crossover.get(), mutation, self.selection.get())
        else:
            alg = Cellular(count, self.task, self.crossover.get(), mutation)
        log1, log2 = alg.solve()
        helper = TaskHelper()
        helper.save_log(log1)
        if log2 is not None:
            helper.save_log(log2)
