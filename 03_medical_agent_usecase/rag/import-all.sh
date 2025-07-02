#!/usr/bin/env bash
set -x

orchestrate env activate test-env
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

for python_tool in diabetes_agent/get_diabetes_diet_rag.py; do
  orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/${python_tool}" \
    -p "${SCRIPT_DIR}/tools/diabetes_agent" \
    -r "${SCRIPT_DIR}/tools/requirements.txt"
done

for agent in diabetes_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done