elif lifeline == "Next Question":
            if lifelines["Next Question"]:
                next_question(index + 1)
                lifelines["Next Question"] = False
            else:
                messagebox.showwarning("Lifeline Error", "You have already used Next Question.")

    question_label = tk.Label(question_window, text="", wraplength=400)
    question_label.pack()

    answer_buttons = [tk.Button(question_window, text="") for _ in range(4)]
    for btn in answer_buttons:
        btn.pack(fill='x')

    lifeline_buttons = {
        "50/50": tk.Button(question_window, text="50/50", command=lambda: use_lifeline("50/50", next_question.index)),
        "Show Answer": tk.Button(question_window, text="Show Answer", command=lambda: use_lifeline("Show Answer", next_question.index)),
        "Next Question": tk.Button(question_window, text="Next Question", command=lambda: use_lifeline("Next Question", next_question.index))
    }
    for btn in lifeline_buttons.values():
        btn.pack(fill='x')

    next_question()
    question_window.mainloop()

def get_name_and_start_quiz():
    name = name_entry.get()
    if name:
        name_window.destroy()
        questions = read_questions("questions.txt")
        ask_questions(name, questions)
    else:
        messagebox.showwarning("Input Error", "Please enter your name.")

name_window = tk.Tk()
name_window.title("Enter Name")
name_window.geometry("300x250+600+400")

tk.Label(name_window, text="Enter your name:").pack()
name_entry = tk.Entry(name_window)
name_entry.pack()
tk.Button(name_window, text="Start Quiz", command=get_name_and_start_quiz).pack()
name_window.mainloop()
