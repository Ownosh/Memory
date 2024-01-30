import random
from tkinter import *
from tkinter import Tk, Frame, Menu, ttk


# root window
root = Tk()
root.geometry('1820x950')
root.title('Menu Demo')
#set window color
root.configure(bg='#95E1D3')

st = Style()
st.configure('W.TButton', background='#345', foreground='black', font=('Arial', 14 ))

Button(root, text='Smash Me', style='W.TButton', command=None).pack()
# create a menubar
menubar = Menu(root)
root.config(menu=menubar)

# create the file_menu
file_menu = Menu(
    menubar,
    tearoff=0
)

# add menu items to the File menu
file_menu.add_command(label='New')
file_menu.add_command(label='Open...')
file_menu.add_command(label='Close')
file_menu.add_separator()

# add Exit menu item
file_menu.add_command(
    label='Exit',
    command=root.destroy
)

# add the File menu to the menubar
menubar.add_cascade(
    label="Options",
    menu=file_menu
)
# create the Help menu
help_menu = Menu(
    menubar,
    tearoff=0
)

help_menu.add_command(label='Welcome')
help_menu.add_command(label='About...')

# add the Help menu to the menubar
menubar.add_cascade(
    label="Help",
    menu=help_menu
)
# model
class DataGame:
    def __init__(self):
        self.buttons_text = [78, 24, 33, 49, 56, 66, 71, 82] * 2

    def get_btn_list(self):
        btn_list = []
        for btn_i in self.buttons_text:
            b = tk.Button(root, text=str(btn_i), fg='black', bg='white', width=5, activeforeground='white',
                          activebackground='white', height=2, font=('Comic Sans MS', 19))
            btn_list.append(b)
        return btn_list

root.mainloop()
if __name__ == '__main__':
    root = tk.Tk()
    cg = ControllerGame(root)

    root.mainloop()