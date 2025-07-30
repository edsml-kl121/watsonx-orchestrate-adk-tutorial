from typing import Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool

import base64
import json
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

def detect_and_convert_table(text):
    """Detect pipe-separated table data and convert to HTML table"""
    lines = text.split('\n')
    
    # Look for lines that contain multiple pipes (|) - likely table rows
    table_lines = []
    non_table_lines = []
    in_table = False
    
    for line in lines:
        stripped_line = line.strip()
        # Check if line looks like a table row (has multiple pipes)
        if stripped_line.count('|') >= 3:  # At least 3 pipes means likely table
            table_lines.append(stripped_line)
            in_table = True
        else:
            if in_table and table_lines:
                # Process the accumulated table
                html_table = convert_pipes_to_html_table(table_lines)
                non_table_lines.append(html_table)
                table_lines = []
                in_table = False
            non_table_lines.append(line)
    
    # Handle remaining table at end of text
    if table_lines:
        html_table = convert_pipes_to_html_table(table_lines)
        non_table_lines.append(html_table)
    
    return '\n'.join(non_table_lines)

def convert_pipes_to_html_table(table_lines):
    """Convert pipe-separated lines to HTML table"""
    if not table_lines:
        return ""
    
    html = '<table border="1" style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; margin: 10px 0;">\n'
    
    for i, line in enumerate(table_lines):
        # Split by pipe and clean up
        cells = [cell.strip() for cell in line.split('|') if cell.strip()]
        
        if not cells:
            continue
            
        # First row is typically header
        tag = 'th' if i == 0 else 'td'
        style = 'style="padding: 8px; text-align: left; background-color: #f2f2f2; font-weight: bold;"' if i == 0 else 'style="padding: 8px; text-align: left;"'
        
        html += '  <tr>\n'
        for cell in cells:
            html += f'    <{tag} {style}>{cell}</{tag}>\n'
        html += '  </tr>\n'
    
    html += '</table>'
    return html

def should_send_as_html(text):
    """Determine if email should be sent as HTML based on content"""
    # Check for table-like content (multiple lines with pipes)
    lines = text.split('\n')
    table_line_count = sum(1 for line in lines if line.strip().count('|') >= 3)
    
    return table_line_count >= 2  # If 2+ lines look like table rows

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

            # Check if we should send as HTML
            if should_send_as_html(body):
                # Convert table content and send as HTML
                html_body = detect_and_convert_table(body)
                # Replace newlines with <br> for HTML
                html_body = html_body.replace('\n', '<br>\n')
                
                message = MIMEMultipart('alternative')
                message['to'] = to_email
                message['subject'] = subject
                
                if cc:
                    message['cc'] = cc
                if bcc:
                    message['bcc'] = bcc

                # Add plain text version
                text_part = MIMEText(body, 'plain', 'utf-8')
                message.attach(text_part)
                
                # Add HTML version
                html_part = MIMEText(html_body, 'html', 'utf-8')
                message.attach(html_part)
            else:
                # Send as plain text only
                message = MIMEMultipart()
                message['to'] = to_email
                message['subject'] = subject
                
                if cc:
                    message['cc'] = cc
                if bcc:
                    message['bcc'] = bcc

                body_part = MIMEText(body, 'plain', 'utf-8')
                message.attach(body_part)

            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('ascii')
            
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

def decode_unicode_escapes(text):
    """Decode Unicode escape sequences in text only if they exist"""
    # Check if text contains Unicode escape sequences
    if '\\u' not in text and '\\n' not in text and '\\t' not in text:
        # No escape sequences found, return original text
        return text
    
    try:
        # Method 1: Use json.loads for proper Unicode handling
        import json
        json_string = f'"{text}"'
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError, ValueError):
        try:
            # Method 2: Use codecs.decode
            import codecs
            return codecs.decode(text, 'unicode_escape')
        except (UnicodeDecodeError, UnicodeEncodeError):
            # If all methods fail, return original text
            return text

@tool
def send_email_gmail_v2(
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
        # Decode Unicode escape sequences
        decoded_subject = decode_unicode_escapes(subject)
        decoded_body = decode_unicode_escapes(body)
        
        gmail_tool = WatsonxGmailTool()
        result = gmail_tool.send_email(to, decoded_subject, decoded_body, cc=cc, bcc=bcc)

        if result['success']:
            return f"""✅ ส่งอีเมลสำเร็จ
ถึง: {to}
หัวข้อ: {decoded_subject}
สำเนา (CC): {cc if cc else "-"}
สำเนาลับ (BCC): {bcc if bcc else "-"}
ID ข้อความ: {result['message_id']}"""
        else:
            raise Exception(result['error'])

    except Exception as e:
        # fallback to simulation
        cc_display = cc if cc is not None else "-"
        bcc_display = bcc if bcc is not None else "-"
        decoded_body_preview = decode_unicode_escapes(body)
        
        return f"""⚠️ จำลองการส่งอีเมล (โหมดจำลอง เนื่องจากเกิดข้อผิดพลาด)

ถึง: {to}
หัวข้อ: {decode_unicode_escapes(subject)}
สำเนา (CC): {cc_display}
สำเนาลับ (BCC): {bcc_display}
---
{decoded_body_preview}

❌ เหตุผลที่ไม่สามารถส่งอีเมลจริงได้: {str(e)}
"""