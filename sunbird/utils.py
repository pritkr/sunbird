import frappe
import dns.resolver
import smtplib

def verify_email_sync(email):
    """Light MX record check (safe for before_save)"""
    domain = email.split('@')[-1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            return False, f"Domain {domain} has no MX records."
        return True, "Domain has MX records."
    except dns.resolver.NoAnswer:
        return False, f"Domain {domain} has no MX records."
    except dns.resolver.NXDOMAIN:
        return False, f"Domain {domain} does not exist."
    except Exception as e:
        return False, f"MX lookup failed: {str(e)}"

def enqueue_email_verification(docname, email):
    """Run full SMTP check in background"""
    frappe.enqueue(
        method="your_app.your_module.utils.verify_email_async",
        queue='long',
        timeout=60,
        now=False,
        docname=docname,
        email=email
    )

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
        server = smtplib.SMTP(mail_server, 25, timeout=10)
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
    """Helper to update the verification status field"""
    try:
        doc = frappe.get_doc("Institute Profile", docname)
        doc.db_set("email_verification_status", status)
    except Exception as e:
        frappe.logger().error(f"Failed to update email status: {str(e)}")
