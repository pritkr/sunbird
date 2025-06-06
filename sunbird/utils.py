import frappe
import dns.resolver
import smtplib
@frappe.whitelist()
def email_verification(email):
    """Validates an email address by checking DNS, MX, and SMTP (RCPT TO)"""

    # Step 0: Basic email format validation
    if not email or "@" not in email:
        return {"message": "Please provide a valid email address.", "indicator": "orange"}

    local_part, domain = email.split('@', 1)

    if not local_part or not domain:
        return {"message": "Incomplete email address.", "indicator": "orange"}

    # Step 1: DNS & MX Validation
    try:
        dns.resolver.resolve(domain, 'A')  # check domain has A record
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
        return {"message": f"Domain {domain} is not valid (DNS A record not found).", "indicator": "orange"}

    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            return {"message": f"Domain {domain} has no MX records (no email server).", "indicator": "orange"}
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        return {"message": f"Domain {domain} has no valid MX records.", "indicator": "orange"}
    except Exception as e:
        return {"message": f"MX check failed: {str(e)}", "indicator": "orange"}

    # Step 2: SMTP verification (RCPT TO)
    mail_server = str(mx_records[0].exchange)
    try:
        smtp = smtplib.SMTP(mail_server, 25, timeout=10)
        smtp.starttls()
        smtp.helo()
        smtp.mail("noreply@example.com")
        code, _ = smtp.rcpt(email)
        smtp.quit()

        if code == 250:
            return {"message": f"Email address {email} is valid and deliverable.", "indicator": "green", "email_verification_status": True}
        else:
            return {"message": f"Domain is valid, but email {email} is not deliverable (SMTP code {code}).", "indicator": "orange"}

    except smtplib.SMTPServerDisconnected:
        return {"message": f"SMTP server {mail_server} disconnected unexpectedly. Could not verify {email}.", "indicator": "orange"}
    except smtplib.SMTPRecipientsRefused:
        return {"message": f"Domain {domain} is valid, but recipient {email} was refused.", "indicator": "orange"}
    except Exception as e:
        return {"message":"Something went wrong! unable to verify email at this moment please try again after some time or check the email address", "indicator": "orange"}
