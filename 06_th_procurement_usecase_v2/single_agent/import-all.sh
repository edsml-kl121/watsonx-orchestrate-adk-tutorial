#!/usr/bin/env bash
set -x

orchestrate env activate .venv
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/procurement_agent/get_procurement_transaction_history/get_procurement_transaction_history.py" \
    -p "${SCRIPT_DIR}/tools/procurement_agent/get_procurement_transaction_history" \
    -r "${SCRIPT_DIR}/tools/procurement_agent/get_procurement_transaction_history/requirements.txt"

orchestrate tools import -k python \
    -f "${SCRIPT_DIR}/tools/procurement_agent/get_procurement_product_list/get_procurement_product_list.py" \
    -r "${SCRIPT_DIR}/tools/procurement_agent/get_procurement_product_list/requirements.txt"


for agent in procurement_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done

