import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from gmail_service import get_gmail_service, get_unread_emails, mark_as_read
from sheets_service import get_sheets_service
from email_parser import parse_email
from config import SPREADSHEET_ID, SHEET_NAME

MAX_CELL_LENGTH = 45000


def main():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    messages = get_unread_emails(gmail_service)
    print(f"Unread emails found: {len(messages)}")

    rows = []

    for msg in messages:
        msg_id = msg["id"]

        full_message = gmail_service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

        parsed = parse_email(full_message)

        # Skip large emails
        if len(parsed["content"]) > MAX_CELL_LENGTH:
            print(f"Skipped large email: {parsed['subject']}")
            mark_as_read(gmail_service, msg_id)
            continue

        rows.append([
            parsed["from"],
            parsed["subject"],
            parsed["date"],
            parsed["content"]
        ])

        # ✅ Mark as read AFTER successful processing
        mark_as_read(gmail_service, msg_id)

    if rows:
        sheets_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:D",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": rows}
        ).execute()

        print(f"{len(rows)} emails appended to Google Sheet")
    else:
        print("No new emails to process")


if __name__ == "__main__":
    main()
