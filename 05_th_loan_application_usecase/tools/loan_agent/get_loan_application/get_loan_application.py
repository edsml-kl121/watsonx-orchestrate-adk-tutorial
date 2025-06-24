from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_loan_application(applicant_id: str = None) -> str:
    """
    Retrieve all loan applications as a CSV-formatted string (ignores input).

    This includes fields like applicant ID, name, loan amount, credit score, etc.
    Used for initial loan review workflows or reporting.

    :param applicant_id: Optional. Currently ignored; all applications are returned.

    :returns: A CSV-formatted string with all loan application records.
    """

    rows = [
        ["applicant_id", "name", "email", "loan_amount", "loan_purpose", "loan_term_months",
         "credit_score", "risk_score", "loan_date_delay_days"],
        ["T001", "สมชาย ใจดี", "somchai.jaidee@example.co.th", 500000, "ซื้อรถยนต์", 84, 720, 15, 5],
        ["T002", "สุดารัตน์ สายใจ", "sudarat.saijai@example.co.th", 300000, "ตกแต่งบ้าน", 60, 580, 52, 0],
        ["T003", "อนันต์ พงษ์ดี", "anan.pongdee@example.co.th", 700000, "ขยายธุรกิจ", 120, 650, 48, 12],
        ["T004", "ณัฐชา วัฒนชัย", "natcha.wattana@example.co.th", 250000, "ค่ารักษาพยาบาล", 36, 610, 30, 3],
        ["T005", "ธีรภัทร แก้วใส", "teerapat.kaewsai@example.co.th", 450000, "ค่าเล่าเรียน", 72, 680, 40, 0]
    ]

    # Convert to CSV string
    csv_string = "\n".join([",".join(map(str, row)) for row in rows])
    return csv_string