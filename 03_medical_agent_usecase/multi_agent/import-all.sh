#!/usr/bin/env bash
set -x

orchestrate env activate test-env
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/medical_agent/get_appointment_history/get_appointment_history.py" \
    -r "${SCRIPT_DIR}/tools/medical_agent/get_appointment_history/requirements.txt"


for agent in diabetes_agent.yaml medical_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done
