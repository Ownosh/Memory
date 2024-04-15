from tkinter import *
from random import shuffle

NUMBER = 15
class MemoryGame:
    def __init__(self):
        self.window = None  # Initialize the window attribute
        self.root = Tk()
        self.root.title("Запомни одинаковые")
        self.root.geometry("900x500")
        self.ROW = 7
        self.COLUMNS = 7
        self.files = ['red.png', 'yellow.png', 'gold.png',
                      'green.png', 'emerald.png', 'cyan.png',
                      'blue.png', 'pink.png', 'azure.png',
                      'bronze.png', 'purple.png', 'scarlet.png',
                      'steel.png', 'silver.png'] * 2
        shuffle(self.files)
        self.Buttons = []
        self.img = []

    def return_to_main_menu(self):
        self.window.destroy()
        self.main_menu()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def start_game(self):
        self.root.destroy()  # Hide the main window
        self.window = Tk()
        self.window.title("Игра")
        self.center_window(self.window, 900, 500)

        img3 = PhotoImage(file="img/Frame 4.png")  # Update the file path if needed
        background_label = Label(self.window, image=img3)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        for i in range(self.ROW):
            temp = []
            for j in range(self.COLUMNS):
                btn = Button(self.window, width=7, height=3)
                temp.append(btn)
                btn.grid(row=i, column=j)  # Place the button directly on the window
            self.Buttons.append(temp)

        for i in range(self.ROW):
            for j in range(self.COLUMNS):
                btn = self.Buttons[i][j]
                btn.grid(row=i, column=j, padx=3, pady=3)

        self.window.mainloop()

    def show_rules(self):
        self.root.destroy()  # Destroy the previous root window
        tk = Tk()  # Create a new Tkinter root window
        tk.title("Правила")
        self.center_window(tk, 900, 500)
        canvas2 = Canvas(tk, width=900, height=500, highlightthickness=0)
        canvas2.pack()
        img3 = PhotoImage(file="img/rin_rules.png")  # Load the image for the canvas
        canvas2.create_image(0, 0, anchor=NW, image=img3)  # Display the image on the canvas
        back_button = Button(canvas2, text="Назад", command=lambda: self.main_menu())
        back_button_window = canvas2.create_window(800, 10, anchor=NW, window=back_button)
        tk.mainloop()

    def exit_game(self):
        self.root.destroy()

    def main_menu(self):
        width = 900
        height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))
        canvas = Canvas(self.root, width=900, height=500, highlightthickness=0)
        canvas.pack()
        img_obj3 = PhotoImage(file="img/dio.png")
        canvas.create_image(0, 0, anchor=NW, image=img_obj3)
        play_button = Button(self.root, text="Играть", fg="Black", font=('times new roman', 15), bg='#CE5480', width=18,
                             height=1, command=self.start_game)
        play_button_window = canvas.create_window(345, 210, anchor=NW, window=play_button)
        rules_button = Button(self.root, text="Правила", fg="Black", font=('times new roman', 15), bg='#CE5480',
                              width=18,
                              height=1, command=self.show_rules)
        rules_button_window = canvas.create_window(345, 300, anchor=NW, window=rules_button)
        exit_button = Button(self.root, text="Выход", fg="Black", font=('times new roman', 15), bg='#CE5480', width=18,
                             height=1, command=self.exit_game)
        exit_button_window = canvas.create_window(345, 390, anchor=NW, window=exit_button)
        self.root.mainloop()


game = MemoryGame()
game.main_menu()
