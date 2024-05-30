import tkinter as tk
from tkinter import ttk


# Main Application Class
class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Application")

        self.user_name = tk.StringVar()

        self.welcome_window = WelcomeWindow(self)
        self.game_window = GameWindow(self)

        self.show_welcome_window()

    def show_welcome_window(self):
        self.game_window.pack_forget()
        self.welcome_window.pack()

    def start_game(self, name):
        self.user_name.set(name)
        self.welcome_window.pack_forget()
        self.game_window.pack()
        self.game_window.update_greeting(name)
        self.game_window.start_timer()


# Welcome Window Class
class WelcomeWindow(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app

        self.label = ttk.Label(self, text="Welcome! Please enter your name:")
        self.label.pack(pady=10)

        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=10)

        self.start_button = ttk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

    def start_game(self):
        name = self.name_entry.get()
        if name:
            self.app.start_game(name)
            self.clear_entry()

    def clear_entry(self):
        self.name_entry.delete(0, tk.END)


# Game Window Class
class GameWindow(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.remaining_time = 3  # `30` seconds timer

        self.greeting_label = ttk.Label(self, text="")
        self.greeting_label.pack(pady=10)

        self.timer_label = ttk.Label(
            self, text=f"Time remaining: {self.remaining_time} seconds"
        )
        self.timer_label.pack(pady=10)

    def update_greeting(self, name):
        self.greeting_label.config(text=f"Hello, {name}! Welcome to the game.")

    def start_timer(self):
        self.remaining_time = 3  # Reset the timer
        self.countdown()

    def countdown(self):
        if self.remaining_time > 0:
            self.timer_label.config(
                text=f"Time remaining: {self.remaining_time} seconds"
            )
            self.remaining_time -= 1
            self.after(1000, self.countdown)  # Call countdown again after 1 second
        else:
            self.app.show_welcome_window()  # Time's up, return to welcome window


if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
