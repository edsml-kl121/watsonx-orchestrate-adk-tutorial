# Google Calendar MCP Server

A powerful Model Context Protocol (MCP) server that integrates with Google Calendar to provide intelligent, context-aware calendar management capabilities.

## Features

- **Smart Calendar Management**
  - List and view upcoming events with detailed information
  - Create new events with custom titles, locations, and attendees
  - Update existing events with new information
  - Delete events from your calendar
  - Support for multiple calendars

- **Context-Aware Operations**
  - Maintains context between calendar operations
  - Intelligent event formatting and display
  - Secure authentication and token management
  - Robust error handling and validation

## Prerequisites

- Node.js (v16 or higher)
- Google Cloud Platform account
- Google Calendar API enabled
- OAuth 2.0 credentials from Google Cloud Console

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/google-calendar-mcp.git
   cd google-calendar-mcp
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```

4. Update the `.env` file with your Google Calendar API credentials:
   - `GOOGLE_CLIENT_ID`: Your Google Cloud Console client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google Cloud Console client secret
   - `GOOGLE_REDIRECT_URI`: Your configured redirect URI

5. Build the project:
   ```bash
   npm run build
   ```

6. Start the server:
   ```bash
   npm start
   ```

## Usage Examples

The MCP server supports various calendar operations through natural language commands:

### Event Listing
- "Show me my next 5 upcoming events"
- "List all events for next week"
- "What's on my calendar for tomorrow?"

### Event Creation
- "Schedule a meeting with John and Sarah tomorrow at 2pm"
- "Create a lunch event with the team next Friday at 12pm"
- "Add a doctor's appointment for next Monday at 10am"

### Event Updates
- "Move my 2pm meeting to 3pm"
- "Add Mike to tomorrow's team meeting"
- "Update the location of Friday's meeting"

### Event Deletion
- "Cancel my 3pm meeting today"
- "Remove the team lunch from next Friday"

## Security

- All credentials and tokens are stored securely and are not committed to version control
- OAuth 2.0 authentication ensures secure access to Google Calendar
- Environment variables are used for sensitive configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

