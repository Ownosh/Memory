from tkinter import *
from memory import Memory
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

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
        img3 = PhotoImage(file="img_rules_menu/rules.png")
        self.canvas.create_image(0, 0, anchor=NW, image=img3)
        back_button = Button(self.canvas, text="Назад", font=("Times New Roman", 20), bg='#3D9CEB', fg='white',
                             command=self.main_menu)
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
        img_obj3 = PhotoImage(file="img_rules_menu/dio.png")
        self.canvas.create_image(0, 0, anchor=NW, image=img_obj3)
        play_button = Button(self.root, text="Играть", fg="Black", font=('times new roman', 15), bg='#F4FBED',
                             width=18, height=1, command=self.start_game)
        self.canvas.create_window(560, 200, anchor=NW, window=play_button)
        rules_button = Button(self.root, text="Правила", fg="Black", font=('times new roman', 15), bg='#F4FBED',
                              width=18, height=1, command=self.show_rules)
        self.canvas.create_window(560, 260, anchor=NW, window=rules_button)
        exit_button = Button(self.root, text="Выход", fg="Black", font=('times new roman', 15), bg='#F4FBED',
                             width=18, height=1, command=self.exit_game)
        self.canvas.create_window(560, 320, anchor=NW, window=exit_button)
        self.root.mainloop()


