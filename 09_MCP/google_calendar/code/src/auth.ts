import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the directory name
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Path to token storage
const TOKEN_PATH = path.join(__dirname, '..', 'token.json');
const CREDENTIALS_PATH = path.join(__dirname, '..', 'credentials.json');

// If modifying these scopes, delete token.json.
const SCOPES = [
  'https://www.googleapis.com/auth/calendar',
  'https://www.googleapis.com/auth/calendar.events'
];

/**
 * Load or request authorization to call Google Calendar APIs.
 */
export async function authorize() {
  console.error('Starting authentication process...');
  console.error(`Looking for credentials at: ${CREDENTIALS_PATH}`);
  console.error(`Credentials file exists: ${fs.existsSync(CREDENTIALS_PATH)}`);
  
  if (!fs.existsSync(CREDENTIALS_PATH)) {
    console.error('ERROR: credentials.json not found!');
    console.error('Please download OAuth credentials from Google Cloud Console and save them as credentials.json in the project root.');
    throw new Error('credentials.json not found');
  }
  
  let credentials: any;
  try {
    // Load client secrets from credentials file
    const content = fs.readFileSync(CREDENTIALS_PATH, 'utf8');
    console.error('Successfully read credentials file');
    
    try {
      credentials = JSON.parse(content);
      console.error('Successfully parsed credentials JSON');
    } catch (jsonError) {
      console.error('Failed to parse credentials.json as JSON:');
      console.error(jsonError);
      throw new Error('Invalid JSON in credentials.json');
    }
  } catch (err) {
    console.error('Error loading client secret file:', err);
    throw new Error('Failed to load credentials');
  }

  // Check if credentials have the expected format
  const hasInstalled = !!credentials.installed;
  const hasWeb = !!credentials.web;
  
  console.error(`Credentials has 'installed' property: ${hasInstalled}`);
  console.error(`Credentials has 'web' property: ${hasWeb}`);
  
  if (!hasInstalled && !hasWeb) {
    console.error('ERROR: Invalid credentials format. Missing both "installed" and "web" properties.');
    console.error('Available keys:', Object.keys(credentials));
    throw new Error('Invalid credentials format');
  }

  const clientConfig = credentials.installed || credentials.web;
  if (!clientConfig.client_id || !clientConfig.client_secret || !clientConfig.redirect_uris) {
    console.error('ERROR: Missing required credential properties');
    console.error('Available properties:', Object.keys(clientConfig));
    throw new Error('Missing required credential properties');
  }
  
  const { client_secret, client_id, redirect_uris } = clientConfig;
  
  if (!Array.isArray(redirect_uris) || redirect_uris.length === 0) {
    console.error('ERROR: redirect_uris must be a non-empty array');
    console.error(`redirect_uris: ${JSON.stringify(redirect_uris)}`);
    throw new Error('Invalid redirect_uris');
  }
  
  console.error('Creating OAuth2 client...');
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

  // Check if we have previously stored a token
  console.error(`Checking for token at: ${TOKEN_PATH}`);
  console.error(`Token file exists: ${fs.existsSync(TOKEN_PATH)}`);
  
  try {
    if (fs.existsSync(TOKEN_PATH)) {
      console.error('Found existing token, attempting to use it');
      const token = fs.readFileSync(TOKEN_PATH, 'utf8');
      
      try {
        const tokenData = JSON.parse(token);
        console.error('Successfully parsed token JSON');
        oAuth2Client.setCredentials(tokenData);
        return oAuth2Client;
      } catch (jsonError) {
        console.error('Failed to parse token.json as JSON, will need to get new token:');
        console.error(jsonError);
        // Continue to getAccessToken
      }
    } else {
      console.error('No existing token found, will request new one');
    }
    
    return await getAccessToken(oAuth2Client);
  } catch (err) {
    console.error('Error handling token:', err);
    throw err;
  }
}

/**
 * Get and store new token after prompting for user authorization
 */
async function getAccessToken(oAuth2Client: any) {
  try {
    console.error('Generating authorization URL...');
    const authUrl = oAuth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: SCOPES,
    });
    
    console.error('\n===========================================================');
    console.error('Authorize this app by visiting this url:');
    console.error(authUrl);
    console.error('\nAfter authorization, copy the code from the browser and paste it below:');
    console.error('===========================================================\n');
    
    // We need to wait for user input
    console.error('Waiting for authorization code input...');
    const code = await new Promise<string>((resolve) => {
      process.stdin.once('data', (data) => {
        const input = data.toString().trim();
        console.error(`Received input of length: ${input.length}`);
        resolve(input);
      });
    });

    try {
      console.error('Getting token from authorization code...');
      const { tokens } = await oAuth2Client.getToken(code);
      console.error('Successfully retrieved access token');
      
      oAuth2Client.setCredentials(tokens);
      
      // Store the token to disk for later program executions
      try {
        fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens));
        console.error('Token stored to', TOKEN_PATH);
      } catch (writeErr) {
        console.error('Error writing token to file:', writeErr);
        // Continue anyway since we have the token in memory
      }
      
      return oAuth2Client;
    } catch (err) {
      console.error('Error retrieving access token:', err);
      throw new Error(`Failed to retrieve access token: ${(err instanceof Error ? err.message : String(err))}`);
    }
  } catch (err) {
    console.error('Error in getAccessToken:', err);
    throw err;
  }
}

/**
 * Create and return the Calendar API client
 */
export async function getCalendarClient() {
  try {
    console.error('Getting OAuth2 client...');
    const auth = await authorize();
    console.error('Successfully obtained authorized client');
    return google.calendar({ version: 'v3', auth });
  } catch (err) {
    console.error('Failed to get Calendar client:', err);
    throw err;
  }
}