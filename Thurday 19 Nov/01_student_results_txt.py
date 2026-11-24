"""PRACTICAL 1: STUDENT RESULTS - plain text file (Thonny)."""

# ============================================================
# SECTION 1: VALIDATE ONE LINE FROM THE TEXT FILE
# ============================================================
def validate_student(line, students):
    fields = line.strip().split(",")
    field_count = 0
    for field in fields:
        field_count += 1
    if field_count != 3:
        return None, "Expected student_number,name,mark1;mark2;mark3"

    student_number = fields[0].strip()
    student_name = fields[1].strip()
    mark_parts = fields[2].split(";")
    if not student_number.isdigit():
        return None, "Student number must contain digits"
    if student_name == "":
        return None, "Student name is missing"
    if student_number in students:
        return None, "Duplicate student number"

    mark_count = 0
    marks = []
    for mark_text in mark_parts:
        mark_count += 1
        mark_text = mark_text.strip()
        if not mark_text.isdigit():
            return None, "Mark is not a whole number"
        mark = int(mark_text)
        if mark < 0 or mark > 100:
            return None, "Mark must be between 0 and 100"
        marks.append(mark)
    if mark_count != 3:
        return None, "Exactly three marks are required"
    return {"number": student_number, "name": student_name, "marks": marks}, ""


# ============================================================
# SECTION 2: CALCULATE AN AVERAGE MANUALLY
# ============================================================
def calculate_average(marks):
    total = 0
    count = 0
    for mark in marks:
        total += mark
        count += 1
    return total / count


# ============================================================
# SECTION 3: SORT RECORDS MANUALLY (SELECTION SORT)
# ============================================================
def sort_by_average(records):
    # Find the highest average in the unsorted portion.
    index = 0
    while index < len(records):
        best = index
        other = index + 1
        while other < len(records):
            if records[other]["average"] > records[best]["average"]:
                best = other
            other += 1
        records[index], records[best] = records[best], records[index]
        index += 1


# ============================================================
# SECTION 4: READ INPUT, CHECK RECORDS AND BUILD THE REGISTER
# ============================================================
def main():
    students = {}               # Dictionary: student number -> record
    errors = []                 # List of rejected lines and reasons
    line_number = 0
    try:
        with open("learners.txt", "r", encoding="utf-8") as input_file:
            for original_line in input_file:
                line_number += 1
                line = original_line.strip()
                if line == "":
                    continue
                record, reason = validate_student(line, students)
                if reason != "":
                    errors.append("Line " + str(line_number) + ": " + reason + " | " + line)
                else:
                    record["average"] = calculate_average(record["marks"])
                    students[record["number"]] = record
    except FileNotFoundError:
        print("ERROR: Put learners.txt in the same folder as this program.")
        return

    # Convert the dictionary to a list so we can rank the students.
    ranking = []
    for student_number in students:
        ranking.append(students[student_number])
    sort_by_average(ranking)

    # ========================================================
    # SECTION 5: WRITE THE RANKING REPORT
    # ========================================================
    with open("report.txt", "w", encoding="utf-8") as report:
        report.write("RANK | NUMBER | NAME | AVERAGE | RESULT\n")
        rank = 0
        for record in ranking:
            rank += 1
            status = "PASS"
            if record["average"] < 50:
                status = "FAIL"
            report.write(f'{rank} | {record["number"]} | {record["name"]} | '
                         f'{record["average"]:.2f} | {status}\n')

    # ========================================================
    # SECTION 6: WRITE THE ERROR LOG AND CLEAN TEXT FILE
    # ========================================================
    with open("errors.log", "w", encoding="utf-8") as error_file:
        for message in errors:
            error_file.write(message + "\n")

    with open("clean.txt", "w", encoding="utf-8") as clean_file:
        for record in ranking:
            marks = record["marks"]
            clean_file.write(f'{record["number"]},{record["name"]},'
                             f'{marks[0]};{marks[1]};{marks[2]}\n')

    # ========================================================
    # SECTION 7: CHECK THE SAVED DATA AND DISPLAY THE SUMMARY
    # ========================================================
    saved_count = 0
    with open("clean.txt", "r", encoding="utf-8") as clean_file:
        for saved_line in clean_file:
            if saved_line.strip() != "":
                saved_count += 1
    accepted_count = 0
    for record in ranking:
        accepted_count += 1
    rejected_count = 0
    for message in errors:
        rejected_count += 1
    print("STUDENT RESULTS PROCESSOR")
    print("Accepted:", accepted_count, "Rejected:", rejected_count)
    print("Saved and reloaded counts match:", saved_count == accepted_count)
    print("Files created: report.txt, errors.log, clean.txt")


# ============================================================
# SECTION 8: START THE PROGRAM
# ============================================================
if __name__ == "__main__":
    main()
