import tkinter as tk
from game_objects import*
window=tk.Tk()
window.title("color game")
window.geometry("900x600")
window.resizable(False,False)

game1=game(window)

window.mainloop()

