#!/usr/bin/env bash
set -x

orchestrate env activate test-env
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/medical_agent/send_email_gmail/send_email_gmail.py" \
    -p "${SCRIPT_DIR}/tools/medical_agent/send_email_gmail" \
    -r "${SCRIPT_DIR}/tools/medical_agent/send_email_gmail/requirements.txt"

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/medical_agent/create_google_meet_event/create_google_meet_event.py" \
    -p "${SCRIPT_DIR}/tools/medical_agent/create_google_meet_event" \
    -r "${SCRIPT_DIR}/tools/medical_agent/create_google_meet_event/requirements.txt"

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/medical_agent/get_appointment_history/get_appointment_history.py" \
    -r "${SCRIPT_DIR}/tools/medical_agent/get_appointment_history/requirements.txt"


for agent in diabetes_agent.yaml medical_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done