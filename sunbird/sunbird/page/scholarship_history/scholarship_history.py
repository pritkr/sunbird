import frappe

@frappe.whitelist()
def get_student_ids():
    """
    Fetch all student IDs from the Student Profile doctype.
    """
    student_ids = frappe.db.get_all('Student Profile', fields=['name'])
    return [student['name'] for student in student_ids]

@frappe.whitelist()
def get_institute_ids():
    """
    Fetch all institute IDs from the Institute Profile doctype.
    """
    institute_ids = frappe.db.get_all('Institute Profile', fields=['name'])
    return [institute['name'] for institute in institute_ids]

@frappe.whitelist()
def get_scholarships(student_id=None, institute_id=None, current_scholarship_year =None):
    # Set up filters based on non-empty arguments
    filters = {}
    if student_id:
        filters["student_id"] = student_id
    if institute_id:
        filters["institute_id"] = institute_id
    if current_scholarship_year:
        filters["year"] = current_scholarship_year

    # Fetch scholarship records based on filters
    scholarships = frappe.get_all(
        "Scholarship Details",
        fields=["name", "student_name", "institute_id", "type_of_student", "scholarship_amount", "scholarship_end_date", "current_scholarship_year"],
        filters=filters
    )

    return scholarships

