"""
validator.py
Field-level validation rules for student IDs, names, emails, and 10-digit phone numbers.
"""

import re

ID_REGEX = re.compile(r"^CAI\d{3,}$", re.IGNORECASE)
NAME_REGEX = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,59}$")
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_student_id(student_id: str) -> tuple[bool, str]:
    if not student_id or not ID_REGEX.match(student_id.strip()):
        return False, "Student ID must follow format CAI### (e.g., CAI121)"
    return True, ""


def validate_name(name: str) -> tuple[bool, str]:
    if not name or not NAME_REGEX.match(name.strip()):
        return False, "Invalid name format (letters, spaces, dots, hyphens only)"
    return True, ""


def validate_email(email: str) -> tuple[bool, str]:
    if not email or not EMAIL_REGEX.match(email.strip()):
        return False, "Invalid email format"
    return True, ""


def validate_phone(phone: str) -> tuple[bool, str]:
    digits = re.sub(r"\D", "", str(phone or ""))
    if len(digits) != 10:
        return False, f"Phone must have 10 digits (got {len(digits)})"
    if digits[0] not in {"6", "7", "8", "9"}:
        return False, f"Invalid starting digit: {digits[0]} (must start with 6, 7, 8, or 9)"
    return True, ""


def validate_student(record: dict) -> tuple[bool, str, str]:
    """
    Validates a single student registration record.
    Returns: (is_valid, category, reason)
    Categories: 'valid', 'name', 'email', 'phone'
    """
    ok_name, msg_name = validate_name(record.get("name", ""))
    if not ok_name:
        return False, "name", msg_name

    ok_email, msg_email = validate_email(record.get("email", ""))
    if not ok_email:
        return False, "email", msg_email

    ok_phone, msg_phone = validate_phone(record.get("phone", ""))
    if not ok_phone:
        return False, "phone", msg_phone

    return True, "valid", "Valid record"


if __name__ == "__main__":
    sample = {"name": "Aarav Sharma", "email": "aarav.sharma@gmail.com", "phone": "9845012341"}
    print("Sample validation check:", validate_student(sample))
    try:
        input("\nPress Enter to close...")
    except EOFError:
        pass
