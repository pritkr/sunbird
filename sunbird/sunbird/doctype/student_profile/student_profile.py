import frappe
from frappe.model.document import Document
from datetime import date

class StudentProfile(Document):
    def before_save(self):
        """Calculate age for multiple DOB fields before saving the Student Profile"""

        # List of (DOB field, Age field) pairs
        dob_fields = [
            ("date_of_birth", "age"),
            ("fathers_date_of_birth", "father_age"),
            ("mothers_date_of_birth", "mother_age"),
            ("parents_dob", "parents_age"),
            ("date_of_birth__copy", "gaurdian_age"),
        ]

        today = date.today()

        for dob_field, age_field in dob_fields:
            dob_value = getattr(self, dob_field, None)  # Get DOB field value
            
            if dob_value:  # Check if DOB field has a value
                dob = frappe.utils.getdate(dob_value)  # Convert to date object
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                setattr(self, age_field, age)  # Set the calculated age
