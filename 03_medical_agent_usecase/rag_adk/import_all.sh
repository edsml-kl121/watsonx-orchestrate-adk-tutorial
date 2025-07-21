#!/usr/bin/env bash
set -x

git lfs install

orchestrate env activate TZ-37
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_base/diabetes_knowledge_base.yaml
orchestrate agents import -f ${SCRIPT_DIR}/agents/diabetes_agent.yaml