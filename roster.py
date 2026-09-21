"""Student A: Roster & Check-In Module.

Handles student identities and daily presence.
Data file: attendance_log.json
Format:
{
  "students": {
    "<Student ID>": {
      "name": "<Full Name>",
      "records": {"YYYY-MM-DD": "Present" | "Late" | "Absent"}
    }
  }
}
"""

import json
import os
from datetime import date, datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "attendance_log.json")


def load_data():
    if not os.path.exists(LOG_FILE):
        return {"students": {}}
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"students": {}}
    if "students" not in data:
        data = {"students": {}}
    return data


def save_data(data):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def create_student(name, student_id):
    """Create a student profile (Name, Student ID)."""
    name = name.strip()
    student_id = student_id.strip()
    if not name or not student_id:
        raise ValueError("Name and Student ID are required.")
    data = load_data()
    students = data["students"]
    if student_id in students:
        # Update name if re-registered (keep records)
        students[student_id]["name"] = name
        save_data(data)
        return False  # already existed
    students[student_id] = {"name": name, "records": {}}
    save_data(data)
    return True


def check_in(student_id, status, day=None):
    """Log a timestamped 'Present' or 'Late' status for a student."""
    status = status.strip().capitalize()
    if status not in ("Present", "Late"):
        raise ValueError("Status must be 'Present' or 'Late'. Use reporting module for 'Absent'.")
    student_id = student_id.strip()
    data = load_data()
    students = data["students"]
    if student_id not in students:
        raise KeyError(f"Student ID '{student_id}' not found. Create profile first.")
    day = day or date.today().isoformat()
    # Validate date format
    datetime.fromisoformat(day)
    students[student_id]["records"][day] = status
    save_data(data)
    return {"student_id": student_id, "date": day, "status": status}


def get_todays_checkins(day=None):
    """Return list of all students checked in today (Present/Late)."""
    day = day or date.today().isoformat()
    data = load_data()
    result = []
    for sid, info in data["students"].items():
        status = info.get("records", {}).get(day)
        if status in ("Present", "Late"):
            result.append({"student_id": sid, "name": info["name"], "status": status})
    return result


def print_todays_summary(day=None):
    """Display a simple list of all students checked in today."""
    day = day or date.today().isoformat()
    rows = get_todays_checkins(day)
    print(f"\n--- Checked in on {day}: {len(rows)} student(s) ---")
    if not rows:
        print("No check-ins yet today.")
        return
    for r in rows:
        print(f"{r['student_id']} | {r['name']} | {r['status']}")
