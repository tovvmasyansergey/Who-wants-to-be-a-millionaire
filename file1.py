"""
create by: Sergey Tovmasyan
date: 07.06.2024
"""
import random
import tkinter
from tkinter import messagebox

def read_questions(filename):
    """
    Function: read_questions
    Brief: Reads questions from a file and extracts them into a 
           list of dictionaries with questions and answers.
    Params: filename - the name of the file containing the questions
    Return: A list of dictionaries with keys 'que' for question and 'ans' for answers
    """
    with open(filename, encoding="utf-8") as ffile:
        lines = ffile.readlines()
    questions = []
    for line in lines:
        line = line.strip()
        if "?" in line:
            question = line[:line.index("?") + 1]
            answers = line[line.index("?") + 1:]
            questions.append({"que": question, "ans": answers})
    return questions

def write_result(filename, name, count):
    """
    Function: write_result
    Brief: Appends the user's name and their score to a file.
    Params: filename - the name of the file to write to
            name - the user's name
            count - the user's score
    Return: None
    """
    with open(filename, "a", encoding="utf-8") as ffile:
        ffile.write(f"{name}:{count}\n")

def open_file(filename):
    """
    Function: open_file
    Brief: Reads a file and returns a dictionary of names and scores.
    Params: filename - the name of the file to read
    Return: A dictionary with names as keys and scores as values
    """
    scores = {}
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            name, score = line.strip().split(":")
            scores[name] = int(score)
    return scores

def sort_result(scores):
    """
    Function: sort_result
    Brief: Sorts a dictionary of scores in descending order.
    Params: scores - a dictionary with names as keys and scores as values
    Return: A list of tuples sorted by score in descending order
    """
    list_sc = list(scores.items())
    list_sc.sort(key=lambda x: x[1], reverse=True)
    return list_sc

def write_result_file(filename, sorted_scores):
    """
    Function: write_result_file
    Brief: Writes sorted scores to a new file.
    Params: filename - the name of the file to write to
            sorted_scores - a list of tuples sorted by score
    Return: None
    """
    with open(filename, "w", encoding="utf-8") as ffile:
        for name, score in sorted_scores:
            ffile.write(f"{name}:{score}\n")

def show_result_window(name, score, sorted_scores):
    """
    Function: show_result_window
    Brief: Shows the result window with the user's score and the leaderboard.
    Params: name - the user's name
            score - the user's score
            sorted_scores - a list of tuples sorted by score
    Return: None
    """
    result_window = tkinter.Tk()
    result_window.title("Quiz Results")
    tkinter.Label(result_window, text=f"You scored {score} out of 10.").pack()
    if score == 10:
        tkinter.Label(result_window, text="You win!").pack()
    else:
        tkinter.Label(result_window, text="You lose.").pack()
    tkinter.Label(result_window, text="Leaderboard:").pack()
    for rank, (n, s) in enumerate(sorted_scores, 1):
        tkinter.Label(result_window, text=f"{rank}. {n}: {s}").pack()
    result_window.mainloop()
def ask_questions(name, questions, num_questions=10):
    sample_questions = random.sample(questions, k=num_questions)
    correct_count = 0
    a_5050 = True
    correct_answer = True
    phone_number = True
    answers_1 = []  # Define answers_1 here
    question_window = tkinter.Tk()
    question_window.title("Question")

    def next_question(index=0):
        nonlocal correct_answer, phone_number, correct_count, a_5050, answers_1
        if index < len(sample_questions):
            question = sample_questions[index]
            question_label.config(text=question["que"])
            answers = question["ans"].split(',')
            answers_1 = list(answers)
            random.shuffle(answers)
            for i, answer in enumerate(answers):
                answer_buttons[i].config(text=answer, state=tkinter.NORMAL, command=lambda ans=answer: check_answer(ans, question["ans"].split(',')[0], index))

            used_5050.config(state=tkinter.NORMAL if a_5050 else tkinter.DISABLED)
            used_correct_answer.config(state=tkinter.NORMAL if correct_answer else tkinter.DISABLED)
            used_phone_number.config(state=tkinter.NORMAL if phone_number else tkinter.DISABLED)
        else:
            question_window.destroy()
            write_result("point.txt", name, correct_count)
            scores = open_file("point.txt")
            sorted_scores = sort_result(scores)
            write_result_file("point1.txt", sorted_scores)
            show_result_window(name, correct_count, sorted_scores)

    def check_answer(user_answer, correct_answer, index):
        nonlocal correct_count
        if user_answer.strip().lower() == correct_answer.strip().lower():
            correct_count += 1
            messagebox.showinfo("Correct!", "You are right!")
        else:
            messagebox.showinfo("Wrong", f"The correct answer is {correct_answer}.")
        next_question(index + 1)

    def use_50(correct_ans, all_answers):
        nonlocal a_5050
        if a_5050:
            a_5050 = False
            incorrect_answers = [ans for ans in all_answers if ans.strip().lower() != correct_ans.strip().lower()]
            for btn in answer_buttons:
                if btn['text'] in incorrect_answers[:2]:
                    btn.config(state=tkinter.DISABLED)
            used_5050.config(state=tkinter.DISABLED)

    def use_call():
        nonlocal phone_number
        if phone_number:
            phone_number = False
            messagebox.showinfo("Phone a friend", "Calling a friend for help...")
        used_phone_number.config(state=tkinter.DISABLED)

    def use_correct(right_answer):
        nonlocal correct_answer
        if correct_answer:
            correct_answer = False
            messagebox.showinfo("Correct answer", f'The correct answer is: {right_answer}')
        used_correct_answer.config(state=tkinter.DISABLED)

    question_label = tkinter.Label(question_window, text="", wraplength=400)
    question_label.pack()
    answer_buttons = [tkinter.Button(question_window, text="") for _ in range(4)]
    for btn in answer_buttons:
        btn.pack(fill='x')

    used_5050 = tkinter.Button(question_window, text="50/50", command=lambda: use_50(answers_1[0], answers_1))
    used_5050.pack()
    used_correct_answer = tkinter.Button(question_window, text="Correct answer", command=lambda: use_correct(answers_1[0]))
    used_correct_answer.pack()
    used_phone_number = tkinter.Button(question_window, text="Call a friend", command=use_call)
    used_phone_number.pack()

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

name_window = tkinter.Tk()
name_window.title("Enter Name")
name_window.geometry("300x250+600+400")
tkinter.Label(name_window, text="Enter your name:").pack()
name_entry = tkinter.Entry(name_window)
name_entry.pack()
tkinter.Button(name_window, text="Start Quiz", command=get_name_and_start_quiz).pack()
name_window.mainloop()
