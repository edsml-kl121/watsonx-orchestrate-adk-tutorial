set -a  # Automatically export all variables
source .env
set +a

orchestrate connections add -a gg_calendar_adk
orchestrate connections configure -a gg_calendar_adk --env draft -k key_value -t team
orchestrate connections configure -a gg_calendar_adk --env live -k key_value -t team
# Set credentials for draft environment
orchestrate connections set-credentials -a gg_calendar_adk --env draft \
  -e "GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID" \
  -e "GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET" \
  -e "GOOGLE_REDIRECT_URI=$GOOGLE_REDIRECT_URI" \
  -e "MCP_SERVER_NAME=$MCP_SERVER_NAME" \
  -e "MCP_SERVER_VERSION=$MCP_SERVER_VERSION"

# Set credentials for live environment  
orchestrate connections set-credentials -a gg_calendar_adk --env live \
  -e "GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID" \
  -e "GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET" \
  -e "GOOGLE_REDIRECT_URI=$GOOGLE_REDIRECT_URI" \
  -e "MCP_SERVER_NAME=$MCP_SERVER_NAME" \
  -e "MCP_SERVER_VERSION=$MCP_SERVER_VERSION"