# Gmail to Google Sheets Automation

## Author
Aakash Chaurasiya

## Description
This project fetches unread emails from a Gmail account using the Gmail API and logs key email details (sender, subject, date, content) into a Google Sheet using the Google Sheets API.

The script processes only unread emails and marks the entire Gmail thread as read after successful insertion to avoid duplicate processing.

## Features
- Fetches unread Gmail messages
- Writes email details to Google Sheets
- Prevents duplicate processing using Gmail thread-level read status
- Handles large inboxes efficiently
- OAuth 2.0 based authentication

## Technologies Used
- Python
- Gmail API
- Google Sheets API
- OAuth 2.0

## Setup Instructions
1. Create a Google Cloud Project
2. Enable Gmail API and Google Sheets API
3. Configure OAuth Consent Screen (External)
4. Add required scopes:
   - https://www.googleapis.com/auth/gmail.modify
   - https://www.googleapis.com/auth/spreadsheets
5. Download `credentials.json` and place it inside `credentials/`
6. Install dependencies:
   ```bash
   pip install -r requirements.txt
