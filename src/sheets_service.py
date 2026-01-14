from googleapiclient.discovery import build
from gmail_service import get_gmail_service

def get_sheets_service():
    # Reuse SAME credentials from Gmail service
    gmail_service = get_gmail_service()
    creds = gmail_service._http.credentials
    return build("sheets", "v4", credentials=creds)
