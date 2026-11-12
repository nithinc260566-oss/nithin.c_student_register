"""
main.py
Interactive 7-option CLI for Student Registration & Contact Management (nithin.c_student_reg).
Options:
  1. View all student records
  2. Search record
  3. Register student
  4. Update student
  5. Delete student
  6. Analytics report
  7. Exit
"""

from loader import load_contacts, save_raw_contacts, DEFAULT_CSV
from validator import validate_student_id, validate_name, validate_email, validate_phone
from analytics import generate_analytics


def print_records_table(records: list[dict], title: str = "STUDENT RECORDS") -> None:
    print("\n" + "=" * 96)
    print(f"{title} ({len(records)} records)")
    print("=" * 96)
    if not records:
        print("No records found.")
        print("=" * 96)
        return

    header = f"{'ID':<8} | {'Name':<18} | {'Email':<28} | {'Phone':<12} | {'Course':<22}"
    print(header)
    print("-" * 96)
    for r in records:
        print(
            f"{r.get('student_id', ''):<8} | "
            f"{r.get('name', ''):<18} | "
            f"{r.get('email', ''):<28} | "
            f"{r.get('phone', ''):<12} | "
            f"{r.get('course', ''):<22}"
        )
    print("=" * 96)


def view_all_records(filepath: str = DEFAULT_CSV) -> None:
    data = load_contacts(filepath)
    print("\nView Mode:")
    print("  [A] All student records in CSV")
    print("  [V] Validated student records only")
    print("  [R] Rejected student records only")
    sub = input("Choose [A/V/R] (default A): ").strip().upper() or "A"

    if sub == "V":
        print_records_table(data["valid"], "VALID STUDENT RECORDS")
    elif sub == "R":
        print("\n" + "=" * 105)
        print(f"REJECTED STUDENT RECORDS ({len(data['rejected'])} records)")
        print("=" * 105)
        for r in data["rejected"]:
            print(
                f"{r['student_id']:<8} | {r['name']:<16} | {r['email']:<25} | "
                f"{r['phone']:<11} | [{r['rejection_category'].upper()}] {r['rejection_reason']}"
            )
        print("=" * 105)
    else:
        print_records_table(data["raw"], "ALL STUDENT RECORDS")


def search_record(filepath: str = DEFAULT_CSV) -> None:
    query = input("\nEnter Student ID, Name, Email, Phone, or Course to search: ").strip().lower()
    if not query:
        print("Search query cannot be empty.")
        return

    data = load_contacts(filepath)
    matches = [
        r for r in data["raw"]
        if query in r.get("student_id", "").lower()
        or query in r.get("name", "").lower()
        or query in r.get("email", "").lower()
        or query in r.get("phone", "").lower()
        or query in r.get("course", "").lower()
    ]
    print_records_table(matches, f"SEARCH RESULTS FOR '{query}'")


def register_student(filepath: str = DEFAULT_CSV) -> None:
    print("\n--- Register Student ---")
    data = load_contacts(filepath)
    raw = data["raw"]
    existing_ids = {r.get("student_id", "").upper() for r in raw}
    valid_emails = {r.get("email", "").lower() for r in data["valid"]}

    student_id = input("Student ID (e.g., CAI121): ").strip().upper()
    ok_id, msg_id = validate_student_id(student_id)
    if not ok_id:
        print(f"Registration failed: {msg_id}")
        return
    if student_id in existing_ids:
        print(f"Registration failed: Student ID '{student_id}' already exists.")
        return

    name = input("Full Name: ").strip()
    ok_name, msg_name = validate_name(name)
    if not ok_name:
        print(f"Registration failed: {msg_name}")
        return

    email = input("Email Address: ").strip()
    ok_email, msg_email = validate_email(email)
    if not ok_email:
        print(f"Registration failed: {msg_email}")
        return
    if email.lower() in valid_emails:
        print(f"Registration failed: Email '{email}' is already registered.")
        return

    phone = input("10-Digit Phone Number: ").strip()
    ok_phone, msg_phone = validate_phone(phone)
    if not ok_phone:
        print(f"Registration failed: {msg_phone}")
        return

    course = input("Course Name: ").strip()
    if not course:
        print("Registration failed: Course cannot be empty.")
        return

    new_record = {
        "student_id": student_id,
        "name": name,
        "email": email,
        "phone": phone,
        "course": course,
    }
    raw.append(new_record)
    save_raw_contacts(raw, filepath)
    print(f"Success! Student {student_id} ({name}) has been registered.")


def update_student(filepath: str = DEFAULT_CSV) -> None:
    print("\n--- Update Student ---")
    target_id = input("Enter Student ID to update (e.g., CAI101): ").strip().upper()
    if not target_id:
        print("Student ID cannot be empty.")
        return

    data = load_contacts(filepath)
    raw = data["raw"]
    target_idx = next((i for i, r in enumerate(raw) if r.get("student_id", "").upper() == target_id), None)

    if target_idx is None:
        print(f"No student found with ID '{target_id}'.")
        return

    current = raw[target_idx]
    print(f"Current Record: {current}")
    print("(Press Enter to keep existing value)")

    new_name = input(f"New Name [{current['name']}]: ").strip() or current["name"]
    ok_name, msg_name = validate_name(new_name)
    if not ok_name:
        print(f"Update aborted: {msg_name}")
        return

    new_email = input(f"New Email [{current['email']}]: ").strip() or current["email"]
    ok_email, msg_email = validate_email(new_email)
    if not ok_email:
        print(f"Update aborted: {msg_email}")
        return

    other_valid_emails = {
        r.get("email", "").lower()
        for r in data["valid"]
        if r.get("student_id", "").upper() != target_id
    }
    if new_email.lower() in other_valid_emails:
        print(f"Update aborted: Email '{new_email}' is already used by another student.")
        return

    new_phone = input(f"New Phone [{current['phone']}]: ").strip() or current["phone"]
    ok_phone, msg_phone = validate_phone(new_phone)
    if not ok_phone:
        print(f"Update aborted: {msg_phone}")
        return

    new_course = input(f"New Course [{current['course']}]: ").strip() or current["course"]

    raw[target_idx] = {
        "student_id": current["student_id"],
        "name": new_name,
        "email": new_email,
        "phone": new_phone,
        "course": new_course,
    }
    save_raw_contacts(raw, filepath)
    print(f"Success! Record {target_id} updated.")


def delete_student(filepath: str = DEFAULT_CSV) -> None:
    print("\n--- Delete Student ---")
    target_id = input("Enter Student ID to delete (e.g., CAI120): ").strip().upper()
    if not target_id:
        print("Student ID cannot be empty.")
        return

    data = load_contacts(filepath)
    raw = data["raw"]
    target = next((r for r in raw if r.get("student_id", "").upper() == target_id), None)

    if target is None:
        print(f"No student found with ID '{target_id}'.")
        return

    confirm = input(f"Are you sure you want to delete {target_id} ({target['name']})? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return

    updated = [r for r in raw if r.get("student_id", "").upper() != target_id]
    save_raw_contacts(updated, filepath)
    print(f"Success! Student {target_id} deleted from contacts.csv.")


def run_menu() -> None:
    while True:
        print("\n" + "=" * 54)
        print("  STUDENT REGISTRATION SYSTEM (nithin.c_student_reg)")
        print("=" * 54)
        print("  1. View all student records")
        print("  2. Search record")
        print("  3. Register student")
        print("  4. Update student")
        print("  5. Delete student")
        print("  6. Analytics report")
        print("  7. Exit")
        print("=" * 54)

        try:
            choice = input("Enter your choice (1-7): ").strip()
        except EOFError:
            break

        if choice == "1":
            view_all_records()
        elif choice == "2":
            search_record()
        elif choice == "3":
            register_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            generate_analytics()
        elif choice == "7":
            print("Exiting Student Registration System. Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    run_menu()
