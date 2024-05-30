import tkinter as tk
import json
import random


# Main Application Class
class ColorGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Game Application")
        width, height = 900, 900
        self.window.geometry(f"{width}x{height}")
        self.window.minsize(300, 200)
        self.window.maxsize(900, 600)
        self.get_user_score()
        self.get_colors()

        self.user_name = ""

        self.welcome_window = WelcomeWindow(self)
        self.game_window = GameWindow(self)

        self.show_welcome_window()

    def get_user_score(self):
        with open("scores.json", "r") as file:
            self.score = sorted(
                json.load(file).items(), key=lambda x: x[1], reverse=True
            )
            self.score = {k: v for k, v in self.score}
            file.close()

    def get_colors(self):
        with open("colors.json", "r") as file:
            self.colors = json.load(file)
            file.close()

    def show_welcome_window(self):
        self.get_user_score()
        self.game_window.pack_forget()
        self.welcome_window.pack()
        self.welcome_window.update_chart()

    def start_game(self, name):
        self.user_name = name
        self.welcome_window.pack_forget()
        self.game_window.pack()
        self.game_window.start_game()
        self.game_window.update_window(name)
        self.game_window.start_timer()

    def save_scores(self):
        with open("scores.json", "w") as file:
            json.dump(self.score, file)


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
            self, text=f"please enter your name:", font=("Helvetica", 10, "bold")
        )
        self.name_label.pack(pady=20)

        self.name_entry = tk.Entry(self, font=("Helvetica", 10))
        self.name_entry.pack(pady=10)

        self.start_button = tk.Button(
            self, text="Get Started!", font=("Helvetica", 10), command=self.start_game
        )
        self.start_button.pack(pady=10)

    def start_game(self):
        name = self.name_entry.get()
        if name:
            if not (name in list(self.app.score.keys())):
                self.app.score[name] = 0
                self.app.save_scores()
            self.app.start_game(name)

    def update_chart(self):
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, "User - Score")
        for user, score in self.app.score.items():
            color = random.choice(list(self.app.colors.keys()))
            padding = " " * (10 - len(f"{user} - {score}"))
            self.listbox.insert(tk.END, f"{user} - {score}{padding}")
            self.listbox.itemconfig(tk.END, {"fg": color})


# Game Window Class
class GameWindow(tk.Frame):
    def __init__(self, app):
        super().__init__(app.window)
        self.app = app

        self.remaining_time = 30  # 30 seconds timer
        self.current_score_label = tk.Label(self, text="", font=("Helvetica", 10))
        self.current_score_label.pack(pady=20)

        self.timer_label = tk.Label(
            self,
            text=f"Time remaining: {self.remaining_time} seconds",
            font=("Helvetica", 10),
        )
        self.timer_label.pack(pady=10)

        self.pick_colors()
        self.backScreen = tk.Frame(self, background=self.app.colors[self.bgColor])
        self.text = tk.Label(
            self.backScreen,
            text=self.realText,
            font=("Calibri", 90, "bold"),
            fg=self.app.colors[self.textColor],
            bg=self.app.colors[self.bgColor],
        )
        self.backScreen.pack(fill="both", expand=True)
        self.text.pack(pady=100)

        self.label = tk.Label(self, text="Enter a word:", font=("Helvetica", 10))
        self.label.pack(pady=10)
        self.entry = tk.Entry(self, font=("Helvetica", 10))
        self.entry.pack(pady=10)
        self.button = tk.Button(
            self, text="Check", font=("Helvetica", 10), command=self.check_answer
        )
        self.button.pack(pady=10)

        # Create a label to show the result
        self.result_label = tk.Label(self, text="", font=("Helvetica", 10))
        self.result_label.pack(pady=10)

    def pick_colors(self, random_state=None):
        if random_state:
            random.seed(random_state)
        self.realText = random.choice(list(self.app.colors.keys()))
        self.textColor = random.choice(list(self.app.colors.keys()))
        self.bgColor = random.choice(
            [i for i in self.app.colors.keys() if i != self.textColor]
        )

    def check_answer(self):
        user_input = self.entry.get().lower()  # Get input and convert to lowercase
        if user_input == self.textColor:
            self.result_label.config(text="You win!")
            self.current_score += 1
        else:
            self.result_label.config(text="You lost!")
        self.update_window(self.user_name)

    def update_window(self, name):
        self.user_name = name
        self.current_score_label.config(
            text=f"score: {self.current_score}\nbest score: {max(self.app.score[self.app.user_name], self.current_score)}"
        )
        self.pick_colors()
        self.backScreen.config(background=self.app.colors[self.bgColor])
        self.text.config(
            text=self.realText,
            fg=self.app.colors[self.textColor],
            bg=self.app.colors[self.bgColor],
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
            self.app.score[self.user_name] = max(
                self.app.score[self.user_name], self.current_score
            )
            self.app.save_scores()
            self.app.show_welcome_window()  # Time's up, return to welcome window

    def start_game(self):
        self.current_score = 0
