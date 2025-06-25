from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def generate_approval_email(
    name: str,
    approved: bool,
    loan_amount: int,
    interest_rate: float = None,
    loan_term_months: int = None
) -> str:
    """
    Generate a Thai-language approval or rejection email for a loan applicant.
    This tool only composes the message and does not send the email.

    :param name: The applicant's full name in Thai.
    :param approved: Whether the loan was approved.
    :param loan_amount: Loan amount requested.
    :param interest_rate: Interest rate if approved.
    :param loan_term_months: Loan term in months if approved.

    :returns: A Thai email message as a string, or a debug message in case of error.
    """

    try:
        if approved:
            if interest_rate is None or loan_term_months is None:
                raise ValueError("Missing interest_rate or loan_term_months for approval case.")

            return (
                f"เรียนคุณ{name},\n\n"
                f"เรายินดีที่จะแจ้งให้ทราบว่าใบสมัครสินเชื่อของคุณจำนวน {loan_amount:,} บาท "
                f"ได้รับการอนุมัติเรียบร้อยแล้ว โดยมีอัตราดอกเบี้ย {interest_rate:.2f}% ต่อปี "
                f"เป็นระยะเวลา {loan_term_months} เดือน\n\n"
                f"กรุณาติดต่อเจ้าหน้าที่ของเราสำหรับขั้นตอนถัดไป\n\n"
                f"ขอแสดงความนับถือ\nฝ่ายสินเชื่อ"
            )
        else:
            return (
                f"เรียนคุณ{name},\n\n"
                f"ขออภัยที่แจ้งให้ทราบว่าใบสมัครสินเชื่อของคุณไม่ผ่านการอนุมัติ "
                f"เนื่องจากไม่เป็นไปตามเงื่อนไขเบื้องต้นที่กำหนด\n\n"
                f"หากคุณต้องการข้อมูลเพิ่มเติม กรุณาติดต่อเจ้าหน้าที่ของเรา\n\n"
                f"ขอแสดงความนับถือ\nฝ่ายสินเชื่อ"
            )

    except Exception as e:
        return f"[ERROR] ไม่สามารถสร้างข้อความอีเมลได้: {str(e).replace(',', ';')}"