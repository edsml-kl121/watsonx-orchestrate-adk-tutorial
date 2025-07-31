#!/usr/bin/env bash
set -x

git lfs install

orchestrate env activate .venv
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_base/project_knowledge_base.yaml
orchestrate agents import -f ${SCRIPT_DIR}/agents/project_agent.yaml