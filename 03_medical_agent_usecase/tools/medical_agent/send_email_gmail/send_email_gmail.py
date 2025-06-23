from typing import Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool

import base64
import json
import os
import datetime
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Get absolute path to `.env` in the same directory
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

token_path = os.getenv("GMAIL_TOKEN_JSON")
if not token_path:
    raise EnvironmentError("❌ GMAIL_TOKEN_JSON environment variable not found")

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class WatsonxGmailTool:
    """Gmail tool for watsonx orchestrate"""

    def __init__(self):
        self.service = None
        self._authenticate()

    def _authenticate(self):
        try:
            token_json = os.environ.get('GMAIL_TOKEN_JSON')
            if not token_json:
                raise ValueError("GMAIL_TOKEN_JSON environment variable not found")

            token_data = json.loads(token_json)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)

            if creds.expired and creds.refresh_token:
                creds.refresh(Request())

            if not creds.valid:
                raise ValueError("Invalid Gmail credentials")

            self.service = build('gmail', 'v1', credentials=creds)
        except Exception as e:
            raise Exception(f"Gmail authentication failed: {e}")

    def send_email(self, to_email, subject, body, cc=None, bcc=None):
        try:
            if not self.service:
                raise Exception("Gmail service not initialized")

            message = MIMEText(body, 'plain')
            message['to'] = to_email
            message['subject'] = subject
            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()

            return {
                'success': True,
                'message_id': result['id'],
                'to': to_email,
                'subject': subject
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

@tool
def send_email_gmail(
    to: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None
) -> str:
    """
    ส่งอีเมลผ่าน Gmail (หรือจำลอง หาก Gmail ไม่ถูกตั้งค่า)

    :param to: อีเมลของผู้รับหลัก
    :param subject: หัวข้อของอีเมล
    :param body: เนื้อหาของอีเมล
    :param cc: รายชื่ออีเมลที่ต้องการคัดลอก (ถ้ามี)
    :param bcc: รายชื่ออีเมลที่ต้องการคัดลอกแบบซ่อน (ถ้ามี)

    :returns: สรุปผลการส่งอีเมล (ภาษาไทย)
    """
    try:
        gmail_tool = WatsonxGmailTool()
        result = gmail_tool.send_email(to, subject, body, cc=cc, bcc=bcc)

        if result['success']:
            return f"""✅ ส่งอีเมลสำเร็จ
ถึง: {to}
หัวข้อ: {subject}
สำเนา (CC): {cc if cc else "-"}
สำเนาลับ (BCC): {bcc if bcc else "-"}"""
        else:
            raise Exception(result['error'])

    except Exception as e:
        # fallback to simulation
        cc_display = cc if cc is not None else "-"
        bcc_display = bcc if bcc is not None else "-"
        return f"""⚠️ จำลองการส่งอีเมล (โหมดจำลอง เนื่องจากเกิดข้อผิดพลาด)

ถึง: {to}
หัวข้อ: {subject}
สำเนา (CC): {cc_display}
สำเนาลับ (BCC): {bcc_display}
---
{body}

❌ เหตุผลที่ไม่สามารถส่งอีเมลจริงได้: {str(e)}
"""