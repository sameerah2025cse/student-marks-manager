"""Student Marks Manager
A simple console app using Python and SQLite.
Features: add students, add marks, view reports, delete students.
"""

import sqlite3

DB_NAME = "students.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            mark INTEGER NOT NULL CHECK (mark BETWEEN 0 AND 100),
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()


def get_grade(percentage):
    if percentage >= 90:
        return "O"
    if percentage >= 80:
        return "A+"
    if percentage >= 70:
        return "A"
    if percentage >= 60:
        return "B+"
    if percentage >= 50:
        return "B"
    return "RA (Re-appear)"


def ask_number(prompt, low, high):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and low <= int(value) <= high:
            return int(value)
        print(f"Please enter a number between {low} and {high}.")


def add_student(conn):
    name = input("Student name: ").strip()
    roll_no = input("Roll number: ").strip()
    if not name or not roll_no:
        print("Name and roll number cannot be empty.")
        return
    try:
        conn.execute(
            "INSERT INTO students (name, roll_no) VALUES (?, ?)", (name, roll_no)
        )
        conn.commit()
        print("Student added.")
    except sqlite3.IntegrityError:
        print("That roll number already exists.")


def find_student(conn, roll_no):
    return conn.execute(
        "SELECT id, name FROM students WHERE roll_no = ?", (roll_no,)
    ).fetchone()


def add_marks(conn):
    roll_no = input("Roll number of the student: ").strip()
    student = find_student(conn, roll_no)
    if student is None:
        print("No student found with that roll number.")
        return
    student_id, name = student
    print(f"Adding marks for {name}. Leave the subject empty to stop.")
    while True:
        subject = input("Subject: ").strip()
        if not subject:
            break
        mark = ask_number("Mark (0-100): ", 0, 100)
        conn.execute(
            "INSERT INTO marks (student_id, subject, mark) VALUES (?, ?, ?)",
            (student_id, subject, mark),
        )
        conn.commit()
        print("Mark saved.")


def view_student(conn):
    roll_no = input("Roll number of the student: ").strip()
    student = find_student(conn, roll_no)
    if student is None:
        print("No student found with that roll number.")
        return
    student_id, name = student
    rows = conn.execute(
        "SELECT subject, mark FROM marks WHERE student_id = ?", (student_id,)
    ).fetchall()
    print(f"\nReport for {name} ({roll_no})")
    print("-" * 30)
    if not rows:
        print("No marks added yet.")
        return
    for subject, mark in rows:
        print(f"{subject:<20} {mark:>5}")
    total = sum(mark for _, mark in rows)
    percentage = total / len(rows)
    print("-" * 30)
    print(f"Total: {total} / {len(rows) * 100}")
    print(f"Percentage: {percentage:.2f}%")
    print(f"Grade: {get_grade(percentage)}")


def view_all(conn):
    rows = conn.execute(
        """
        SELECT s.roll_no, s.name, COUNT(m.id), COALESCE(AVG(m.mark), 0)
        FROM students s
        LEFT JOIN marks m ON m.student_id = s.id
        GROUP BY s.id
        ORDER BY s.roll_no
        """
    ).fetchall()
    if not rows:
        print("No students yet.")
        return
    print(f"\n{'Roll No':<12}{'Name':<20}{'Subjects':<10}{'Average':>8}")
    print("-" * 50)
    for roll_no, name, count, average in rows:
        print(f"{roll_no:<12}{name:<20}{count:<10}{average:>8.2f}")


def delete_student(conn):
    roll_no = input("Roll number to delete: ").strip()
    student = find_student(conn, roll_no)
    if student is None:
        print("No student found with that roll number.")
        return
    sure = input(f"Delete {student[1]} and all marks? (yes/no): ").strip().lower()
    if sure == "yes":
        conn.execute("DELETE FROM students WHERE id = ?", (student[0],))
        conn.commit()
        print("Deleted.")
    else:
        print("Cancelled.")


def main():
    conn = connect()
    create_tables(conn)
    actions = {
        "1": add_student,
        "2": add_marks,
        "3": view_student,
        "4": view_all,
        "5": delete_student,
    }
    while True:
        print("\n=== Student Marks Manager ===")
        print("1. Add student")
        print("2. Add marks")
        print("3. View one student's report")
        print("4. View all students")
        print("5. Delete a student")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(conn)
        else:
            print("Invalid option, try again.")
    conn.close()


if __name__ == "__main__":
    main()
