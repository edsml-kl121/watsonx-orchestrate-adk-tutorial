#!/usr/bin/env bash
set -x

orchestrate env activate ibm-env
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

for python_tool in hr_agent/get_my_policies.py; do
  orchestrate tools import -k python -f ${SCRIPT_DIR}/tools/${python_tool} -r ${SCRIPT_DIR}/tools/requirements.txt
done

for agent in hr_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done

