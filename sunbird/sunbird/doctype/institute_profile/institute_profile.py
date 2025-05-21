import frappe
import smtplib
import dns.resolver
from frappe.model.document import Document

class InstituteProfile(Document):
    def before_save(self):
        if self.email_id:
            status, message = verify_email(self.email_id)
            if not status:
                if "MX" in message or "Domain" in message:
                    frappe.throw(f"Email verification failed: {message}")  # critical failure
                else:
                    frappe.msgprint(f"Warning: {message}")  # soft warning, allow save

def verify_email(email):
    domain = email.split('@')[-1]

    # Step 1: Check MX Records (Domain Check)
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            return False, f"Domain {domain} has no MX records (Email server not found)."
    except dns.resolver.NoAnswer:
        return False, f"Domain {domain} does not have any MX records."
    except dns.resolver.NXDOMAIN:
        return False, f"Domain {domain} does not exist."
    except Exception as e:
        return False, f"Error checking MX records for {domain}: {str(e)}"

    # Step 2: SMTP Email Verification
    mail_server = str(mx_records[0].exchange)
    try:
        server = smtplib.SMTP(mail_server, 25, timeout=10)
        server.helo()
        server.mail("test@example.com")  # Fake sender email
        response_code, _ = server.rcpt(email)
        server.quit()

        if response_code == 250:
            return True, "Email exists and is deliverable."
        else:
            return False, f"SMTP check failed for {email}. Server response: {response_code}"
    except smtplib.SMTPConnectError:
        return False, f"Unable to connect to mail server {mail_server}."
    except smtplib.SMTPServerDisconnected:
        frappe.logger().error(f"Mail server {mail_server} disconnected unexpectedly.")
        return False, f"Mail server {mail_server} disconnected unexpectedly."
    except smtplib.SMTPException as e:
        return False, f"SMTP verification error: {str(e)}"
