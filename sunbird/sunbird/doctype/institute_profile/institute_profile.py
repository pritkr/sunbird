import frappe
from frappe.model.document import Document
from sunbird.utils import verify_email_sync, enqueue_email_verification

class InstituteProfile(Document):
    def before_save(self):
        if self.email_id:
            status, message = verify_email_sync(self.email_id)
            if not status:
                if "MX" in message or "Domain" in message:
                    frappe.throw(f"Email verification failed: {message}")  # critical failure
                else:
                    frappe.msgprint(f"Warning: {message}")  # soft warning

    def after_insert(self):
        if self.email_id:
            enqueue_email_verification(self.name, self.email_id)
