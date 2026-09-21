"""KAB Attendance Registry - main entry point (Student A version).

NOTE: This file is intentionally edited by BOTH students to trigger
a merge conflict (DevOps Step 3). Student A wires Roster options here,
Student B wires Reporting options in the same menu block.
"""

from roster import create_student, check_in, print_todays_summary


def main():
    while True:
        print("\n=== KAB Attendance Registry ===")
        # === MAIN MENU (shared - both students edit this block) ===
        print("1. Add student profile (Roster)")
        print("2. Check-in Present/Late (Roster)")
        print("3. View today's check-ins (Roster)")
        print("0. Exit")
        # === END MENU ===
        choice = input("Choose option: ").strip()

        if choice == "1":
            name = input("Full Name: ").strip()
            sid = input("Student ID: ").strip()
            try:
                is_new = create_student(name, sid)
                print("Profile created." if is_new else "Profile updated (ID already existed).")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "2":
            sid = input("Student ID: ").strip()
            status = input('Status (Present/Late): ').strip()
            try:
                rec = check_in(sid, status)
                print(f"Checked in {rec['student_id']} as {rec['status']} on {rec['date']}.")
            except (ValueError, KeyError) as e:
                print(f"Error: {e}")
        elif choice == "3":
            print_todays_summary()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
