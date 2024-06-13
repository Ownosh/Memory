import os
import sys
import random
from tkinter import *
from random import shuffle
from math import sqrt
from utils import center_window


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Memory:
    def __init__(self, number=8, wid=1090, hei=630):
        self.root = Tk()
        self.root.title("Запомни одинаковые")
        self.bg = PhotoImage(file="img_rules_menu/bg.png")
        self.label10 = Label(self.root, image=self.bg)
        self.label10.place(x=-5, y=0)

        self.advanced_selected = [False, False, False]
        self.my_frame = Frame(self.root)
        self.my_frame.pack(anchor=NW)
        center_window(self.root, wid, hei)
        self.root.resizable(width=False, height=False)

        self.chances = 10
        self.points = 0
        self.NUMBER = number
        self.increasePoints = 10
        self.won = False
        self.level_selected = False
        self.reset_locked = False
        self.is_two_player_mode = False
        self.current_player = 0
        self.players = [{"points": 0, "chances": 15}, {"points": 0, "chances": 15}]

        self.root.configure(bg='#5F74A4')

        self.label = Label(self.root, text="", font=("Times New Roman", 30), bg='#3D9CEB', fg='white')
        self.label.pack(anchor=NE)
        self.label_player1 = Label(self.root, text=" ", font=("Times New Roman", 30),
                                   bg='#3D9CEB', fg='white')
        self.label_player1.pack(anchor=NW)
        self.label_player2 = Label(self.root, text=" ", font=("Times New Roman", 30),
                                   bg='#3D9CEB', fg='white')
        self.label_player2.pack(anchor=NW)

        self.answer_list = []
        self.setup_buttons()
        self.hide_player_labels()

        self.root.mainloop()

    def setup_menu(self):
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)

        option_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Настройки", menu=option_menu)
        option_menu.add_command(label="Перезапустить", command=self.reset_game)

        option_menu.add_separator()
        option_menu.add_command(label="Назад", command=self.back)

        if not self.is_two_player_mode:  # Если не режим "Игра на двоих"
            difficulty_menu = Menu(self.my_menu, tearoff=False)
            self.my_menu.add_cascade(label="Уровень сложности", menu=difficulty_menu)
            difficulty_menu.add_command(label="Начинающий",
                                        command=lambda: self.set_difficulty(8, 2, 0, 10))
            difficulty_menu.add_command(label="Средний",
                                        command=lambda: self.set_difficulty(10, 2, 1, 15))
            difficulty_menu.add_command(label="Продвинутый",
                                        command=lambda: self.set_difficulty(12, 2, 2, 20))

    def setup_buttons(self):
        self.buttons = [
            Button(self.root, text="Начальный уровень", fg="Black", font=('times new roman', 15),
                   bg='#F4FBED',
                   width=30,
                   command=lambda: self.set_difficulty(8, 2, 0, 10, )),
            Button(self.root, text="Средний уровень", fg="Black", font=('times new roman', 15),
                   bg='#F4FBED',
                   width=30,
                   command=lambda: self.set_difficulty(10, 2, 1, 15)),
            Button(self.root, text="Продвинутый уровень", fg="Black", font=('times new roman', 15),
                   bg='#F4FBED', width=30,
                   command=lambda: self.set_difficulty(12, 2, 2, 20)),
            Button(self.root, text="Игра на двоих", fg="Black", font=('times new roman', 15),
                   bg='#F4FBED', width=30,
                   command=self.two_player_mode),
            Button(self.root, text="Назад", fg="Black", font=('times new roman', 15),
                   bg='#F4FBED', width=20,
                   command=self.back)
        ]
        for button in self.buttons:
            button.pack(anchor=CENTER, padx=50, pady=10)

    def hide_single_player_score_label(self):
        self.label.pack_forget()

    def show_single_player_score_label(self):
        self.label.pack(anchor=NE)

    def two_player_mode(self):
        self.is_two_player_mode = True
        self.set_difficulty(12, 2, 2, 15)
        self.hide_single_player_score_label()

    def set_difficulty(self, number, range_, level, chances):
        if not self.level_selected and not self.advanced_selected[level]:
            self.level_selected = True
            self.setup_menu()
            self.hide_buttons()
            self.advanced_selected = [False, False, False]
            self.advanced_selected[level] = True
            self.label.pack(anchor=SW)
            self.reset_game_parameters(number, range_, chances)
            self.create_tiles()
            self.root.after(6000, self.unlock_buttons)
            if self.is_two_player_mode:
                for player in self.players:
                    player["chances"] = chances
                    player["points"] = 0
                self.show_player_labels()
            else:
                self.hide_player_labels()
        elif self.level_selected:
            print("Подождите 6 секунд перед выбором следующего уровня.")
        else:
            print(
                f"Уровень сложности '{['Начальный', 'Средний', 'Продвинутый'][level]}' "
                f"уже был выбран. Повторный выбор невозможен.")

    def unlock_buttons(self):
        self.level_selected = False

    def hide_buttons(self):
        for button in self.buttons:
            button.pack_forget()

    def reset_game_parameters(self, number, range_, chances):
        self.NUMBER = number
        self.matches = [x for x in range(number) for _ in range(range_)]
        shuffle(self.matches)
        self.load_images()
        self.current_chances = chances  # Add this line
        self.reset_game(self.current_chances)

    def reset_game(self, chances=None):
        if self.reset_locked:
            print("Подождите 6 секунд перед перезапуском игры.")
            return
        self.reset_locked = True
        self.root.after(6000, self.unlock_reset)

        self.answer_list = []
        self.chances = chances if chances is not None else self.current_chances  # Modify this line
        self.points = 0
        self.increasePoints = 10
        self.won = 0
        self.label["text"] = ' '
        shuffle(self.matches)
        self.create_tiles()
        self.change_background_image()

        if self.is_two_player_mode:
            self.players = [{"points": 0, "chances": self.current_chances}, {"points": 0, "chances": self.current_chances}]
            self.current_player = 0
            self.update_label()

    def unlock_reset(self):
        self.reset_locked = False

    def load_images(self):
        self.images = []
        for i in range(self.NUMBER):
            image = PhotoImage(file=f"balls3/{i+1}.png")
            self.images.append(image)
        self.empty_image = PhotoImage()

    def create_tiles(self):
        self.cols = self.find_rows_cols(len(self.matches))[1]
        for item in self.my_frame.winfo_children():
            item.destroy()
        self.tiles = [
            Button(self.my_frame, text=' ', font=("Times New Roman", 40), height=100, width=100, fg='#FFFFFF',
                   bg='white', bd=4,command=lambda i=i: self.onclick(i)) for i in range(len(self.matches))
        ]
        for i, tile in enumerate(self.tiles):
            row = i % self.cols
            col = int(i / self.cols)
            tile.grid(row=row, column=col)
        self.show_elements()

    def show_elements(self):
        for i, tile in enumerate(self.tiles):
            tile.config(image=self.images[self.matches[i]], state='disabled')
        self.root.after(5000, self.hide_elements)

    def hide_elements(self):
        for tile in self.tiles:
            tile.config(image=self.empty_image, state='normal')

    def change_background_image(self):
        level_folders = ["img_beginner", "img_intermediate", "img_advanced"]
        selected_folder = level_folders[self.advanced_selected.index(True)]
        image_files = [file for file in os.listdir(selected_folder) if file.endswith(".png")]
        selected_image = random.choice(image_files)
        self.bg = PhotoImage(file=f"{selected_folder}/{selected_image}")
        self.label10.config(image=self.bg)

    def onclick(self, index):
        if len(self.answer_list) >= 2 or index in self.answer_list:
            return

        if self.tiles[index]["state"] == "normal":
            self.label["text"] = (f'Попыток: {self.chances}\n'
                                  f'Очков: {self.points}')
            tile = self.tiles[index]

            if tile["image"] == str(self.empty_image):
                tile["image"] = self.images[self.matches[index]]
                tile['state'] = DISABLED
                self.answer_list.append(index)
            else:
                tile["image"] = self.empty_image

            if len(self.answer_list) == 2:
                self.root.after(700, self.check_match)

    def check_match(self):
        if len(self.answer_list) != 2:
            return

        first, second = self.answer_list
        if first == second:
            self.answer_list = []
            return
        current_player = self.players[self.current_player]

        if self.matches[first] == self.matches[second]:
            if self.is_two_player_mode:
                self.points += 10
                current_player['points'] += 10
            else:
                self.points += self.increasePoints
                current_player['points'] += self.increasePoints
                self.increasePoints += 10

            self.tiles[first]["state"] = DISABLED
            self.tiles[second]["state"] = DISABLED
            self.label["text"] = (f"Попыток: {self.chances}\n"
                                  f"Очков: {self.points}")
            self.won += 1
            if self.won == self.NUMBER:
                if self.is_two_player_mode:
                    self.show_victory_multi()
                else:
                    self.show_victory_window()
        else:
            self.increasePoints = 10
            if self.is_two_player_mode:
                current_player['chances'] -= 1
                if current_player['chances'] == 0:
                    self.show_lose_multi()
            else:
                self.chances -= 1
                if self.chances == 0:
                    self.show_lose_window()

            self.label["text"] = (f"Попыток: {self.chances}\n"
                                  f"Очков: {self.points}")
            self.tiles[first].after(500, lambda: self.tiles[first].config(image=self.empty_image, state='normal'))
            self.tiles[second].after(500, lambda: self.tiles[second].config(image=self.empty_image, state='normal'))

            for index in self.answer_list:
                self.tiles[index]["state"] = NORMAL

        self.answer_list = []
        if self.is_two_player_mode:
            self.switch_player()

    def switch_player(self):
        self.current_player = 1 if self.current_player == 0 else 0
        self.update_label()

    def update_label(self):
        self.label_player1[
            "text"] = f"Игрок 1 - Очки: {self.players[0]['points']}, Попытки: {self.players[0]['chances']}"
        self.label_player2[
            "text"] = f"Игрок 2 - Очки: {self.players[1]['points']}, Попытки: {self.players[1]['chances']}"
        current = self.players[self.current_player]
        self.label["text"] = (
            f"Очков:{current['points']}")

    def hide_player_labels(self):
        self.label_player1.pack_forget()
        self.label_player2.pack_forget()

    def show_player_labels(self):
        self.label_player1.pack(anchor=NW)
        self.label_player2.pack(anchor=NW)

    def back(self):
        from main_menu import MainMenu
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
        victory_window = Toplevel(self.root)
        victory_window.title("Победа")
        victory_window.geometry("1090x665")
        center_window(victory_window, 1090, 665)
        victory_window.configure(bg='#A45F5F')

        self.victory_bg = PhotoImage(file="img_rules_menu/win.png")
        victory_label_bg = Label(victory_window, image=self.victory_bg)
        victory_label_bg.place(x=0, y=0, relwidth=1, relheight=1)

        victory_label = Label(victory_window, text=f"Победа!\n Количество набранных очков: {self.points}",
                              font=("Times New Roman", 40), bg='white', fg='black')
        victory_label.pack()

        restart_button = Button(victory_window, text="Перезапустить", command=lambda: self.on_reset(victory_window),
                                font=('times new roman', 15), bg='White', width=18)
        restart_button.pack(anchor=CENTER, padx=50, pady=50)

        main_menu_button = Button(victory_window, text="Главное меню", command=lambda: self.on_back(victory_window),
                                  font=('times new roman', 15), bg='White', width=18)
        main_menu_button.pack(anchor=CENTER, padx=50, pady=0)

    def show_victory_multi(self):
        victory_window = Toplevel(self.root)
        victory_window.title("Победа")
        victory_window.geometry("1090x665")
        center_window(victory_window, 1090, 665)
        victory_window.configure(bg='#A45F5F')

        self.victory_bg = PhotoImage(file="img_rules_menu/win_multi.png")
        victory_label_bg = Label(victory_window, image=self.victory_bg)
        victory_label_bg.place(x=0, y=0, relwidth=1, relheight=1)

        winner = self.determine_winner()

        if winner == -1:
            victory_label = Label(victory_window, text=f"Ничья!",
                                  font=("Times New Roman", 40), bg='white', fg='black')
            victory_label.pack()
        else:
            victory_label = Label(victory_window, text=f"Победа!\n"
                                                       f" Игрок {winner + 1} набрал больше очков.",
                                  font=("Times New Roman", 40), bg='white', fg='black')
            victory_label.pack()

        restart_button = Button(victory_window, text="Перезапустить", command=lambda: self.on_reset(victory_window),
                                font=('times new roman', 15), bg='White', width=18)
        restart_button.pack(anchor=CENTER, padx=50, pady=50)

        main_menu_button = Button(victory_window, text="Главное меню", command=lambda: self.on_back(victory_window),
                                  font=('times new roman', 15), bg='White', width=18)
        main_menu_button.pack(anchor=CENTER, padx=50, pady=0)

    def determine_winner(self):
        if self.players[0]['points'] > self.players[1]['points']:
            return 0
        elif self.players[0]['points'] < self.players[1]['points']:
            return 1
        else:
            return -1

    def on_reset(self, window):
        self.reset_game()
        window.destroy()

    def on_back(self, window):
        self.back()
        window.destroy()

    def show_lose_window(self):
        lose_window1 = Toplevel(self.root)
        lose_window1.title("Поражение")
        lose_window1.geometry("1090x665")
        center_window(lose_window1, 1090, 665)
        lose_window1.configure(bg='#A45F5F')

        self.lose_bg1 = PhotoImage(file="img_rules_menu/lose.png")
        lose_label_bg1 = Label(lose_window1, image=self.lose_bg1)
        lose_label_bg1.place(x=0, y=0, relwidth=1, relheight=1)

        lose_label2 = Label(lose_window1, text=f"Поражение...\nКоличество набранных очков: {self.points}",
                            font=("Times New Roman", 40), bg='white', fg='black')
        lose_label2.pack()

        restart_button2 = Button(lose_window1, text="Перезапустить", command=lambda: self.on_reset(lose_window1),
                                font=('times new roman', 15), bg='White', width=18)
        restart_button2.pack(anchor=CENTER, padx=50, pady=50)

        main_menu_button2 = Button(lose_window1, text="Главное меню", command=lambda: self.on_back(lose_window1),
                                  font=('times new roman', 15), bg='White', width=18)
        main_menu_button2.pack(anchor=CENTER, padx=50, pady=0)

    def show_lose_multi(self):
        lose_window = Toplevel(self.root)
        lose_window.title("Поражение")
        lose_window.geometry("1090x665")
        center_window(lose_window, 1090, 665)
        lose_window.configure(bg='#A45F5F')

        self.lose_bg = PhotoImage(file="img_rules_menu/lose_multi.png")
        lose_label_bg = Label(lose_window, image=self.lose_bg)
        lose_label_bg.place(x=0, y=0, relwidth=1, relheight=1)

        loser = self.determine_loser()

        lose_label = Label(lose_window, text=f"Поражение...\nИгрок {loser + 1} проиграл.",
                           font=("Times New Roman", 40), bg='white', fg='black')
        lose_label.pack()

        restart_button = Button(lose_window, text="Перезапустить", command=lambda: self.on_reset(lose_window),
                                font=('times new roman', 15), bg='White', width=18)
        restart_button.pack(anchor=CENTER, padx=50, pady=50)

        main_menu_button = Button(lose_window, text="Главное меню", command=lambda: self.on_back(lose_window),
                                  font=('times new roman', 15), bg='White', width=18)
        main_menu_button.pack(anchor=CENTER, padx=50, pady=0)

    def determine_loser(self):
        if self.players[0]['chances'] == 0:
            return 0
        elif self.players[1]['chances'] == 0:
            return 1
        else:
            return -1
