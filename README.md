# Student Marks Manager

A simple console application built with Python and SQLite to manage student records and marks.

## Features

- Add students with name and roll number
- Add subject-wise marks (0 to 100)
- View a student's report with total, percentage and grade
- View a summary of all students
- Delete a student along with their marks

## Technologies Used

- Python 3
- SQLite (`sqlite3` module, built into Python)

## How to Run

1. Install Python 3 from [python.org](https://www.python.org/downloads/).
2. Download `student_manager.py`.
3. Open a terminal in the folder containing the file.
4. Run:

```
python student_manager.py
```

The program creates a `students.db` database file automatically on the first run.

## What I Learned

- Using SQL (CREATE TABLE, INSERT, SELECT, JOIN, DELETE) from Python
- Designing two related tables with a foreign key
- Validating user input
- Building a menu-driven console program

## Possible Improvements

- Edit existing marks
- Search students by name
- Export reports to Excel or CSV
- Add a graphical interface
