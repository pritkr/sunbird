import frappe
from frappe.model.document import Document
from datetime import date
import smtplib
import dns.resolver

class StudentProfile(Document):
    def before_save(self):
        """Calculate age for multiple DOB fields before saving the Student Profile"""
        self.calculate_age()
        self.verify_emails()

    def calculate_age(self):
        """Calculate age based on various date of birth fields"""
        dob_fields = [
            ("date_of_birth", "age"),
            ("fathers_date_of_birth", "father_age"),
            ("mothers_date_of_birth", "mother_age"),
            ("parents_dob", "parents_age"),
            ("date_of_birth__copy", "gaurdian_age"),
        ]

        today = date.today()

        for dob_field, age_field in dob_fields:
            dob_value = getattr(self, dob_field, None)  
            if dob_value:
                dob = frappe.utils.getdate(dob_value)
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                setattr(self, age_field, age)  

    def verify_emails(self):
        """Verify multiple email fields by checking MX records and SMTP"""
        email_fields = [
            "student_email_id",
            "mother_email_id",
            "father_email_id",
            "gaurdian_email_id",
        ]

        for field in email_fields:
            email = getattr(self, field, None)
            if email:
                domain = email.split("@")[-1]
                mx_valid = self.check_mx_records(domain)
                smtp_valid = self.check_smtp(email) if mx_valid else False
                
                # Store verification result in Frappe Logs
                frappe.logger().info(f"Email: {email}, MX: {mx_valid}, SMTP: {smtp_valid}")
                
                if not mx_valid:
                    frappe.msgprint(f"Invalid email domain: {domain} for {field}", alert=True, indicator="red")
                elif not smtp_valid:
                    frappe.msgprint(f"Email address {email} could not be verified via SMTP.", alert=True, indicator="orange")

    def check_mx_records(self, domain):
        """Check MX records for a given domain"""
        try:
            mx_records = dns.resolver.resolve(domain, "MX")
            return bool(mx_records)
        except Exception as e:
            frappe.logger().error(f"MX Lookup Failed for {domain}: {e}")
            return False

    def check_smtp(self, email):
        """Perform SMTP check to verify if email exists"""
        domain = email.split("@")[-1]
        try:
            mx_records = dns.resolver.resolve(domain, "MX")
            mx_host = str(mx_records[0].exchange)
            server = smtplib.SMTP(mx_host, 25, timeout=5)
            server.helo()
            server.mail("test@example.com")  # Use a dummy sender email
            code, _ = server.rcpt(email)
            server.quit()
            return code == 250  # 250 means the email is valid
        except Exception as e:
            frappe.logger().error(f"SMTP Check Failed for {email}: {e}")
            return False
