import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import json

# setup
root = tk.Tk()
root.title("Biology Quiz")
root.geometry("650x650")
root.resizable(width=False, height=False)
root.configure(bg="AliceBlue")

# load the questions file

with open("geneticsquiz.json") as file:
    obj = json.load(file)
questions_genetics = (obj["questions_gen"])
options_genetics = (obj["options_gen"])
answers_genetics = (obj["answers_gen"])

# initialize the score and question number
current_question_number = 0
final_score = 0


def load_question(num):
    """Displays the current question. """
    lbl_current_question = tk.Label(questions_frame,
                                    text=questions_genetics[num],
                                    font=("Calibre", 18, "bold"),
                                    background="AliceBlue")
    lbl_current_question.pack(pady=20, padx=50, anchor=tk.W)

    return num


def enable_next_button():
    """ Enables the Next button if an answer to the current question is chosen"""
    btn_next.configure(state="normal")
    if current_question_number == (len(questions_genetics) - 1):
        pr_bar["value"] = 100
        btn_next.configure(command=display_result, text="Results", state="normal")


def load_buttons(qnum):
    """Displays the answer options for the current questions."""
    global chosen_option
    chosen_option = tk.IntVar(value=0)
    for i in range(len(options_genetics[qnum])):
        op1 = tk.Radiobutton(questions_frame, text=options_genetics[qnum][i],
                             background="AliceBlue",
                             font=("Calibre", 14),
                             activebackground="LightSteelBlue1",
                             variable=chosen_option,
                             value=i + 1,
                             command=enable_next_button

                             )
        op1.pack(anchor=tk.W, padx=80)
    return qnum


def check_answer(qnum):
    """Checks if the chosen answer is correct."""
    if chosen_option.get() == answers_genetics[qnum]:
        return True


def next_question():
    """ Alters the score and modifies the current question number and disables the Next button."""

    global final_score
    global current_question_number

    pr_bar["value"] += 20

    if check_answer(current_question_number):
        final_score += 1
    if current_question_number < (len(questions_genetics) - 1):
        btn_next.configure(state="disabled")
        current_question_number += 1
        for child in questions_frame.winfo_children():
            child.pack_forget()
        load_question(current_question_number)
        load_buttons(current_question_number)


def retake_quiz():
    """ Sets the score, the question number and the progressbar value to 0.
    Displays the instruction, the progressbar, the question frame and the buttons again. """

    global current_question_number
    current_question_number = 0

    global final_score
    final_score = 0

    instruction_label.pack(anchor="center", padx=10, pady=10)
    pr_bar.pack()
    pr_bar["value"] = 0

    results_frame.pack_forget()
    btn_retake_quiz.pack_forget()

    questions_frame.pack(pady=20, padx=20, ipadx=20, ipady=20, fill="both")
    for child in questions_frame.winfo_children():
        child.pack_forget()
    load_question(current_question_number)
    load_buttons(current_question_number)
    btn_next.configure(text="Next", command=next_question)
    button_frame.pack()


def score_message(current_score):
    """Checks the score and returns a message to the user based on the score. """
    if current_score < 80:
        return "Revise the material and retake the quiz. You can do it!"
    elif 80 <= current_score < 100:
        return "You passed the test! Good job!"
    else:
        return "Perfect score! You passed the test!"


#
def display_result():
    """ Displays the final score and a Retake Quiz button. """

    global final_score

    if check_answer(current_question_number):
        final_score += 1

    final_score = round(final_score * (100/len(questions_genetics)))


    results_frame.pack()
    btn_retake_quiz.pack()
    lbl_results.configure(text=f"Your final score is {final_score}%.\n{score_message(final_score)}")

    questions_frame.pack_forget()
    button_frame.pack_forget()
    instruction_label.pack_forget()
    pr_bar.pack_forget()


def want_to_quit():
    """ Asks for confirmation if the Quit button is pressed. """
    answer = tkinter.messagebox.askyesno(title="Confirmation",
                                         message="Are you sure you want to quit "
                                                 "your exam?")
    if answer:
        display_result()


# heading

heading_frame = tk.Frame(root, background="AliceBlue")
heading_frame.pack()

quiz_name_label = tk.Label(heading_frame, text="Genetics Quiz",
                           font=("Calibre", 25, "bold"),
                           background="AliceBlue")
quiz_name_label.pack(anchor="center", padx=10, pady=10)
instruction_label = tk.Label(heading_frame,
                             text="Read each question carefully and choose"
                                  " the correct answer.\n"
                                  "When you are done with the quiz, "
                                  "you will be able to see your score. Good luck!",
                             font=("Calibre", 12, "italic"),
                             background="AliceBlue")
instruction_label.pack(anchor="center", padx=10, pady=10)

# progress bar

pr_bar = ttk.Progressbar(heading_frame, orient="horizontal",
                         length=600, mode="determinate")
pr_bar.pack()

# question frame

questions_frame = tk.Frame(root,
                           background="AliceBlue",
                           borderwidth=5,
                           relief="ridge",
                           width=610, height=250)

questions_frame.pack(pady=20, padx=20, ipadx=20, ipady=20)
questions_frame.pack_propagate(0)

# button frame

button_frame = tk.Frame(root, background="AliceBlue")
button_frame.pack()

# button Next


btn_next = tk.Button(button_frame, text="Next Question",
                     font=("Calibre", 18, "bold"),
                     background="LightSteelBlue1", state="disabled")
btn_next.configure(height=1, width=15, activebackground="LightBlue3", command=next_question)
btn_next.pack(padx=20, pady=15)

load_question(current_question_number)
load_buttons(current_question_number)

# results frame
results_frame = tk.Frame(root, background="AliceBlue")

lbl_results = tk.Label(results_frame, text="",
                       background="AliceBlue",
                       font=("Calibre", 14),
                       height=13)

lbl_results.pack(anchor="center", ipady=50, ipadx=10)

btn_retake_quiz = tk.Button(text="Retake Exam",
                            font=("Calibre", 18, "bold"),
                            background="LightSteelBlue1",
                            command=retake_quiz,
                            activebackground="LightBlue3")

# button quit
btn_quit = tk.Button(button_frame, text="Quit Exam",
                     font=("Calibre", 18, "bold"),
                     background="LightSteelBlue1", command=want_to_quit)
btn_quit.configure(height=1, width=15, activebackground="LightBlue3")

btn_quit.pack(padx=20, pady=10)

root.mainloop()
