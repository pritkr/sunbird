import frappe
from frappe import _

def get_data(filters):
    conditions = []
    if filters.get("student_id"):
        conditions.append(("Scholarship Details", "student_id", "=", filters["student_id"]))
    if filters.get("institute_id"):
        conditions.append(("Scholarship Details", "institute_id", "=", filters["institute_id"]))
    if filters.get("year"):
        conditions.append(("Scholarship Details", "current_scholarship_year", "=", filters["year"]))
    if filters.get("status"):
        conditions.append(("Scholarship Details", "scholarship_status", "=", filters['status']))

    data = frappe.get_all(
        "Scholarship Details",
        fields=["student_name", "institute_id","institute_name" ,"type_of_student", "scholarship_amount", "current_scholarship_year","scholarship_start_date" ,"scholarship_end_date", "scholarship_status"],
        filters=conditions,
        order_by="student_name, current_scholarship_year"
    )

    grouped_data = []
    previous_student = None
    previous_institute = None
    previous_institute_name = None

    for row in data:
        display_student_name = row["student_name"] if row["student_name"] != previous_student else ""
        display_institute_id = row["institute_id"] if row["institute_id"] != previous_institute else ""
        display_institute_name = row["institute_name"] if row["institute_name"] != previous_institute_name else ""

        grouped_data.append({
            "student_name": display_student_name,
            "institute_id": display_institute_id,
            "institute_name": display_institute_name,
            "type_of_student": row["type_of_student"],
            "scholarship_amount": row["scholarship_amount"],
            "current_scholarship_year": row["current_scholarship_year"],
            "scholarship_start_date": row["scholarship_start_date"],
            "scholarship_end_date": row["scholarship_end_date"],
            "scholarship_status": row["scholarship_status"]
        })

        previous_student = row["student_name"]
        previous_institute = row["institute_id"]
        previous_institute_name = row["institute_name"]

    return grouped_data

def execute(filters=None):
    columns = [
        {"label": _("Student Name"), "fieldname": "student_name", "fieldtype": "Link", "options": "Student Profile"},
        {"label": _("Institute ID"), "fieldname": "institute_id", "fieldtype": "Link", "options": "Institute Profile"},
        {"label": _("Institute Name"), "fieldname":"institute_name", "fieldtype": "Data"},
        {"label": _("Student Type"), "fieldname": "type_of_student", "fieldtype": "Link", "options": "Type of Student"},
        {"label": _("Scholarship Amount"), "fieldname": "scholarship_amount", "fieldtype": "Currency"},
        {"label": _("Scholarship Year"), "fieldname": "current_scholarship_year", "fieldtype": "Int"},
        {"label": _("Scholarship Start Date"), "fieldname": "scholarship_start_date", "fieldtype": "Date"},
        {"label": _("Scholarship End Date"), "fieldname": "scholarship_end_date", "fieldtype": "Date"},
        {"label": _("Scholarship Status"), "fieldname":"scholarship_status", "fieldtype": "Select"}
    ]

    data = get_data(filters)
    return columns, data
