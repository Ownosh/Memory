from tkinter import *
from random import shuffle
from tkinter import messagebox
from math import sqrt

NUMBER = 15


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


class MainMenu:
    def __init__(self):
        self.window = None
        self.root = Tk()
        self.canvas = Canvas(self.root, width=900, height=500, highlightthickness=0)
        self.canvas.pack()
        self.root.title("Запомни одинаковые")
        self.root.geometry("900x500")

    def multiplayer(self):
        pass



    def start_game(self):
        self.root.destroy()
        self.memory = Memory()
        self.memory.root.mainloop()

    def show_rules(self):

        self.root.title("Правила")
        self.canvas.delete('all')
        img3 = PhotoImage(file="img/rin_rules.png")
        self.canvas.create_image(0, 0, anchor=NW, image=img3)
        back_button = Button(self.canvas, text="Назад", command=self.main_menu)
        self.canvas.create_window(800, 10, anchor=NW, window=back_button)
        self.canvas.pack()
        self.root.mainloop()

    def exit_game(self):
        self.root.destroy()

    def main_menu(self):
        width = 900
        height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.canvas.delete('all')
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.root.title("Запомни одинаковые")
        img_obj3 = PhotoImage(file="img/dio.png")
        self.canvas.create_image(0, 0, anchor=NW, image=img_obj3)
        play_button = Button(self.root, text="Играть", fg="Black", font=('times new roman', 15), bg='#CE5480', width=18,
                             height=1, command=self.start_game)
        self.canvas.create_window(345, 210, anchor=NW, window=play_button)
        rules_button = Button(self.root, text="Правила", fg="Black", font=('times new roman', 15), bg='#CE5480',
                              width=18,
                              height=1, command=self.show_rules)
        self.canvas.create_window(345, 330, anchor=NW, window=rules_button)
        multiplayer = Button(self.root, text="2 игрока", fg="Black", font=('times new roman', 15), bg='#CE5480', width=18,
                             height=1)
        self.canvas.create_window(345, 270, anchor=NW, window=multiplayer)
        exit_button = Button(self.root, text="Выход", fg="Black", font=('times new roman', 15), bg='#CE5480', width=18,
                             height=1, command=self.exit_game)
        self.canvas.create_window(345, 390, anchor=NW, window=exit_button)
        self.root.mainloop()


class Memory:
    def __init__(self, number=15):
        self.root = Tk()
        self.root.title("Одиночная игра")
        bg = PhotoImage(file="img/bg1prob.png")
        self.label10 = Label(self.root, image=bg)
        self.label10.place(x=0, y =0)
        self.my_frame = Frame(self.root)
        self.my_frame.pack(anchor = NW)
        center_window(self.root, 1100,620)
        self.matches = [x for x in range(number) for _ in range(2)]
        shuffle(self.matches)

        self.chances = 35


        self.won = False
        self.cols = 0
        self.answer_list = []
        self.NUMBER = number

        self.label = Label(self.root, text=f"{self.chances}", font=("Helvetica", 30))
        self.label.pack(anchor=NW)

        self.reset_game()
        self.cols = self.find_rows_cols(len(self.matches))[1]

        self.tiles = []
        for i in range(len(self.matches)):
            self.tiles.append(Button(self.my_frame, text=' ', font=("Helvetica", 40), height=1, width=3,fg='#B2DFDB', bd=4,
                                     command=lambda i=i: self.onclick(i)))

        for i, tile in enumerate(self.tiles):
            row = i % self.cols
            col = int(i / self.cols)
            tile.grid(row=row, column=col)

        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)

        option_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Options", menu=option_menu)
        option_menu.add_command(label="Reset Game", command=self.reset_game)
        option_menu.add_separator()
        option_menu.add_command(label="Выход", command=self.back)

        self.root.mainloop()

    def onclick(self, index):
        self.label["text"] = f'{self.chances}'

        if self.tiles[index]["text"] == ' ':
            self.tiles[index]["text"] = str(self.matches[index])
            self.tiles[index]['state'] = DISABLED
            self.answer_list.append(index)
        else:
            self.tiles[index]["text"] = ' '

        flag = True
        if len(self.answer_list) == 2:
            if self.matches[self.answer_list[0]] == self.matches[self.answer_list[1]] and flag:
                self.tiles[self.answer_list[0]]["state"] = DISABLED
                self.tiles[self.answer_list[1]]["state"] = DISABLED
                self.label["text"] = f"ВЕРНО!Попыток: {self.chances}"
                self.won += 1
                if self.won == self.NUMBER:
                    self.label["text"] = "ПОБЕДА!"
            else:
                self.chances -= 1
                self.label["text"] = f"Попыток: {self.chances}"
                messagebox.showinfo("Incorrect", "ОШИБКА")
                self.tiles[self.answer_list[0]]["state"] = NORMAL
                self.tiles[self.answer_list[1]]["state"] = NORMAL
                self.tiles[self.answer_list[0]]["text"] = ' '
                self.tiles[self.answer_list[1]]["text"] = ' '

            self.answer_list = []

        if self.chances == 0:
            for tile in self.tiles:
                tile["state"] = DISABLED
            self.label["text"] = "ИГРА ПРОИГРАНА"

    def reset_game(self):
        self.answer_list = []
        self.chances = 35
        self.won = False
        shuffle(self.matches)

        self.label["text"] = ' '

        self.cols = self.find_rows_cols(len(self.matches))[1]

        self.tiles = []
        for i in range(len(self.matches)):
            self.tiles.append(Button(self.my_frame, text=' ', font=("Helvetica", 40), height=1, width=3,fg='#B2DFDB', bd=4,
                                     command=lambda i=i: self.onclick(i)))

        for i, tile in enumerate(self.tiles):
            row = i % self.cols
            col = int(i / self.cols)
            tile.grid(row=row, column=col)

    def back(self):
        self.root.destroy()



    def find_rows_cols(self, number):
        max_cols = int(sqrt(number))
        cols = int()
        for i in range(max_cols, 0, -1):
            if number % i == 0:
                cols = i
                break
        rows = int(number / cols)
        return rows, cols


game = MainMenu()
game.main_menu()
