import tkinter as tk
import random
import json


class ColorGame:
    def __init__(self, window):
        self.window = window
        with open("scores.json", "r") as file:
            self.score = sorted(
                json.load(file).items(), key=lambda x: x[1], reverse=True
            )
            self.score = {k: v for k, v in self.score}
            file.close()
        self.current_gamer = ""
        self.current_score = 0
        # self.colors=[("Orange","#ee541a"),("Blue","#1a6dec"),("Yellow","#f3d332"),("Purple","#b244d3"),("Pink","#e65f7c"),("Green","#52d734"),("red","#ea2e35")]
        self.colors = {
            "orange": "#ee541a",
            "blue": "#1a6dec",
            "yellow": "#f3d332",
            "purple": "#b244d3",
            "pink": "#e6869a",
            "green": "#52d734",
            "red": "#ea2e35",
        }

    def start(self):
        welcome_label = tk.Label(
            self.window,
            text=f"Welcome to the Color Game!",
            font=("Helvetica", 30, "bold"),
        )
        welcome_label.pack(pady=20)

        self.listbox = tk.Listbox(self.window, width=20, font=("Helvetica", 20, "bold"))
        self.listbox.insert(tk.END, "User - Score")

        # Inserting data into the listbox
        for user, score in self.score.items():
            color = random.choice(list(self.colors.keys()))
            padding = " " * (10 - len(f"{user} - {score}"))
            self.listbox.insert(tk.END, f"{user} - {score}{padding}")
            self.listbox.itemconfig(tk.END, {"fg": color})

        self.listbox.pack(padx=10, pady=10)

        name_label = tk.Label(
            self.window, text=f"please enter your name:", font=("Helvetica", 10, "bold")
        )
        name_label.pack(pady=20)

        self.name_entry = tk.Entry(self.window, font=("Helvetica", 10))
        self.name_entry.pack(pady=10)

        button = tk.Button(
            self.window,
            text="Get Started!",
            font=("Helvetica", 10),
            command=self.check_name,
        )
        button.pack(pady=10)

        result_label = tk.Label(self.window, text="", font=("Helvetica", 10))
        result_label.pack(pady=10)
        print(self.score.keys())

    def check_name(self):
        user_input = self.name_entry.get()  # Get input and convert to lowercase
        if user_input in list(self.score.keys()):
            self.best_score = self.score[user_input]
            print(user_input, self.best_score)
        else:
            self.score[user_input] = 0
            self.save_scores()

    def check_answer(self):
        user_input = self.entry.get().lower()  # Get input and convert to lowercase
        if user_input == self.textColor:
            self.result_label.config(text="You win!")
            self.update_score()
        else:
            self.result_label.config(text="You lost!")
        self.update_window()

    def update_score(self):
        self.score[self.current_gamer] += 1
        self.current_score_label.config(text=f"score: {self.score[self.current_gamer]}")

    def save_scores(self):
        with open("scores.json", "w") as file:
            json.dump(self.score, file)

    def update_window(self):
        self.pick_colors()
        self.backScreen.config(background=self.colors[self.bgColor])
        self.text.config(
            text=self.realText,
            fg=self.colors[self.textColor],
            bg=self.colors[self.bgColor],
        )

    def pick_colors(self, random_state=None):
        if random_state:
            random.seed(random_state)
        self.realText = random.choice(list(self.colors.keys()))
        self.textColor = random.choice(list(self.colors.keys()))
        self.bgColor = random.choice(
            [i for i in self.colors.keys() if i != self.textColor]
        )

    def play(self):
        self.best_score = self.score[self.current_gamer]
        self.current_score_label = tk.Label(
            self.window, text=f"score: {self.score}", font=("Helvetica", 10)
        )
        self.current_score_label.pack(pady=20)
        self.pick_colors(42)
        self.backScreen = tk.Frame(self.window, background=self.colors[self.bgColor])

        self.text = tk.Label(
            self.backScreen,
            text=self.realText,
            font=("Calibri", 90, "bold"),
            fg=self.colors[self.textColor],
            bg=self.colors[self.bgColor],
        )
        self.backScreen.pack(fill="both", expand=True)
        self.text.pack(pady=100)

        self.label = tk.Label(self.window, text="Enter a word:", font=("Helvetica", 10))
        self.label.pack(pady=10)
        self.entry = tk.Entry(self.window, font=("Helvetica", 10))
        self.entry.pack(pady=10)

        self.button = tk.Button(
            self.window, text="Check", font=("Helvetica", 10), command=self.check_answer
        )
        self.button.pack(pady=10)

        # Create a label to show the result
        self.result_label = tk.Label(self.window, text="", font=("Helvetica", 10))
        self.result_label.pack(pady=10)
