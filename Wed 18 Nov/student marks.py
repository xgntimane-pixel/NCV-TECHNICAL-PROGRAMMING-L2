
# NCV LEVEL 4 - DAY 3
# COLLECTIONS AND RECORDS
# PROJECT: STUDENT MARKS MANAGEMENT SYSTEM

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ---------------------------------
# STEP 1: CREATE THE MAIN WINDOW
# ---------------------------------

root = tk.Tk()
root.title("Student Marks Management System")
root.geometry("850x600")
root.resizable(True, True)

root.configure(bg="#eef2f7")

# ---------------------------------
# STEP 2: STORE STUDENT RECORDS
# ---------------------------------

FILE_NAME = "student_marks.json"

students = []


def load_records():
    global students

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                students = json.load(file)
        except (json.JSONDecodeError, OSError):
            students = []


def save_records():
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


# ---------------------------------
# DISPLAY RECORDS IN THE TABLE
# ---------------------------------

def refresh_table(order_by_marks=False):

    for item in table.get_children():
        table.delete(item)

    records = students.copy()

    if order_by_marks:
        records.sort(key=lambda x: x["mark"], reverse=True)

    ranking = sorted(
        students,
        key=lambda x: x["mark"],
        reverse=True
    )

    for student in records:

        position = ranking.index(student) + 1

        table.insert(
            "",
            "end",
            iid=str(student["id"]),
            values=(
                position,
                student["name"],
                student["mark"]
            )
        )

    status_label.config(
        text=f"Total students: {len(students)}"
    )


# ---------------------------------
# STEP 3: ADD AND STORE STUDENTS
# ---------------------------------

def add_student():

    name = name_entry.get().strip()
    mark_text = mark_entry.get().strip()

    if not name or not mark_text:
        messagebox.showwarning(
            "Missing information",
            "Please enter a name and mark."
        )
        return

    try:
        mark = float(mark_text)
    except ValueError:
        messagebox.showerror(
            "Invalid mark",
            "Please enter a valid number."
        )
        return

    if not 0 <= mark <= 100:
        messagebox.showerror(
            "Invalid mark",
            "Marks must be between 0 and 100."
        )
        return

    student = {
        "id": max(
            (s["id"] for s in students),
            default=0
        ) + 1,
        "name": name,
        "mark": mark
    }

    students.append(student)

    save_records()
    refresh_table()

    name_entry.delete(0, tk.END)
    mark_entry.delete(0, tk.END)

    messagebox.showinfo(
        "Success",
        "Student record added successfully."
    )


# ---------------------------------
# STEP 4: RENAME A STUDENT
# ---------------------------------

def rename_student():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Select student",
            "Please select a student first."
        )
        return

    new_name = name_entry.get().strip()

    if not new_name:
        messagebox.showwarning(
            "Missing name",
            "Enter the new student name."
        )
        return

    student_id = int(selected[0])

    for student in students:

        if student["id"] == student_id:
            student["name"] = new_name
            break

    save_records()
    refresh_table()

    name_entry.delete(0, tk.END)

    messagebox.showinfo(
        "Updated",
        "Student name changed successfully."
    )


# ---------------------------------
# STEP 5: DELETE A STUDENT
# ---------------------------------

def delete_student():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Select student",
            "Please select a student to delete."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm deletion",
        "Are you sure you want to delete this student?"
    )

    if confirm:

        student_id = int(selected[0])

        students[:] = [
            s for s in students
            if s["id"] != student_id
        ]

        save_records()
        refresh_table()


# ---------------------------------
# STEP 6: FIND STUDENT BY NAME
# ---------------------------------

def find_student():

    search_name = name_entry.get().strip().lower()

    if not search_name:
        messagebox.showwarning(
            "Search",
            "Please enter a student name."
        )
        return

    found = False

    for student in students:

        if search_name in student["name"].lower():

            table.selection_set(str(student["id"]))
            table.focus(str(student["id"]))
            table.see(str(student["id"]))

            messagebox.showinfo(
                "Student found",
                f"Name: {student['name']}\n"
                f"Mark: {student['mark']}"
            )

            found = True
            break

    if not found:
        messagebox.showinfo(
            "Search result",
            "Student not found."
        )


# ---------------------------------
# STEP 7: CALCULATE CLASS AVERAGE
# ---------------------------------

def calculate_average():

    if len(students) == 0:
        messagebox.showwarning(
            "No records",
            "There are no student marks available."
        )
        return

    total = sum(s["mark"] for s in students)

    average = total / len(students)

    highest = max(s["mark"] for s in students)
    lowest = min(s["mark"] for s in students)

    messagebox.showinfo(
        "Class Statistics",
        f"Number of students: {len(students)}\n"
        f"Total marks: {total:.2f}\n"
        f"Class average: {average:.2f}\n"
        f"Highest mark: {highest:.2f}\n"
        f"Lowest mark: {lowest:.2f}"
    )


# ---------------------------------
# RANK STUDENTS
# ---------------------------------

def rank_students():

    if not students:
        messagebox.showwarning(
            "No records",
            "Add student records first."
        )
        return

    refresh_table(order_by_marks=True)


# ---------------------------------
# CREATE THE APPLICATION MENU
# ---------------------------------

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(
    label="Save Records",
    command=save_records
)
file_menu.add_separator()
file_menu.add_command(
    label="Exit",
    command=root.destroy
)

records_menu = tk.Menu(menu_bar, tearoff=0)
records_menu.add_command(
    label="Add Student",
    command=add_student
)
records_menu.add_command(
    label="Rename Student",
    command=rename_student
)
records_menu.add_command(
    label="Delete Student",
    command=delete_student
)
records_menu.add_command(
    label="Find Student",
    command=find_student
)

reports_menu = tk.Menu(menu_bar, tearoff=0)
reports_menu.add_command(
    label="Class Average",
    command=calculate_average
)
reports_menu.add_command(
    label="Student Ranking",
    command=rank_students
)

menu_bar.add_cascade(
    label="File",
    menu=file_menu
)
menu_bar.add_cascade(
    label="Records",
    menu=records_menu
)
menu_bar.add_cascade(
    label="Reports",
    menu=reports_menu
)

root.config(menu=menu_bar)


# ---------------------------------
# CREATE GUI TITLE
# ---------------------------------

title_label = tk.Label(
    root,
    text="STUDENT MARKS MANAGEMENT SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#eef2f7",
    fg="#17365d"
)

title_label.pack(pady=15)


# ---------------------------------
# INPUT SECTION
# ---------------------------------

input_frame = tk.LabelFrame(
    root,
    text="Student Information",
    font=("Arial", 11, "bold"),
    bg="#eef2f7",
    padx=15,
    pady=10
)

input_frame.pack(fill="x", padx=20, pady=10)

tk.Label(
    input_frame,
    text="Student Name:",
    bg="#eef2f7"
).grid(row=0, column=0, padx=5, pady=8)

name_entry = tk.Entry(
    input_frame,
    width=25
)
name_entry.grid(row=0, column=1, padx=5)


tk.Label(
    input_frame,
    text="Student Mark:",
    bg="#eef2f7"
).grid(row=0, column=2, padx=5)

mark_entry = tk.Entry(
    input_frame,
    width=15
)
mark_entry.grid(row=0, column=3, padx=5)


# ---------------------------------
# ACTION BUTTONS
# ---------------------------------

button_frame = tk.Frame(
    root,
    bg="#eef2f7"
)

button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add Student",
    width=15,
    command=add_student,
    bg="#198754",
    fg="white"
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Rename",
    width=12,
    command=rename_student
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Delete",
    width=12,
    command=delete_student,
    bg="#dc3545",
    fg="white"
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Find Student",
    width=15,
    command=find_student
).grid(row=0, column=3, padx=5)


# ---------------------------------
# STUDENT RECORD TABLE
# ---------------------------------

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("rank", "name", "mark")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)

table.heading("rank", text="Position")
table.heading("name", text="Student Name")
table.heading("mark", text="Mark")

table.column("rank", width=100, anchor="center")
table.column("name", width=350)
table.column("mark", width=150, anchor="center")

table.pack(fill="both", expand=True)


# ---------------------------------
# REPORT BUTTONS
# ---------------------------------

report_frame = tk.Frame(
    root,
    bg="#eef2f7"
)

report_frame.pack(pady=10)

tk.Button(
    report_frame,
    text="Class Average & Statistics",
    width=25,
    command=calculate_average
).grid(row=0, column=0, padx=10)

tk.Button(
    report_frame,
    text="Rank Students",
    width=20,
    command=rank_students
).grid(row=0, column=1, padx=10)


# ---------------------------------
# STATUS BAR
# ---------------------------------

status_label = tk.Label(
    root,
    text="Total students: 0",
    anchor="w",
    bg="#17365d",
    fg="white",
    padx=10
)

status_label.pack(fill="x", side="bottom")


# ---------------------------------
# START THE PROGRAM
# ---------------------------------

load_records()
refresh_table()

root.mainloop()
