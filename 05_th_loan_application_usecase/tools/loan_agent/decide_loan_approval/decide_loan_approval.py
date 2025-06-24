from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def decide_loan_approval(applicant_id: str) -> str:
    """
    Decide whether a loan should be approved based on mocked credit/risk scores.
    Returns CSV-formatted string.
    """

    header = "applicant_id,approved,interest_rate,reason"

    try:
        applicants = {
            "T001": {"credit_score": 720, "risk_score": 15},
            "T002": {"credit_score": 580, "risk_score": 52},
            "T003": {"credit_score": 650, "risk_score": 48},
            "T004": {"credit_score": 610, "risk_score": 30},
            "T005": {"credit_score": 680, "risk_score": 40}
        }

        if applicant_id not in applicants:
            return f"{header}\n{applicant_id},UNKNOWN,,Applicant ID not found"

        credit = applicants[applicant_id]["credit_score"]
        risk = applicants[applicant_id]["risk_score"]

        if credit >= 600 and risk < 45:
            approved = "TRUE"
            rate = round(6.5 + (50 - min(credit, 850)) * 0.01, 2)
            rate_str = f"{rate:.2f}"
            reason = "Eligible based on credit and risk thresholds"
        else:
            approved = "FALSE"
            rate_str = ""
            reason = "Rejected due to credit score or risk score"

        return f"{header}\n{applicant_id},{approved},{rate_str},{reason}"

    except Exception as e:
        return f"{header}\n{applicant_id},ERROR,,Tool error: {str(e).replace(',', ';')}"