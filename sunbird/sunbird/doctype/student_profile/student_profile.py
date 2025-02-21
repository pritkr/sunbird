# Copyright (c) 2024, T4GC and contributors
# For license information, please see license.txt

import frappe
import dns.resolver
import smtplib
from frappe.model.document import Document
from frappe import _
from datetime import date

class StudentProfile(Document):
    def before_save(self):
        """Perform validations and calculations before saving the Student Profile"""

        # Calculate age for multiple DOB fields
        self.calculate_ages()

        # Validate multiple email fields
        self.validate_emails()

    def calculate_ages(self):
        """Calculate age for multiple DOB fields"""
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

    def validate_emails(self):
        """Validate multiple email fields"""
        email_fields = ["student_email_id", "mother_email_id", "father_email_id", "gaurdian_email_id"]
        invalid_emails = []

        for field in email_fields:
            email = getattr(self, field, None)
            if email:  # Only check if email is provided
                domain_status, smtp_status = validate_email(email)
                
                if not domain_status:
                    invalid_emails.append(f"Invalid domain: {field} ({email})")
                elif not smtp_status:
                    invalid_emails.append(f"SMTP check failed: {field} ({email})")

        if invalid_emails:
            frappe.throw(_("Email validation errors:\n" + "\n".join(invalid_emails)))

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
