#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { getCalendarClient } from "./auth.js";
import { calendar_v3 } from "googleapis";

// Define a type for our calendar client
type CalendarClient = calendar_v3.Calendar;

// Create server instance
const server = new McpServer({
  name: "google-calendar",
  version: "1.0.0",
  capabilities: {
    resources: {},
    tools: {},
  },
});

// Helper to format date to ISO string
function formatDateToISO(date: Date): string {
  return date.toISOString();
}

// Helper to format event to readable text
function formatEvent(event: calendar_v3.Schema$Event): string {
  const startTime = event.start?.dateTime || event.start?.date || 'Unknown';
  const endTime = event.end?.dateTime || event.end?.date || 'Unknown';
  
  return [
    `Title: ${event.summary || 'Untitled Event'}`,
    `When: ${new Date(startTime).toLocaleString()} - ${new Date(endTime).toLocaleString()}`,
    `Location: ${event.location || 'No location specified'}`,
    `Description: ${event.description || 'No description provided'}`,
    `Attendees: ${event.attendees?.map(a => a.email).join(', ') || 'None'}`,
    `Status: ${event.status || 'Unspecified'}`,
    `Calendar ID: ${event.organizer?.email || 'primary'}`,
    `Event ID: ${event.id || 'Unknown'}`,
    "---",
  ].join("\n");
}

// Register calendar tools

// 1. Get upcoming events
server.tool(
  "list-events",
  "List upcoming calendar events",
  {
    maxResults: z.number().min(1).max(100).default(10)
      .describe("Maximum number of events to return"),
    timeMin: z.string().optional()
      .describe("Start time in ISO format (defaults to now)"),
    calendarId: z.string().default("primary")
      .describe("Calendar ID to fetch events from"),
  },
  async ({ maxResults, timeMin, calendarId }) => {
    try {
      const calendar = await getCalendarClient();
      
      const response = await calendar.events.list({
        calendarId,
        timeMin: timeMin || formatDateToISO(new Date()),
        maxResults,
        singleEvents: true,
        orderBy: "startTime",
      });

      const events = response.data.items || [];
      
      if (events.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: "No upcoming events found.",
            },
          ],
        };
      }

      const formattedEvents = events.map(formatEvent);
      const eventsText = `Upcoming events:\n\n${formattedEvents.join("\n")}`;

      return {
        content: [
          {
            type: "text",
            text: eventsText,
          },
        ],
      };
    } catch (error) {
      console.error("Error fetching events:", error);
      return {
        content: [
          {
            type: "text",
            text: `Failed to retrieve events: ${(error as Error).message}`,
          },
        ],
      };
    }
  }
);

// 2. Create new event
server.tool(
  "create-event",
  "Create a new calendar event",
  {
    summary: z.string().describe("Title of the event"),
    location: z.string().optional().describe("Location of the event"),
    description: z.string().optional().describe("Description of the event"),
    startTime: z.string().describe("Start time in ISO format"),
    endTime: z.string().describe("End time in ISO format"),
    attendees: z.array(z.string()).optional().describe("Email addresses of attendees"),
    calendarId: z.string().default("primary").describe("Calendar ID to create event in"),
  },
  async ({ summary, location, description, startTime, endTime, attendees, calendarId }) => {
    try {
      const calendar = await getCalendarClient();
      
      const event: calendar_v3.Schema$Event = {
        summary,
        location,
        description,
        start: {
          dateTime: startTime,
          timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        },
        end: {
          dateTime: endTime,
          timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        },
        attendees: attendees?.map(email => ({ email })),
      };

      const response = await calendar.events.insert({
        calendarId,
        requestBody: event,
        sendUpdates: "all",
      });

      return {
        content: [
          {
            type: "text",
            text: `Event created successfully!\n\n${formatEvent(response.data)}`,
          },
        ],
      };
    } catch (error) {
      console.error("Error creating event:", error);
      return {
        content: [
          {
            type: "text",
            text: `Failed to create event: ${(error as Error).message}`,
          },
        ],
      };
    }
  }
);

// 3. Delete an event
server.tool(
  "delete-event",
  "Delete a calendar event",
  {
    eventId: z.string().describe("ID of the event to delete"),
    calendarId: z.string().default("primary").describe("Calendar ID containing the event"),
  },
  async ({ eventId, calendarId }) => {
    try {
      const calendar = await getCalendarClient();
      
      await calendar.events.delete({
        calendarId,
        eventId,
        sendUpdates: "all",
      });

      return {
        content: [
          {
            type: "text",
            text: `Successfully deleted event with ID: ${eventId}`,
          },
        ],
      };
    } catch (error) {
      console.error("Error deleting event:", error);
      return {
        content: [
          {
            type: "text",
            text: `Failed to delete event: ${(error as Error).message}`,
          },
        ],
      };
    }
  }
);

// 4. Update an event
server.tool(
  "update-event",
  "Update an existing calendar event",
  {
    eventId: z.string().describe("ID of the event to update"),
    summary: z.string().optional().describe("New title of the event"),
    location: z.string().optional().describe("New location of the event"),
    description: z.string().optional().describe("New description of the event"),
    startTime: z.string().optional().describe("New start time in ISO format"),
    endTime: z.string().optional().describe("New end time in ISO format"),
    attendees: z.array(z.string()).optional().describe("Updated email addresses of attendees"),
    calendarId: z.string().default("primary").describe("Calendar ID containing the event"),
  },
  async ({ eventId, summary, location, description, startTime, endTime, attendees, calendarId }) => {
    try {
      const calendar = await getCalendarClient();
      
      // First get the current event
      const eventResponse = await calendar.events.get({
        calendarId,
        eventId,
      });
      
      const currentEvent = eventResponse.data;
      
      // Update fields that were provided
      const updatedEvent: calendar_v3.Schema$Event = {
        ...currentEvent,
        summary: summary || currentEvent.summary,
        location: location || currentEvent.location,
        description: description || currentEvent.description,
      };
      
      // Update start and end times if provided
      if (startTime) {
        updatedEvent.start = {
          dateTime: startTime,
          timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        };
      }
      
      if (endTime) {
        updatedEvent.end = {
          dateTime: endTime,
          timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        };
      }
      
      // Update attendees if provided
      if (attendees) {
        updatedEvent.attendees = attendees.map(email => ({ email }));
      }

      const response = await calendar.events.update({
        calendarId,
        eventId,
        requestBody: updatedEvent,
        sendUpdates: "all",
      });

      return {
        content: [
          {
            type: "text",
            text: `Event updated successfully!\n\n${formatEvent(response.data)}`,
          },
        ],
      };
    } catch (error) {
      console.error("Error updating event:", error);
      return {
        content: [
          {
            type: "text",
            text: `Failed to update event: ${(error as Error).message}`,
          },
        ],
      };
    }
  }
);

// 5. Check availability for a given time period
server.tool(
  "check-availability",
  "Check calendar availability for a given time period",
  {
    startTime: z.string().describe("Start time in ISO format"),
    endTime: z.string().describe("End time in ISO format"),
    calendarIds: z.array(z.string()).default(["primary"]).describe("Calendar IDs to check"),
  },
  async ({ startTime, endTime, calendarIds }) => {
    try {
      const calendar = await getCalendarClient();
      
      const response = await calendar.freebusy.query({
        requestBody: {
          timeMin: startTime,
          timeMax: endTime,
          items: calendarIds.map(id => ({ id })),
        },
      });

      const calendars = response.data.calendars || {};
      let availabilityText = "Availability check results:\n\n";
      
      for (const calendarId of calendarIds) {
        const calendarData = calendars[calendarId];
        if (!calendarData) {
          availabilityText += `Calendar ${calendarId}: Unable to check\n`;
          continue;
        }
        
        const busySlots = calendarData.busy || [];
        if (busySlots.length === 0) {
          availabilityText += `Calendar ${calendarId}: Available for the entire period\n`;
        } else {
          availabilityText += `Calendar ${calendarId}: Busy during the following times:\n`;
          busySlots.forEach(slot => {
            const start = new Date(slot.start || '').toLocaleString();
            const end = new Date(slot.end || '').toLocaleString();
            availabilityText += `- ${start} to ${end}\n`;
          });
        }
        availabilityText += "\n";
      }

      return {
        content: [
          {
            type: "text",
            text: availabilityText,
          },
        ],
      };
    } catch (error) {
      console.error("Error checking availability:", error);
      return {
        content: [
          {
            type: "text",
            text: `Failed to check availability: ${(error as Error).message}`,
          },
        ],
      };
    }
  }
);

// Main function to run the server
async function main() {
  console.error("Starting Google Calendar MCP Server...");
  
  // Use StdioServerTransport for local testing
  const transport = new StdioServerTransport();
  
  try {
    // Try to authorize early to prompt for auth if needed
    await getCalendarClient();
    console.error("Successfully authenticated with Google Calendar API");
    
    // Connect the server to the transport
    await server.connect(transport);
    console.error("Google Calendar MCP Server running on stdio");
  } catch (error) {
    console.error("Error starting server:", error);
    process.exit(1);
  }
}

// Run the main function
main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});