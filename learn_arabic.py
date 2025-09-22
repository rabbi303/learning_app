import tkinter as tk
import random
import os
import pygame  # for playing sound

# ---------------- Configuration ----------------

# Arabic letters in order
arabic_letters = ["ا", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش",
                  "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "و", "ه", "ي"]

# Grouped letters for Learn pages
learn_pages = [
    ["ا"],
    ["ث", "ت", "ب"],
    ["خ", "ح", "ج"],
    ["ذ", "د"],
    ["ز", "ر"],
    ["ش", "س"],
    ["ض", "ص"],
    ["ظ", "ط"],
    ["غ", "ع"],
    ["ق", "ف"],
    ["ل", "ك"],
    ["م"],
    ["ن"],
    ["و"],
    ["ه"],
    ["ي"]
]

# Pastel color palette for letter buttons
color_palette = ["#ffadad", "#ffd6a5", "#fdffb6", "#caffbf",
                 "#9bf6ff", "#a0c4ff", "#bdb2ff", "#ffc6ff"]

# Audio folder path (adjust as needed)
audio_path = "/home/rabbi/Downloads/arabic_letters_audio"


# -------------------- Main App --------------------

class ArabicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arabic Learning App")
        self.root.geometry("900x600")
        self.root.configure(bg="#d0f0fd")
        self.learn_index = 0
        self.speaker_label = None
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_screen()

        tk.Label(self.root, text="Assalamu Alaikum\nWellcome to Arabic world", font=("Arial", 36, "bold"),
                 bg="#d0f0fd", fg="#004466").pack(pady=40)

        tk.Button(self.root, text="📖 Learn Arabic", font=("Arial", 24), width=15,
                  bg="#66d9f2", command=self.start_learn_mode).pack(pady=20)

        tk.Button(self.root, text="🧩 Arabic Quiz", font=("Arial", 24), width=15,
                  bg="#1e90ff", fg="white", command=self.start_quiz_mode).pack(pady=20)

    # ----------- Learn Mode Section ------------

    def start_learn_mode(self):
        self.learn_index = 0
        self.show_learn_page()

    def show_learn_page(self):
        self.clear_screen()

        if self.learn_index >= len(learn_pages):
            self.show_learn_completion()
            return

        letters = learn_pages[self.learn_index]

        tk.Label(self.root, text="Learn Arabic Letters", font=("Arial", 24, "bold"),
                 bg="#4682b4", fg="white").pack(fill=tk.X, pady=(0, 10))

        tk.Label(self.root, text="Click a letter to hear it", font=("Arial", 18),
                 bg="#d0f0fd").pack(pady=10)

        grid_frame = tk.Frame(self.root, bg="#d0f0fd")
        grid_frame.pack(pady=30)

        for idx, letter in enumerate(letters):
            color = random.choice(color_palette)
            btn = tk.Button(grid_frame, text=letter, font=("Arial", 60, "bold"),
                            width=3, height=2, bg=color,
                            command=lambda l=letter: self.play_sound(l))
            btn.grid(row=idx // 4, column=idx % 4, padx=20, pady=20)

        self.speaker_label = tk.Label(self.root, text="", font=("Arial", 36),
                                      bg="#d0f0fd", fg="#004466")
        self.speaker_label.pack()

        nav_frame = tk.Frame(self.root, bg="#d0f0fd")
        nav_frame.pack()

        if self.learn_index > 0:
            tk.Button(nav_frame, text="⟨ Previous", font=("Arial", 16),
                      bg="#b0c4de", command=self.prev_learn_page).pack(side=tk.LEFT, padx=10)

        if self.learn_index < len(learn_pages) - 1:
            tk.Button(nav_frame, text="Next ⟩", font=("Arial", 16),
                      bg="#20b2aa", fg="white", command=self.next_learn_page).pack(side=tk.LEFT, padx=10)
        else:
            tk.Button(nav_frame, text="Finish", font=("Arial", 16),
                      bg="#20b2aa", fg="white", command=self.show_learn_completion).pack(side=tk.LEFT, padx=10)

        tk.Button(self.root, text="🏠 Back to Menu", font=("Arial", 14),
                  bg="#cccccc", command=self.create_main_menu).pack(pady=30)

    def show_learn_completion(self):
        self.clear_screen()
        tk.Label(self.root, text="Alhamdulillah , You nailed it!!", font=("Arial", 32, "bold"),
                 bg="#d0f0fd", fg="green").pack(pady=40)

        tk.Button(self.root, text="🔁 Play Again", font=("Arial", 16),
                  bg="#1e90ff", fg="white", command=self.start_learn_mode).pack(pady=15)

        tk.Button(self.root, text="⬅ Back to Home", font=("Arial", 16),
                  bg="#cccccc", command=self.create_main_menu).pack(pady=10)

    def play_sound(self, letter):
        try:
            if self.speaker_label:
                self.speaker_label.config(text="🔊")
                self.root.update()

            letter_index = arabic_letters.index(letter) + 1
            file_path = os.path.join(audio_path, f"{letter_index}.mp3")

            if os.path.exists(file_path):
                pygame.mixer.init()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                self.root.after(1200, lambda: self.speaker_label.config(text=""))
            else:
                self.root.after(1200, lambda: self.speaker_label.config(text=""))
        except:
            if self.speaker_label:
                self.root.after(1200, lambda: self.speaker_label.config(text=""))

    def next_learn_page(self):
        if self.learn_index < len(learn_pages) - 1:
            self.learn_index += 1
            self.show_learn_page()

    def prev_learn_page(self):
        if self.learn_index > 0:
            self.learn_index -= 1
            self.show_learn_page()

    def start_quiz_mode(self):
        self.clear_screen()
        ArabicClickPuzzle(self.root, parent=self)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ------------------- Quiz Game -------------------

class ArabicClickPuzzle:
    def __init__(self, root, parent=None):
        self.root = root
        self.parent = parent
        self.level = None
        self.buttons = []
        self.puzzles = []
        self.index = 0
        self.choice_made = False
        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Arabic Letter Puzzle", font=("Arial", 30, "bold"),
                 bg="#d0f0fd", fg="#004466").pack(pady=40)

        tk.Label(self.root, text="Choose a level to start!", font=("Arial", 20),
                 bg="#d0f0fd").pack(pady=20)

        frame = tk.Frame(self.root, bg="#d0f0fd")
        frame.pack(pady=30)

        tk.Button(frame, text="Easy (10)", font=("Arial", 18), width=12, bg="#a2d5f2",
                  command=lambda: self.start_game("easy", 10, 1)).grid(row=0, column=0, padx=15, pady=10)
        tk.Button(frame, text="Medium (20)", font=("Arial", 18), width=12, bg="#66c2f5",
                  command=lambda: self.start_game("medium", 20, 2)).grid(row=0, column=1, padx=15, pady=10)
        tk.Button(frame, text="Hard (30)", font=("Arial", 18), width=12, bg="#1e90ff", fg="white",
                  command=lambda: self.start_game("hard", 30, 3)).grid(row=0, column=2, padx=15, pady=10)

        tk.Button(self.root, text="🏠 Back to Menu", font=("Arial", 14),
                  bg="#cccccc", command=self.parent.create_main_menu).pack(pady=30)

    def start_game(self, level, count, targets_per_puzzle):
        self.level = level
        self.puzzles = self.generate_puzzles(count, targets_per_puzzle)
        self.index = 0
        self.setup_game_ui()
        self.show_puzzle()

    def generate_puzzles(self, count, num_targets):
        puzzles = []
        for _ in range(count):
            targets = random.sample(arabic_letters, num_targets)
            choices = set(targets)
            while len(choices) < max(6, num_targets + 4):
                choices.add(random.choice(arabic_letters))
            choices = list(choices)
            random.shuffle(choices)
            puzzles.append({"targets": targets, "choices": choices, "selected": set()})
        return puzzles

    def setup_game_ui(self):
        self.clear_screen()

        tk.Label(self.root, text="Arabic Letter Puzzle", font=("Arial", 24, "bold"),
                 bg="#4682b4", fg="white").pack(fill=tk.X, pady=(0, 10))

        self.instruction_var = tk.StringVar()
        self.instruction_label = tk.Label(self.root, textvariable=self.instruction_var,
                                          font=("Helvetica", 22, "bold"), bg="#d0f0fd")
        self.instruction_label.pack(pady=(10, 5))

        self.choices_frame = tk.Frame(self.root, bg="#d0f0fd")
        self.choices_frame.pack(pady=10)

        self.feedback_var = tk.StringVar()
        self.feedback_label = tk.Label(self.root, textvariable=self.feedback_var,
                                       font=("Arial", 18, "bold"), bg="#d0f0fd")
        self.feedback_label.pack(pady=12)

        nav = tk.Frame(self.root, bg="#d0f0fd")
        nav.pack(pady=10)
        tk.Button(nav, text="⟨ Previous", font=("Arial", 14),
                  command=self.prev_puzzle, width=12, bg="#b0c4de").pack(side=tk.LEFT, padx=12)
        tk.Button(nav, text="Next ⟩", font=("Arial", 14),
                  command=self.next_puzzle, width=12, bg="#20b2aa", fg="white").pack(side=tk.LEFT, padx=12)
        tk.Button(nav, text="🏠 Home", font=("Arial", 14),
                  bg="#cccccc", command=self.parent.create_main_menu).pack(side=tk.LEFT, padx=12)

        self.counter_var = tk.StringVar()
        tk.Label(nav, textvariable=self.counter_var, font=("Arial", 12),
                 bg="#d0f0fd").pack(side=tk.LEFT, padx=20)

    def show_puzzle(self):
        for w in self.choices_frame.winfo_children():
            w.destroy()
        self.feedback_var.set("")
        self.buttons = []
        self.choice_made = False

        if self.index >= len(self.puzzles):
            self.show_completion_message()
            return

        puzzle = self.puzzles[self.index]
        targets = puzzle["targets"]
        choices = puzzle["choices"]
        puzzle["selected"] = set()

        styled_targets = [f'\u2022 {t}' for t in targets]
        self.instruction_var.set("Find the letters:\n" + "   ".join(styled_targets))

        cols = 6
        for i, ch in enumerate(choices):
            color = random.choice(color_palette)
            btn = tk.Button(self.choices_frame, text=ch,
                            font=("Arial", 28, "bold"), width=4, height=2,
                            bg=color, fg="black",
                            command=lambda c=ch, b=i: self.on_choice(c, b))
            r = i // cols
            c = i % cols
            btn.grid(row=r, column=c, padx=10, pady=10)
            self.buttons.append(btn)

        self.counter_var.set(f"Puzzle {self.index + 1} / {len(self.puzzles)}")

    def on_choice(self, ch, btn_index):
        puzzle = self.puzzles[self.index]
        targets = set(puzzle["targets"])
        selected = puzzle["selected"]

        if ch in selected:
            return

        self.choice_made = True
        selected.add(ch)
        btn = self.buttons[btn_index]

        if ch in targets:
            btn.config(bg="#90ee90")
            if targets.issubset(selected):
                self.feedback_var.set("✅ Well done! You found them all!")
                self.feedback_label.config(fg="green")
                for i, choice in enumerate(puzzle["choices"]):
                    if choice in targets:
                        self.buttons[i].config(bg="#00cc66", fg="white")
        else:
            self.feedback_var.set("Think again, this could be the right answer")
            self.feedback_label.config(fg="orange")
            self.blink_correct_buttons(puzzle)

    def blink_correct_buttons(self, puzzle):
        targets = puzzle["targets"]
        for i, choice in enumerate(puzzle["choices"]):
            if choice in targets:
                self.flash_button(self.buttons[i])

    def flash_button(self, btn, color1="#00cc66", color2="#caffbf", count=3):
        def blink(count_left):
            if count_left <= 0:
                btn.config(bg=color1)
                return
            current_color = btn.cget("bg")
            next_color = color2 if current_color == color1 else color1
            btn.config(bg=next_color)
            self.root.after(200, blink, count_left - 1)

        blink(count * 2)

    def next_puzzle(self):
        if not self.choice_made:
            self.feedback_var.set("Oops! You didn't pick any letters. Please choose one.")
            self.feedback_label.config(fg="red")
            return
        if self.index < len(self.puzzles) - 1:
            self.index += 1
            self.show_puzzle()
        else:
            self.show_completion_message()

    def prev_puzzle(self):
        if self.index > 0:
            self.index -= 1
            self.show_puzzle()

    def show_completion_message(self):
        self.clear_screen()
        tk.Label(self.root, text="Alhamdulillah, This task turned out fantastic!", font=("Arial", 28, "bold"),
                 bg="#d0f0fd", fg="green").pack(pady=40)

        tk.Button(self.root, text="🔁 Play Again", font=("Arial", 16),
                  bg="#1e90ff", fg="white", command=lambda: self.start_game(self.level, len(self.puzzles), len(self.puzzles[0]['targets']))).pack(pady=15)

        tk.Button(self.root, text="⬅ Back to Quiz", font=("Arial", 16),
                  bg="#cccccc", command=self.create_welcome_screen).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# --------- Run the App ----------

if __name__ == '__main__':
    root = tk.Tk()
    app = ArabicApp(root)
    root.mainloop()
