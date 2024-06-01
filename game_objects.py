import tkinter as tk
import random


# Main Application Class
class ColorGame:
    def __init__(self, window, manager):
        self.window = window
        self.manager = manager
        self.window.title("Color Game Application")
        width, height = 1300, 1100
        self.window.geometry(f"{width}x{height}")
        self.window.minsize(300, 200)
        self.window.maxsize(900, 600)
        self.manager.create_table_users()
        self.manager.create_colors_table()
        self.scores = self.manager.retrieve_user_data()
        self.colors = self.manager.retrieve_all_colors()

        self.user_name = ""
        self.best_score = 0
        self.trys = 1

        self.welcome_window = WelcomeWindow(self)
        self.game_window = GameWindow(self)

        self.show_welcome_window()

    def show_welcome_window(self):
        self.scores = self.manager.retrieve_user_data()
        self.game_window.pack_forget()
        self.welcome_window.pack()
        self.welcome_window.update_chart()

    def start_game(self, name):
        self.user_name = name
        for username, score, trys in self.scores:
            if username == name:
                self.best_score = score
                self.trys = trys + 1
        self.welcome_window.pack_forget()
        self.welcome_window.update_button()
        self.game_window.pack()
        self.game_window.start_game()
        self.game_window.update_window(name)
        self.game_window.start_timer()


# Welcome Window Class
class WelcomeWindow(tk.Frame):
    def __init__(self, app):
        super().__init__(app.window)
        self.app = app
        self.welcome_label = tk.Label(
            self, text="Welcome to Color Game!", font=("Helvetica", 30, "bold")
        )
        self.welcome_label.pack(pady=20)

        self.listbox = tk.Listbox(self, width=20, font=("Helvetica", 20, "bold"))
        self.listbox.pack(padx=10, pady=10)

        self.name_label = tk.Label(
            self, text=f"please enter your name:", font=("Helvetica", 15, "bold")
        )
        self.name_label.pack(pady=5)

        self.name_entry = tk.Entry(self, font=("Helvetica", 15))
        self.name_entry.pack(pady=10)

        self.start_button = tk.Button(
            self,
            text="Get Started!",
            font=("Helvetica", 10, "bold"),
            command=self.start_game,
        )
        self.start_button.pack(pady=10)

    def start_game(self):
        name = self.name_entry.get()
        if name:
            if not (name in [i[0] for i in self.app.scores]):
                self.app.manager.store_user_data(name, 0, 1)
            self.app.start_game(name)

    def on_delete(self, name):
        print(f"deleted {name}")

    def update_chart(self):
        self.app.scores = sorted(self.app.scores, key=lambda x: x[1], reverse=True)
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, "User - Score - Trys")
        for user, score, trys in self.app.scores:
            color = random.choice([i[0] for i in self.app.colors])
            self.listbox.insert(tk.END, f"{user} - {score} - {trys}")
            self.listbox.itemconfig(tk.END, {"fg": color})

    def update_button(self):
        self.start_button.config(text="Retry!")


# Game Window Class
class GameWindow(tk.Frame):
    def __init__(self, app):
        super().__init__(app.window)
        self.app = app

        self.remaining_time = 30  # 30 seconds timer
        self.info_label = tk.Label(self, text="", font=("Helvetica", 10))
        self.info_label.pack(pady=10)

        self.timer_label = tk.Label(
            self,
            text=f"Time remaining: {self.remaining_time} seconds",
            font=("Helvetica", 10, "bold"),
        )
        self.timer_label.pack(pady=5)

        self.pick_colors()
        self.backScreen = tk.Frame(
            self,
            background=next(
                (code for name, code in self.app.colors if name == self.bgColor), None
            ),
        )
        self.text = tk.Label(
            self.backScreen,
            text=self.realText,
            font=("Calibri", 80, "bold"),
            fg=next(
                (code for name, code in self.app.colors if name == self.textColor), None
            ),
            bg=next(
                (code for name, code in self.app.colors if name == self.bgColor), None
            ),
        )
        self.backScreen.pack(fill="both", expand=True)
        self.text.pack(pady=100)

        self.label = tk.Label(
            self, text="Enter your color guess:", font=("Helvetica", 15, "bold")
        )
        self.label.pack(pady=5)
        self.entry = tk.Entry(self, font=("Helvetica", 15))
        self.entry.pack(pady=5)
        self.button = tk.Button(
            self,
            text="Check",
            font=("Helvetica", 10, "bold"),
            command=self.check_answer,
        )
        self.button.pack(pady=10)

        # Create a label to show the result
        self.result_label = tk.Label(self, text="", font=("Helvetica", 10))
        self.result_label.pack(pady=10)

    def pick_colors(self, random_state=None):
        if random_state:
            random.seed(random_state)
        self.realText = random.choice([i[0] for i in self.app.colors])
        self.textColor = random.choice([i[0] for i in self.app.colors])
        self.bgColor = random.choice(
            [i for i in [j[0] for j in self.app.colors] if i != self.textColor]
        )

    def check_answer(self):
        user_input = self.entry.get().lower()  # Get input and convert to lowercase
        if user_input == self.textColor:
            self.result_label.config(text="Correct!")
            self.current_score += 1
        else:
            self.result_label.config(text="Wrong!")
        self.update_window(self.user_name)

    def update_window(self, name):
        self.user_name = name
        self.info_label.config(
            text=f"gamer: {self.user_name}\nscore: {self.current_score}\nbest score: {max(self.app.best_score, self.current_score)}"
        )
        self.pick_colors()

        self.backScreen.config(
            background=next(
                (code for name, code in self.app.colors if name == self.bgColor), None
            ),
        )
        self.text.config(
            text=self.realText,
            fg=next(
                (code for name, code in self.app.colors if name == self.textColor), None
            ),
            bg=next(
                (code for name, code in self.app.colors if name == self.bgColor), None
            ),
        )
        self.entry.delete(0, tk.END)

    def start_timer(self):
        self.remaining_time = 30  # Reset the timer
        self.countdown()

    def countdown(self):
        if self.remaining_time > 0:
            self.timer_label.config(
                text=f"Time remaining: {self.remaining_time} seconds"
            )
            self.remaining_time -= 1
            self.after(1000, self.countdown)  # Call countdown again after 1 second
        else:
            self.app.manager.store_user_data(
                self.user_name,
                max(self.app.best_score, self.current_score),
                self.app.trys,
            )
            self.app.show_welcome_window()  # Time's up, return to welcome window

    def start_game(self):
        self.current_score = 0
        self.result_label.config(text="")
