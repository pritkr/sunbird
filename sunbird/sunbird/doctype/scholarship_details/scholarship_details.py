# Copyright (c) 2024, T4GC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate
from frappe import _

class ScholarshipDetails(Document):
    def before_save(self):
        """Calculate total scholarship amount before saving"""
        
        # List of scholarship fields to sum
        scholarship_fields = [
            "tuition_fees_approved",
            "nutrition_support_fees_approved",
            "hostel_fees_approved",
            "scholarship_amount",
            "other_sponsorship_approved",
        ]

        total_scholarship = 0

        for field in scholarship_fields:
            value = getattr(self, field, 0)  # Get field value, default to 0 if None
            if isinstance(value, (int, float)):  # Ensure the value is numeric
                total_scholarship += value
        
        self.total_amount_of_scholarship_recieving = total_scholarship  # Set total amount

def check_scholarship_status(doc, method):
    # Avoid recursion using status_updated flag
    if getattr(frappe.flags, 'status_updated', False):
        return  
    
    if not doc.scholarship_end_date:
        frappe.throw(_("Scholarship end date is missing."))

    current_date = getdate(today())

    if doc.scholarship_end_date and getdate(doc.scholarship_end_date) < current_date:
        doc.scholarship_status = "Tenure Completed"
        
        frappe.flags.status_updated = True
        
        doc.save(ignore_permissions=True)
