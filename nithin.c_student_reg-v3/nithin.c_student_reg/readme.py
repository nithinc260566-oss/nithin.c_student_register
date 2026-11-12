"""
readme.py
Project documentation for the Student Contact Validation & Analytics System (nithin.c_student_reg).
Run `python readme.py` (or double-click it) to view the full guide.
"""

README_TEXT = """
================================================================================
STUDENT CONTACT VALIDATION & ANALYTICS SYSTEM (nithin.c_student_reg) — README
================================================================================

1. OVERVIEW
This Python project provides an interactive 7-option CLI menu to view, search,
register, update, delete, validate, and analyze student registration records
stored in `contacts.csv` (CAI101 through CAI120).

2. PROJECT FILES (nithin.c_student_reg/)
- contacts.csv : Dataset of 20 realistic student registration records.
- validator.py : Validates student IDs, names, emails, and 10-digit Indian
                 mobile numbers via regex and length checks.
- loader.py    : Reads/writes `contacts.csv`, runs field validation, detects
                 duplicate IDs and emails, and separates `raw`, `valid`, and `rejected`.
- analytics.py : Computes rejection counts by reason, leading phone digit
                 distribution, email domain frequency, and valid course counts.
- main.py      : Interactive 7-option menu runner:
                   1. View all student records
                   2. Search record
                   3. Register student
                   4. Update student
                   5. Delete student
                   6. Analytics report
                   7. Exit
- readme.py    : Displays this documentation when executed.

3. HOW TO RUN
- Double-click `main.py` or run `python main.py` inside `nithin.c_student_reg/`.
================================================================================
"""


def print_readme() -> None:
    print(README_TEXT.strip())


if __name__ == "__main__":
    print_readme()
    try:
        input("\nPress Enter to close...")
    except EOFError:
        pass
