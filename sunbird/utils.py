import frappe
import dns.resolver
import smtplib

def verify_email_async(docname, email):
    """SMTP check and update the document"""
    domain = email.split('@')[-1]

    # Step 1: MX check again (to avoid retrying SMTP blindly)
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            update_status(docname, "Invalid domain: No MX records")
            return
    except Exception as e:
        update_status(docname, f"MX check failed: {str(e)}")
        return

    # Step 2: SMTP deliverability check
    mail_server = str(mx_records[0].exchange)
    try:
        server = smtplib.SMTP(mail_server, 587, timeout=10)  # Use port 587 with STARTTLS
        server.starttls()
        server.helo()
        server.mail("noreply@example.com")
        response_code, _ = server.rcpt(email)
        server.quit()

        if response_code == 250:
            update_status(docname, "Deliverable")
        else:
            update_status(docname, f"Undeliverable (SMTP {response_code})")
    except Exception as e:
        update_status(docname, f"SMTP error: {str(e)}")

def update_status(docname, status):
    """Update both the status and checkbox based on result"""
    try:
        doc = frappe.get_doc("Institute Profile", docname)
        is_verified = status.lower() == "deliverable"
        doc.db_set({
            "email_verification_status": status,
            "email_verification_done": 1 if is_verified else 0
        })
    except Exception as e:
        frappe.logger().error(f"Failed to update email status: {str(e)}")
