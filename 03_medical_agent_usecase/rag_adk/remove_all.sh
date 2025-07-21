#!/usr/bin/env bash
set -x

orchestrate env activate TZ-37
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

orchestrate knowledge-bases remove -n diabetes_knowledge_base
# orchestrate agents remove -n ibm_agent -k native