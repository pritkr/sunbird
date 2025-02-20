import frappe
from frappe.model.document import Document

class ScholarshipApplication(Document):
    def before_save(self):
        self.total_amount_of_scholarship_recieving = (
            (self.tuition_fees_approved or 0) + 
            (self.nutrition_support_fees_approved or 0) + 
            (self.hostel_fees_approved or 0) + 
            (self.scholarship_amount or 0) + 
            (self.other_sponsorship_approved or 0)
        )
