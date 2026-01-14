import base64
from email.utils import parsedate_to_datetime


def get_header(headers, name):
    """
    Utility to fetch header value safely
    """
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def extract_email_body(payload):
    """
    Extract plain text body from email payload
    """
    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType")
            body = part.get("body", {}).get("data")

            if mime_type == "text/plain" and body:
                return base64.urlsafe_b64decode(body).decode("utf-8")

    # Fallback (single-part email)
    body = payload.get("body", {}).get("data")
    if body:
        return base64.urlsafe_b64decode(body).decode("utf-8")

    return ""


def parse_email(message):
    """
    Parse Gmail message into structured data
    """
    payload = message["payload"]
    headers = payload.get("headers", [])

    from_email = get_header(headers, "From")
    subject = get_header(headers, "Subject")
    date_raw = get_header(headers, "Date")

    try:
        date = parsedate_to_datetime(date_raw)
    except Exception:
        date = date_raw

    body = extract_email_body(payload)

    return {
        "from": from_email,
        "subject": subject,
        "date": str(date),
        "content": body.strip()
    }
