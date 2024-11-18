# Copyright (c) 2024, T4GC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today
class ScholarshipDetails(Document):
	pass

def check_scholarship_status(doc, method):
    # Avoid recursion using status_updated flag
    if getattr(frappe.flags, 'status_updated', False):
        return  
    
    if not doc.scholarship_end_date:
        frappe.throw(_("Scholarship end date is missing."))

    current_date = today()

    if doc.scholarship_end_date and doc.scholarship_end_date < current_date:
        doc.scholarship_status = "Tenure Completed"
        
        frappe.flags.status_updated = True
        
        doc.save(ignore_permissions=True)