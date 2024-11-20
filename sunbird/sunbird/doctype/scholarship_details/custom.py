import frappe
from frappe import _

@frappe.whitelist()
def update_student_educational_details(scholarship_details):

    if not scholarship_details:
        frappe.throw(_("Scholarship details are missing."))

    scholarship_data = frappe.parse_json(scholarship_details)

    # Fetch the student_id from scholarship details
    student_id = scholarship_data.get("student_id")
    if not student_id:
        frappe.throw(_("Student ID is missing in the scholarship details."))

    # Find a corresponding Student Educational Details record using the student_id
    student_educational_detail_name = frappe.get_value(
        "Student Educational Detail",
        {"student_id": student_id},
        "name"
    )
    
    if not student_educational_detail_name:
        frappe.throw(_("No Student Educational Details found for Student ID {0}.").format(student_id))

    # Fetch the Student Educational Details document
    student_educational_details = frappe.get_doc("Student Educational Detail", student_educational_detail_name)
   
    # Check if the record already exists in the child table
    for record in student_educational_details.scholarship_history:
        if (record.scholarship_start_date == scholarship_data.get("scholarship_start_date") and
            record.scholarship_end_date == scholarship_data.get("scholarship_end_date")):
            frappe.throw(_("A similar scholarship record already exists in the Scholarship History."))

    student_educational_details.append("scholarship_history", {
        "scholarship_start_date": scholarship_data.get("scholarship_start_date"),
        "scholarship_end_date": scholarship_data.get("scholarship_end_date"),
        "total_amount_of_scholarship": scholarship_data.get("scholarship_amount")
    })

    student_educational_details.save()
    frappe.db.commit()

 
    return _("Student Educational Details updated successfully for Student ID {0}.").format(student_id)
