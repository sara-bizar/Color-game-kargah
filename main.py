import tkinter as tk
from game_objects import *
from data import *


if __name__ == "__main__":
    window = tk.Tk()
    manager = UserDataManager()
    app = ColorGame(window, manager)
    window.mainloop()
