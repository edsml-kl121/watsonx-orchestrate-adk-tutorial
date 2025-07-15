set -a  # Automatically export all variables
source .env
set +a

orchestrate connections add -a watsonx_ai_creds
orchestrate connections configure -a watsonx_ai_creds --env draft -k key_value -t team
orchestrate connections configure -a watsonx_ai_creds --env live -k key_value -t team
orchestrate connections set-credentials -a watsonx_ai_creds --env draft \
  -e "api_key=$WATSONX_API_KEY" \
  -e "watsonx_project_id=$WATSONX_PROJECT_ID" 
orchestrate connections set-credentials -a watsonx_ai_creds --env live \
  -e "api_key=$WATSONX_API_KEY" \
  -e "watsonx_project_id=$WATSONX_PROJECT_ID"