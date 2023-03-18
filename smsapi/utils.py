def convert_grade_to_gpa(grade):
    if grade >= 90:
        return 4.0
    elif grade >= 80:
        return 3.0
    elif grade >= 70:
        return 2.0
    elif grade >= 60:
        return 1.0
    else:
        return 0.0


def calculate_gpa(grades):
    """
    Calculate the GPA for a list of grades on a 4.0 scale.

    :param grades: A list of numerical grades (floats) in the range of 0.0 to 4.0.
    :return: The calculated GPA (float) rounded to 2 decimal places.
    """
    if not grades:
        return 0.0

    total_gpa = 0
    total_courses = len(grades)

    for grade in grades:
        total_gpa += convert_grade_to_gpa(grade.grade)

    gpa = total_gpa/total_courses
    return round(gpa, 2)
