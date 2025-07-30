orchestrate toolkits import \
  --kind=mcp \
  --name=mcp-airbnb-adk \
  --description="Airbnb Servers" \
  --package="@openbnb/mcp-server-airbnb" \
  --language=node \
  --tools="airbnb_search,airbnb_listing_details" \
  --command='["npx", "-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"]'