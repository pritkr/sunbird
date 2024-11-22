import frappe
from frappe import _

@frappe.whitelist()
def update_student_profile(scholarship_details):

    if not scholarship_details:
        frappe.throw(_("Scholarship details are missing."))

    scholarship_data = frappe.parse_json(scholarship_details)

    # Fetch the student_id from scholarship details
    student_id = scholarship_data.get("student_id")
    if not student_id:
        frappe.throw(_("Student ID is missing in the scholarship details."))

    student_profile_name = student_id

    if not student_profile_name:
        frappe.throw(_("No Student Profile found for Student ID {0}.").format(student_id))

    student_profile = frappe.get_doc("Student Profile", student_profile_name)
   
    # Find a corresponding Student Educational Details record using the student_id
    student_educational_detail_name = frappe.get_value(
        "Student Educational Detail",
        {"student_id": student_id},
        "name"
    )
    
    if not student_educational_detail_name:
        frappe.throw(_("No Student Educational Details found for Student ID {0}.").format(student_id))

    student_educational_details = frappe.get_doc("Student Educational Detail", student_educational_detail_name)

    # Get the current year class from Student Educational Details
    current_year_class = student_educational_details.current_year_class
   
    # Check if the record already exists in the child table
    for record in student_profile.scholarship_history:
        if (record.scholarship_start_date == scholarship_data.get("scholarship_start_date") and
            record.scholarship_end_date == scholarship_data.get("scholarship_end_date")):
            frappe.throw(_("A similar scholarship record already exists in the Scholarship History."))

    # Append the scholarship record to the Student Profile
    student_profile.append("scholarship_history", {
        "class": current_year_class,
        "scholarship_start_date": scholarship_data.get("scholarship_start_date"),
        "scholarship_end_date": scholarship_data.get("scholarship_end_date"),
        "total_amount_of_scholarship": scholarship_data.get("scholarship_amount")
    })

    student_profile.save()
    frappe.db.commit()

 
    return _("Student Educational Details updated successfully for Student ID {0}.").format(student_id)
