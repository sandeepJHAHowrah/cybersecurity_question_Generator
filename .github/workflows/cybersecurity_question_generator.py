import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests

class SandeepCyberSecurityAwarenessProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("Sandeep CyberSecurity Awareness Program")

        self.assessor_email = "sandeep.a.jha@gmail.com"
        self.name_var = tk.StringVar()
        self.emp_id_var = tk.StringVar()
        self.question_set_var = tk.StringVar()
        self.questions = []

        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry Widgets
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(self.root, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Employee ID:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(self.root, textvariable=self.emp_id_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Question Set Level:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        level_choices = ["Naive", "Basic", "Advanced", "God Level"]
        level_dropdown = ttk.Combobox(self.root, textvariable=self.question_set_var, values=level_choices)
        level_dropdown.grid(row=2, column=1, padx=10, pady=5)
        level_dropdown.set("Naive")

        # Submit Button
        submit_button = tk.Button(self.root, text="Submit", command=self.submit_answers)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def fetch_questions(self, difficulty):
        url = f"https://opentdb.com/api.php?amount=10&category=18&difficulty={difficulty}&type=multiple"
        response = requests.get(url)
        data = response.json()

        if data["response_code"] == 0:
            return data["results"]
        else:
            messagebox.showerror("Error", "Failed to fetch questions. Please try again.")
            return []

    def submit_answers(self):
        name = self.name_var.get()
        emp_id = self.emp_id_var.get()
        question_set_level = self.question_set_var.get()

        if not name or not emp_id:
            messagebox.showwarning("Warning", "Please enter Name and Employee ID.")
            return

        self.questions = self.fetch_questions(self.map_level_to_difficulty(question_set_level))

        if not self.questions:
            return

        # Display questions and get answers from the user
        answers = []
        for i, question in enumerate(self.questions, start=1):
            answer = self.display_question(i, question)
            if answer is None:
                return
            answers.append(answer)

        # Calculate and display the result
        correct_answers = sum(1 for user_ans, correct_ans in zip(answers, [q["correct_answer"] for q in self.questions]) if user_ans == correct_ans)
        total_questions = len(self.questions)

        result_message = f"Dear {name},\n\nYou have scored {correct_answers}/{total_questions} in the {question_set_level} CyberSecurity Awareness Program."

        messagebox.showinfo("Result", result_message)

        # Mail the result to the assessor's email address (not implemented in this example)

    def display_question(self, question_number, question_data):
        question_text = question_data["question"]
        options = [question_data["correct_answer"]] + question_data["incorrect_answers"]
        options = [option.encode('latin1').decode('utf-8') for option in options]  # Convert HTML entities

        user_answer = tk.StringVar()

        question_window = tk.Toplevel(self.root)
        question_window.title(f"Question {question_number}")
        tk.Label(question_window, text=f"Q{question_number}: {question_text}", wraplength=400, justify="left").pack(padx=10, pady=10)

        for i, option in enumerate(options, start=1):
            tk.Radiobutton(question_window, text=option, variable=user_answer, value=option).pack(pady=5)

        submit_button = tk.Button(question_window, text="Submit", command=question_window.destroy)
        submit_button.pack(pady=10)

        question_window.wait_window(question_window)

        return user_answer.get()

    def map_level_to_difficulty(self, level):
        difficulty_mapping = {"Naive": "easy", "Basic": "medium", "Advanced": "hard", "God Level": "hard"}
        return difficulty_mapping.get(level, "easy")

if __name__ == "__main__":
    root = tk.Tk()
    app = SandeepCyberSecurityAwarenessProgram(root)
    root.mainloop()
