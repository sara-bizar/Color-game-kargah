import tkinter as tk
from game_objects import *


if __name__ == "__main__":

    window = tk.Tk()
    width, height = 900, 900
    window.title("Color Game App")
    window.geometry(f"{width}x{height}")
    window.minsize(300, 200)
    window.maxsize(900, 600)

    game1 = ColorGame(window)
    if not game1.current_gamer:
        game1.start()
    else:
        game1.play()

    window.mainloop()
