from tkinter import *
from random import shuffle
from math import sqrt
import os


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
        self.main_menu()

    def start_game(self):
        self.root.destroy()
        Memory()

    def show_rules(self):
        self.root.title("Правила")
        self.canvas.delete('all')
        img3 = PhotoImage(file="img_rules/rin_rules.png")
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
        self.root.resizable(width=False, height=False)
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
        self.canvas.create_window(560, 200, anchor=NW, window=play_button)
        rules_button = Button(self.root, text="Правила", fg="Black", font=('times new roman', 15), bg='#CE5480',
                              width=18,
                              height=1, command=self.show_rules)
        self.canvas.create_window(560, 260, anchor=NW, window=rules_button)
        exit_button = Button(self.root, text="Выход", fg="Black", font=('times new roman', 15), bg='#CE5480', width=18,
                             height=1, command=self.exit_game)
        self.canvas.create_window(560, 320, anchor=NW, window=exit_button)
        self.root.mainloop()


class Memory:
    def __init__(self, number=8):
        self.root = Tk()
        self.root.title("Одиночная игра")
        self.bg = PhotoImage(file="img/bg1prob.png")
        self.label10 = Label(self.root, image=self.bg)
        self.label10.place(x=-5, y=0)

        self.advanced_selected = [False, False, False]
        self.my_frame = Frame(self.root)
        self.my_frame.pack(anchor=NW)
        center_window(self.root, 1090, 630)
        self.root.resizable(width=False, height=False)

        self.chances = 10
        self.points = 0
        self.NUMBER = number
        self.increasePoints = 10
        self.won = False

        self.label = Label(self.root, text="", font=("Times New Roman", 40), bg='#5F74A4', fg='white')
        self.label.pack()
        self.answer_list = []

        self.setup_menu()
        self.setup_buttons()

        self.root.mainloop()

    def setup_menu(self):
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)

        option_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Настройки", menu=option_menu)
        option_menu.add_command(label="Перезапустить", command=self.reset_game)
        option_menu.add_separator()
        option_menu.add_command(label="Назад", command=self.back)

        difficulty_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Уровень сложности", menu=difficulty_menu)
        difficulty_menu.add_command(label="Начинающий", command=lambda: self.set_difficulty(8, 2, 0, 10))
        difficulty_menu.add_command(label="Средний", command=lambda: self.set_difficulty(10, 2, 1, 15))
        difficulty_menu.add_command(label="Продвинутый", command=lambda: self.set_difficulty(15, 2, 2, 20))

    def setup_buttons(self):
        self.buttons = [
            Button(self.root, text="Начальный", fg="Black", font=('times new roman', 15), bg='White', width=18,
                   command=lambda: self.set_difficulty(8, 2, 0, 10)),
            Button(self.root, text="Средний", fg="Black", font=('times new roman', 15), bg='White', width=18,
                   command=lambda: self.set_difficulty(10, 2, 1, 15)),
            Button(self.root, text="Продвинутый", fg="Black", font=('times new roman', 15), bg='White', width=18,
                   command=lambda: self.set_difficulty(15, 2, 2, 20))
        ]
        for button in self.buttons:
            button.pack(anchor=W, padx=50, pady=10)

    def set_difficulty(self, number, range_, level, chances):
        if not self.advanced_selected[level]:
            self.hide_buttons()
            self.advanced_selected = [False, False, False]
            self.advanced_selected[level] = True
            self.label.pack(anchor=SW)
            self.reset_game_parameters(number, range_, chances)
            self.create_tiles()
        else:
            print(
                f"Уровень сложности '{['Начальный', 'Средний', 'Продвинутый'][level]}' уже был выбран. Повторный выбор невозможен.")


    def hide_buttons(self):
        for button in self.buttons:
            button.pack_forget()

    def reset_game_parameters(self, number, range_, chances):
        self.NUMBER = number
        self.matches = [x for x in range(number) for _ in range(range_)]
        shuffle(self.matches)
        self.reset_game(chances)

    def reset_game(self, chances=10):
        self.answer_list = []
        self.chances = chances
        self.points = 0
        self.increasePoints = 10
        self.won = False
        self.label["text"] = ' '
        shuffle(self.matches)
        self.create_tiles()
        self.change_background_image()

    def create_tiles(self):
        self.cols = self.find_rows_cols(len(self.matches))[1]
        for item in self.my_frame.winfo_children():
            item.destroy()
        self.tiles = [
            Button(self.my_frame, text=' ', font=("Times New Roman", 40), height=1, width=3, fg='Grey', bd=4,
                   command=lambda i=i: self.onclick(i)) for i in range(len(self.matches))
        ]
        for i, tile in enumerate(self.tiles):
            row = i % self.cols
            col = int(i / self.cols)
            tile.grid(row=row, column=col)
        self.show_elements()

    def show_elements(self):
        for i, tile in enumerate(self.tiles):
            tile.config(text=str(self.matches[i]))
        self.root.after(5000, self.hide_elements)
        for tile in self.tiles:
            tile.config(state='disabled')

    def hide_elements(self):
        for tile in self.tiles:
            tile.config(text=' ')
            tile.config(state='normal')

    def change_background_image(self):
        # List all image files in the directory
        image_files = [file for file in os.listdir("img") if file.endswith(".png")]

        # Select a random image file
        import random
        selected_image = random.choice(image_files)

        # Update the background image
        self.bg = PhotoImage(file=f"img/{selected_image}")
        self.label10.config(image=self.bg)

    def onclick(self, index):
        self.label["text"] = f'Попыток: {self.chances}, Очков: {self.points}'
        tile = self.tiles[index]

        if tile["text"] == ' ':
            tile["text"] = str(self.matches[index])
            tile['state'] = DISABLED
            self.answer_list.append(index)
        else:
            tile["text"] = ' '

        if len(self.answer_list) == 2:
            self.check_match()

    def check_match(self):
        first, second = self.answer_list
        if self.matches[first] == self.matches[second]:
            self.points += self.increasePoints
            self.increasePoints += 10
            self.tiles[first]["state"] = DISABLED
            self.tiles[second]["state"] = DISABLED
            self.label["text"] = f"+{self.increasePoints - 10} очков!, Стало:{self.points}"
            self.won += 1
            if self.won == self.NUMBER:
                self.show_victory_window()
        else:
            self.increasePoints = 10
            self.chances -= 1
            self.label["text"] = f"Попыток: {self.chances}, Очков: {self.points}"
            self.tiles[first].after(500, lambda: self.tiles[first].config(text=' '))
            self.tiles[second].after(500, lambda: self.tiles[second].config(text=' '))
            self.tiles[first]["state"] = NORMAL
            self.tiles[second]["state"] = NORMAL

        self.answer_list = []

        if self.chances == 0:
            for tile in self.tiles:
                tile["state"] = DISABLED
            self.label["text"] = "ИГРА ПРОИГРАНА"

    def back(self):
        self.root.destroy()
        MainMenu()

    def find_rows_cols(self, number):
        max_cols = int(sqrt(number))
        for i in range(max_cols, 0, -1):
            if number % i == 0:
                cols = i
                break
        rows = number // cols
        return rows, cols

    def show_victory_window(self):
        # Скрываем основное окно
        self.root.withdraw()

        # Создаем новое окно "victory window"
        self.victory_window = Toplevel()
        self.victory_window.title("Победа!")
        self.victory_window.geometry("900x500")

        # Добавляем фоновое изображение
        victory_bg = PhotoImage(file="img/bg1prob1.png")
        victory_bg_label = Label(self.victory_window, image=victory_bg)
        victory_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Добавляем кнопки повтора и выхода
        replay_button = Button(self.victory_window, text="Повторить", command=self.reset_game)
        replay_button.place(relx=0.5, rely=0.5, anchor="center")

        exit_button = Button(self.victory_window, text="Выйти", command=self.root.destroy)
        exit_button.place(relx=0.5, rely=0.6, anchor="center")

        # Добавим обработчик закрытия окна победы для восстановления основного окна
        self.victory_window.protocol("WM_DELETE_WINDOW", self.restore_main_window)

    def restore_main_window(self):
        # Восстанавливаем основное окно
        self.root.deiconify()

    def reset_game1(self, chances=10):
        # Закрываем окно победы, если оно открыто
        if hasattr(self, 'victory_window') and self.victory_window.winfo_exists():
            self.victory_window.destroy()


if __name__ == '__main__':
    game = MainMenu()
