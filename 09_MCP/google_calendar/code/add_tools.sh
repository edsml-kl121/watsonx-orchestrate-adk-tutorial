orchestrate toolkits import \
  --kind=mcp \
  --name=mcp-ggcal-adk \
  --description="google calendar Servers" \
  --package-root="." \
  --language=node \
  --tools="*" \
  --command='["npx", "ts-node", "src/index.ts", "--transport", "stdio"]' \
  --app-id "gg_calendar_adk"