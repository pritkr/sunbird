# Copyright (c) 2024, T4GC and contributors
# For license information, please see license.txt

import frappe
import dns.resolver
import smtplib
from frappe.model.document import Document
from frappe import _

class InstitutePOC(Document):
    def before_save(self):
        if self.email_id:
            domain_status, smtp_status = validate_email(self.email_id)
            if not domain_status:
                frappe.throw(_("Invalid email domain: {0}").format(self.email_id))
            elif not smtp_status:
                frappe.msgprint(_("Email domain exists, but SMTP verification failed for {0}").format(self.email_id), alert=True)

def validate_email(email):
    """Validate email domain and check SMTP"""
    try:
        domain = email.split('@')[-1]

        # Check if domain has MX records
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            return False, False  # Domain check failed
        
        # Check SMTP connection
        mx_record = str(mx_records[0].exchange)
        smtp = smtplib.SMTP(timeout=10)
        smtp.connect(mx_record)
        smtp.helo()
        smtp.quit()
        
        return True, True  # Both checks passed

    except dns.resolver.NoAnswer:
        return False, False  # No MX records found
    except dns.resolver.NXDOMAIN:
        return False, False  # Domain does not exist
    except smtplib.SMTPException:
        return True, False  # SMTP check failed

