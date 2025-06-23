from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def create_google_meet_event(title: str, date: str, time: str, attendees: list[str]) -> str:
    """
    จำลองการสร้างการนัดหมายผ่าน Google Meet

    :param title: ชื่อกิจกรรม
    :param date: วันที่ในรูปแบบ YYYY-MM-DD
    :param time: เวลาในรูปแบบ HH:MM (24 ชั่วโมง)
    :param attendees: รายชื่ออีเมลของผู้เข้าร่วม

    :returns: ข้อมูลการนัดหมายแบบจำลองในภาษาไทย
    """
    attendee_list = ", ".join(attendees)
    return f"""📅 จำลองการสร้างกิจกรรม Google Meet

หัวข้อ: {title}
วันที่: {date}
เวลา: {time}
ผู้เข้าร่วม: {attendee_list}
ลิงก์การประชุม: https://meet.google.com/mock-link-1234
"""