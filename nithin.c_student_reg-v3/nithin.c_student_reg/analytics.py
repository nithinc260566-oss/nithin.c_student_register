"""
analytics.py
Generates statistical breakdowns for registration outcomes, phone starting digits,
email domains, and valid course enrollments from contacts.csv.
"""

import re
from collections import Counter
from loader import load_contacts, DEFAULT_CSV


def generate_analytics(filepath: str = DEFAULT_CSV) -> None:
    data = load_contacts(filepath)
    raw = data["raw"]
    valid = data["valid"]
    rejected = data["rejected"]

    print("=" * 66)
    print("STUDENT REGISTRATION & CONTACT ANALYTICS REPORT")
    print("=" * 66)
    print(f"Total Records Processed : {len(raw)}")
    print(f"Valid Registrations     : {len(valid)}")
    print(f"Rejected Registrations  : {len(rejected)}")

    # 1. Rejection Breakdown
    print("\n--- Rejection Breakdown ---")
    rejection_counts = Counter(r["rejection_category"] for r in rejected)
    for category in ["phone", "email", "name", "duplicate"]:
        print(f"  {category.capitalize():<12}: {rejection_counts.get(category, 0)}")

    print("\nRejected Record Details:")
    for r in rejected:
        print(f"  {r['student_id']} | {r['name']:<16} | {r['rejection_category'].upper():<9} | {r['rejection_reason']}")

    # 2. Phone Leading Digit Distribution (All rows)
    print("\n--- Phone Starting Digit Distribution (All Records) ---")
    digit_counts = Counter()
    for r in raw:
        digits = re.sub(r"\D", "", r.get("phone", ""))
        if digits:
            digit_counts[digits[0]] += 1

    for digit in ["9", "8", "7", "6"]:
        print(f"  Starts with {digit}: {digit_counts.get(digit, 0)}")

    # 3. Email Domain Distribution (All rows with '@')
    print("\n--- Email Domain Distribution (All Records) ---")
    domain_counts = Counter()
    for r in raw:
        email = r.get("email", "").strip().lower()
        if "@" in email:
            domain = "@" + email.split("@", 1)[1]
            domain_counts[domain] += 1

    for domain, count in domain_counts.most_common():
        print(f"  {domain:<15}: {count}")

    if domain_counts:
        top_domain, top_count = domain_counts.most_common(1)[0]
        print(f"\nTop Email Domain: {top_domain} ({top_count} records)")

    # 4. Valid Course Distribution
    print("\n--- Valid Registrations by Course ---")
    course_counts = Counter(r.get("course", "Unknown") for r in valid)
    for course, count in course_counts.most_common():
        print(f"  {course:<24}: {count}")
    print("=" * 66)


if __name__ == "__main__":
    generate_analytics()
    try:
        input("\nPress Enter to close...")
    except EOFError:
        pass
