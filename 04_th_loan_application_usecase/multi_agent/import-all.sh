#!/usr/bin/env bash
set -x

orchestrate env activate test-env
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/loan_agent/decide_loan_approval/decide_loan_approval.py" \
    -p "${SCRIPT_DIR}/tools/loan_agent/decide_loan_approval" \
    -r "${SCRIPT_DIR}/tools/loan_agent/decide_loan_approval/requirements.txt"

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/loan_agent/get_loan_application/get_loan_application.py" \
    -r "${SCRIPT_DIR}/tools/loan_agent/get_loan_application/requirements.txt"

# orchestrate tools import -k python \
#     -f "${SCRIPT_DIR}/tools/loan_agent/generate_approval_email/generate_approval_email.py" \
#     -r "${SCRIPT_DIR}/tools/loan_agent/generate_approval_email/requirements.txt"


for agent in loan_knowledge_agent.yaml loan_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done

