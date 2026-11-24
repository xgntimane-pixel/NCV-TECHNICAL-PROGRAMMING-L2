"""PRACTICAL 3: STUDENT ATTENDANCE - JSON file (Thonny)."""
import json

# ============================================================
# SECTION 1: VALIDATE A JSON STUDENT RECORD
# ============================================================
def check_student(student, seen_ids):
    if type(student) is not dict:
        return "Student record must be a JSON object"
    required_fields = ["student_id", "name", "sessions_total",
                       "sessions_attended", "late_submissions"]
    for field in required_fields:
        if field not in student:
            return "Missing field: " + field
    if type(student["student_id"]) is not str or student["student_id"].strip() == "":
        return "Invalid student ID"
    if type(student["name"]) is not str or student["name"].strip() == "":
        return "Invalid student name"
    if student["student_id"] in seen_ids:
        return "Duplicate student ID"
    total = student["sessions_total"]
    attended = student["sessions_attended"]
    late = student["late_submissions"]
    if type(total) is not int or type(attended) is not int or type(late) is not int:
        return "Attendance and late submissions must be whole numbers"
    if total <= 0 or attended < 0 or attended > total or late < 0:
        return "Attendance or late submission values are out of range"
    return ""


# ============================================================
# SECTION 2: CALCULATE RISK USING IF / ELIF / ELSE
# ============================================================
def calculate_risk(attendance_percent, late_submissions):
    if attendance_percent < 60 or late_submissions >= 5:
        return "HIGH"
    elif attendance_percent < 75 or late_submissions >= 3:
        return "MEDIUM"
    else:
        return "LOW"


# ============================================================
# SECTION 3: SORT BY ATTENDANCE (LOWEST FIRST)
# ============================================================
def sort_by_attendance(students):
    i = 0
    while i < len(students):
        smallest = i
        j = i + 1
        while j < len(students):
            first = students[j]
            second = students[smallest]
            if first["attendance_percent"] < second["attendance_percent"]:
                smallest = j
            elif first["attendance_percent"] == second["attendance_percent"]:
                if first["late_submissions"] > second["late_submissions"]:
                    smallest = j
            j += 1
        students[i], students[smallest] = students[smallest], students[i]
        i += 1


# ============================================================
# SECTION 4: READ THE JSON FILE
# ============================================================
def main():
    try:
        with open("attendance.json", "r", encoding="utf-8") as input_file:
            input_records = json.load(input_file)
    except FileNotFoundError:
        print("ERROR: Put attendance.json in the program's folder.")
        return
    except json.JSONDecodeError:
        print("ERROR: The JSON file contains invalid JSON syntax.")
        return
    if type(input_records) is not list:
        print("ERROR: The JSON file must contain a list of students.")
        return

    # ========================================================
    # SECTION 5: VALIDATE AND CLASSIFY STUDENTS
    # ========================================================
    clean_students = []
    errors = []
    seen_ids = {}  # Dictionary used to detect duplicate student IDs.
    record_number = 0
    high_count = 0
    medium_count = 0
    low_count = 0
    for student in input_records:
        record_number += 1
        reason = check_student(student, seen_ids)
        if reason != "":
            errors.append("Record " + str(record_number) + ": " + reason)
            continue
        seen_ids[student["student_id"]] = True
        percent = 100 * student["sessions_attended"] / student["sessions_total"]
        risk = calculate_risk(percent, student["late_submissions"])
        student["attendance_percent"] = percent
        student["risk"] = risk
        clean_students.append(student)
        if risk == "HIGH":
            high_count += 1
        elif risk == "MEDIUM":
            medium_count += 1
        else:
            low_count += 1
    sort_by_attendance(clean_students)

    # ========================================================
    # SECTION 6: SAVE CLEAN JSON AND ERROR LOG
    # ========================================================
    with open("attendance_clean.json", "w", encoding="utf-8") as clean_file:
        json.dump(clean_students, clean_file, indent=2)
    with open("attendance_errors.log", "w", encoding="utf-8") as error_file:
        for error in errors:
            error_file.write(error + "\n")

    # ========================================================
    # SECTION 7: WRITE THE SUMMARY REPORT
    # ========================================================
    accepted_count = 0
    for student in clean_students:
        accepted_count += 1
    rejected_count = 0
    for error in errors:
        rejected_count += 1
    with open("attendance_report.txt", "w", encoding="utf-8") as report:
        report.write("STUDENT ATTENDANCE EARLY WARNING\n")
        report.write(f"Accepted: {accepted_count} | Rejected: {rejected_count}\n")
        report.write(f"HIGH: {high_count}\nMEDIUM: {medium_count}\nLOW: {low_count}\n")
        report.write("\n10 LOWEST ATTENDANCE RECORDS\n")
        count = 0
        for student in clean_students:
            if count == 10:
                break
            count += 1
            report.write(f'{student["student_id"]} {student["name"]}: '
                         f'{student["attendance_percent"]:.1f}% ({student["risk"]})\n')

    # ========================================================
    # SECTION 8: DISPLAY THE SUMMARY
    # ========================================================
    print("STUDENT ATTENDANCE PROCESSOR")
    print("Accepted:", accepted_count, "Rejected:", rejected_count)
    print("HIGH:", high_count, "MEDIUM:", medium_count, "LOW:", low_count)
    print("Files created: attendance_clean.json, attendance_errors.log, attendance_report.txt")


# ============================================================
# SECTION 9: START THE PROGRAM
# ============================================================
if __name__ == "__main__":
    main()
