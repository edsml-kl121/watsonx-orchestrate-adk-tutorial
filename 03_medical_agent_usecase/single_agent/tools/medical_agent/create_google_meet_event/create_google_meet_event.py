import os
import json
import re
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from dotenv import load_dotenv

# Get absolute path to `.env` in the same directory
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

def _convert_to_24hour(time_str):
    """Convert various time formats to 24-hour HH:MM format"""
    time_str = time_str.strip().lower()
    
    # Already in HH:MM format
    if re.match(r'^\d{1,2}:\d{2}$', time_str):
        parts = time_str.split(':')
        hour = int(parts[0])
        minute = int(parts[1])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return f"{hour:02d}:{minute:02d}"
    
    # Handle AM/PM format like "6pm", "6:30pm", "6 pm"
    am_pm_match = re.match(r'^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$', time_str)
    if am_pm_match:
        hour = int(am_pm_match.group(1))
        minute = int(am_pm_match.group(2)) if am_pm_match.group(2) else 0
        am_pm = am_pm_match.group(3)
        
        # Convert to 24-hour
        if am_pm == 'pm' and hour != 12:
            hour += 12
        elif am_pm == 'am' and hour == 12:
            hour = 0
        
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return f"{hour:02d}:{minute:02d}"
    
    # Handle just numbers like "6", "18"
    if re.match(r'^\d{1,2}$', time_str):
        hour = int(time_str)
        # Assume PM for single digit hours 1-11, 24-hour for 12-23
        if 1 <= hour <= 11:
            hour += 12  # Convert to PM
        elif hour == 12:
            hour = 12   # Keep as noon
        elif 0 <= hour <= 23:
            pass  # Already in 24-hour format
        else:
            return None
        
        return f"{hour:02d}:00"
    
    return None

def _parse_time_input(time_input):
    """Parse various time formats and return start_time and end_time in HH:MM format"""
    # Remove spaces and convert to lowercase
    time_str = time_input.strip().lower()
    
    # Handle range formats like "6-8pm", "18:00-20:00", "6pm-8pm"
    if '-' in time_str:
        parts = time_str.split('-')
        if len(parts) == 2:
            start_part = parts[0].strip()
            end_part = parts[1].strip()
            
            # Convert to 24-hour format
            start_24 = _convert_to_24hour(start_part)
            end_24 = _convert_to_24hour(end_part)
            
            if start_24 and end_24:
                return start_24, end_24
    
    # Handle single time like "6pm", "18:00"
    start_24 = _convert_to_24hour(time_str)
    if start_24:
        # Default to 1-hour duration
        start_hour, start_min = map(int, start_24.split(':'))
        end_hour = start_hour + 1
        if end_hour >= 24:
            end_hour = 23
            end_min = 59
        else:
            end_min = start_min
        end_24 = f"{end_hour:02d}:{end_min:02d}"
        return start_24, end_24
    
    # If nothing works, return None
    return None, None

@tool
def create_google_meet_event(title: str, date: str, time: str, attendees: list[str]) -> str:
    """
    สร้างการนัดหมายผ่าน Google Calendar พร้อม Google Meet

    :param title: ชื่อกิจกรรม
    :param date: วันที่ในรูปแบบ YYYY-MM-DD
    :param time: เวลาในรูปแบบ HH:MM หรือ 6-8pm
    :param attendees: รายชื่ออีเมลของผู้เข้าร่วม

    :returns: ข้อมูลการนัดหมายในภาษาไทย
    """
    
    # Try to create real calendar event first
    try:
        result = _create_real_calendar_event(title, date, time, attendees)
        if result and result.get('success'):
            attendee_list = ", ".join(attendees)
            return f"""✅ สร้างกิจกรรม Google Calendar สำเร็จ!

📅 รายละเอียดการนัดหมาย:
หัวข้อ: {title}
วันที่: {date}
เวลา: {result.get('display_time', time)} น. (เวลาประเทศไทย)
ผู้เข้าร่วม: {attendee_list}

🔗 ลิงก์:
• กิจกรรมใน Google Calendar: {result.get('event_link', '')}
• Event ID: {result.get('event_id', '')}

💡 หมายเหตุ: การนัดหมายถูกสร้างในปฏิทิน Google Calendar ของคุณแล้ว"""
        else:
            # Show the actual error instead of simulation
            error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
            attendee_list = ", ".join(attendees)
            return f"""❌ ไม่สามารถสร้างกิจกรรม Google Calendar ได้

📅 รายละเอียดที่ขอสร้าง:
หัวข้อ: {title}
วันที่: {date}
เวลา: {time} น.
ผู้เข้าร่วม: {attendee_list}

🔧 สาเหตุข้อผิดพลาด: {error_msg}

💡 วิธีแก้ไข:
• หากแสดง "GOOGLE_CALENDAR_TOKEN_JSON not found" = ยังไม่ได้ตั้งค่า .env file
• หากแสดง "Token file not found" = ไฟล์ token.json ไม่อยู่ใน path ที่ระบุ
• หากแสดง "Google API libraries not available" = ต้อง install libraries
• หากแสดง "Invalid time format" = ใช้รูปแบบเวลาที่ถูกต้อง เช่น 18:00, 6pm, 6-8pm

ลิงก์จำลอง: https://meet.google.com/mock-link-1234"""
        
    except Exception as e:
        # Show the exception error
        attendee_list = ", ".join(attendees)
        return f"""❌ เกิดข้อผิดพลาดในการสร้างกิจกรรม

📅 รายละเอียดที่ขอสร้าง:
หัวข้อ: {title}
วันที่: {date}
เวลา: {time} น.
ผู้เข้าร่วม: {attendee_list}

🔧 ข้อผิดพลาด: {str(e)}

💡 ตรวจสอบการตั้งค่า .env file และ Google API libraries

ลิงก์จำลอง: https://meet.google.com/mock-link-1234"""

def _create_real_calendar_event(title, date, time, attendees):
    """Helper function to create real Google Calendar event"""
    try:
        # Get token data from environment variable
        token_data = os.getenv("GOOGLE_CALENDAR_TOKEN_JSON")
        if not token_data:
            return {'success': False, 'error': 'GOOGLE_CALENDAR_TOKEN_JSON environment variable not found in .env file'}
        
        # Import Google libraries only when needed
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        
        # Check if token_data is a file path or JSON content
        if token_data.startswith('{'):
            # It's JSON content directly
            try:
                token_info = json.loads(token_data)
                creds = Credentials.from_authorized_user_info(token_info, SCOPES)
            except json.JSONDecodeError as e:
                return {'success': False, 'error': f'Invalid JSON in GOOGLE_CALENDAR_TOKEN_JSON: {e}'}
        else:
            # It's a file path
            if not os.path.exists(token_data):
                return {'success': False, 'error': f'Token file not found at: {token_data}'}
            
            # Load credentials from file
            creds = Credentials.from_authorized_user_file(token_data, SCOPES)
        
        # Refresh token if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # If it was from a file, save back to file
            if not token_data.startswith('{') and os.path.exists(token_data):
                with open(token_data, 'w') as token:
                    token.write(creds.to_json())
        
        # Build the Calendar API service
        service = build('calendar', 'v3', credentials=creds)
        
        # Parse time input to handle various formats
        start_time, end_time = _parse_time_input(time)
        if not start_time or not end_time:
            return {'success': False, 'error': f'Invalid time format: {time}. Use formats like "18:00", "6pm", "6-8pm", "18:00-20:00"'}
        
        # Create event object
        event = {
            'summary': title,
            'location': 'Conference Room A',
            'description': 'Meeting created via Watsonx Orchestrate',
            'start': {
                'dateTime': f'{date}T{start_time}:00+07:00',  # Bangkok timezone
                'timeZone': 'Asia/Bangkok',
            },
            'end': {
                'dateTime': f'{date}T{end_time}:00+07:00',  # Bangkok timezone
                'timeZone': 'Asia/Bangkok',
            },
            'attendees': [{'email': email} for email in attendees],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                    {'method': 'popup', 'minutes': 10},       # 10 minutes before
                ],
            },
        }
        
        # Create the event
        event_result = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()
        
        return {
            'success': True,
            'event_id': event_result['id'],
            'event_link': event_result['htmlLink'],
            'display_time': f'{start_time}-{end_time}'
        }
        
    except ImportError:
        return {'success': False, 'error': 'Google API libraries not available. Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv'}
    except FileNotFoundError:
        return {'success': False, 'error': 'Token file not found'}
    except Exception as e:
        return {'success': False, 'error': str(e)}