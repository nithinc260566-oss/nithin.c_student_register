"""
loader.py
Batch CSV loader, CRUD persistence helpers, and duplicate ID/email detection.
"""

import csv
import os
from validator import validate_student

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(BASE_DIR, "contacts.csv")
FIELDNAMES = ["student_id", "name", "email", "phone", "course"]


def load_contacts(filepath: str = DEFAULT_CSV) -> dict:
    """
    Loads contacts from contacts.csv, runs field validation and duplicate detection,
    and returns structured valid/rejected records along with raw rows.
    """
    raw_records = []
    valid_records = []
    rejected_records = []

    seen_ids = set()
    seen_emails = set()

    with open(filepath, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {k: (v.strip() if v is not None else "") for k, v in row.items()}
            raw_records.append(cleaned)

            is_valid, category, reason = validate_student(cleaned)
            if not is_valid:
                rejected_records.append({
                    **cleaned,
                    "rejection_category": category,
                    "rejection_reason": reason,
                })
                continue

            student_id = cleaned.get("student_id", "").upper()
            email_lower = cleaned.get("email", "").lower()

            if student_id in seen_ids:
                rejected_records.append({
                    **cleaned,
                    "rejection_category": "duplicate",
                    "rejection_reason": f"Duplicate student ID ({student_id})",
                })
                continue

            if email_lower in seen_emails:
                rejected_records.append({
                    **cleaned,
                    "rejection_category": "duplicate",
                    "rejection_reason": f"Email address already exists ({cleaned.get('email')})",
                })
                continue

            seen_ids.add(student_id)
            seen_emails.add(email_lower)
            valid_records.append(cleaned)

    return {
        "raw": raw_records,
        "valid": valid_records,
        "rejected": rejected_records,
    }


def save_raw_contacts(records: list[dict], filepath: str = DEFAULT_CSV) -> None:
    """Writes the updated list of student records back to contacts.csv."""
    with open(filepath, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for rec in records:
            writer.writerow({field: rec.get(field, "").strip() for field in FIELDNAMES})


if __name__ == "__main__":
    data = load_contacts()
    print(f"Total Records : {len(data['raw'])}")
    print(f"Valid Records : {len(data['valid'])}")
    print(f"Rejected      : {len(data['rejected'])}")
    for item in data["rejected"]:
        print(f"  - {item['student_id']} ({item['name']}): [{item['rejection_category'].upper()}] {item['rejection_reason']}")
    try:
        input("\nPress Enter to close...")
    except EOFError:
        pass
