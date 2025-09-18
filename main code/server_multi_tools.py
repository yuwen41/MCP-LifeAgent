import smtplib
import requests
import json
import time
import httpx
import os.path
import os
import base64
from typing import List
from mcp.server.fastmcp import FastMCP
from email.mime.text import MIMEText
from email.header import Header
from typing import List, Dict, Any
from langchain_community.utilities import GoogleSearchAPIWrapper
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


mcp = FastMCP("Email/Calendar/Weather/GoogleSearch", port=8001)

#google search
@mcp.tool()
async def google_search(input: str) -> str:
    '''Use the Google Search API to conduct a search (only when the agent cannot answer using its existing knowledge), and return the results'''
    print('[Google Search tool used]: Search query is', input)

    # Read the key from the environment variable
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cse_id = os.getenv("GOOGLE_CSE_ID")

    if not google_api_key or not google_cse_id:
        return "[Error] GOOGLE_API_KEY or GOOGLE_CSE_ID environment variable not set"

    search = GoogleSearchAPIWrapper(
    google_api_key = google_api_key,
    google_cse_id = google_cse_id
    )
    result = search.run(input)
    return result

#Draft an email
@mcp.tool()
async def prepare_email(username: str, subject: str, message: str) -> str:
    """Preview the email content and ask the user to confirm before sending"""
    email_preview = (
        "[📨 Email Preview]\n"
        f"To: {username}\n"
        f"Subject: {subject}\n"
        "-------------------------\n"
        f"{message}\n"
        "-------------------------\n"
        "Please confirm whether you want to send this email. If you need to modify the content, please specify the changes; if you want to send it, please say 'Yes'."
    )
    print("[Email preview created]")
    return email_preview

#Please confirm the email information and send it
@mcp.tool()
async def confirm_send_email(receiver_email: str, subject: str, message: str) -> str:
    """Send the email after user confirmation"""
    print('[Send email tool used] Recipient email:', receiver_email)
    print(f"To: {receiver_email}\nMessage:\n{message}")

    # Read the key from the environment variable
    app_password = os.getenv("APP_PASSWORD")

    # Email content configuration
    sender_email = "set your email address"
    app_password = app_password

    # Create the email using UTF-8 encoding
    message = MIMEText(message, "plain", "utf-8")
    message["Subject"] = Header(subject, "utf-8")
    message["From"] = sender_email
    message["To"] = receiver_email

    # Establish a secure connection with Gmail SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, [receiver_email], message.as_string())
        print("✅ Email sent successfully!")
        return f"✅Email successfully sent to {receiver_email}!"
    except Exception as e:
        print("❌ Failed to send email：", e)
        return f"❌ Failed to send email：{e}"

#Query weather 
@mcp.tool()
async def get_weather(city: str) -> str:
    """Fetch real-time weather for a specified city, displaying temperature and conditions"""
    try:
        # Use Open-Meteo's geolocation API to get the latitude and longitude of the city
        geo_resp = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "zh", "format": "json"}
        )
        geo_data = geo_resp.json()
        if "results" not in geo_data or not geo_data["results"]:
            return f"❌City {city} not found. Please check if the name is correct."

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        location_name = geo_data["results"][0]["name"]

        # Query real-time weather
        weather_resp = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "timezone": "Asia/Taipei"
            }
        )
        weather_data = weather_resp.json()
        weather = weather_data.get("current_weather", {})
        temp = weather.get("temperature")
        desc = f"{weather.get('weathercode', 'Unknown code')}"
        wind = weather.get("windspeed")

        return (
            f"🌤️ {location_name} 's real-time weather：\n"
            f"Temperature：{temp}°C\n"
            f"Wind speed：{wind} km/h\n"
            f"Weather code：{desc} (see reference table)"
        )
    except Exception as e:
        return f"⚠️ An error occurred during the query：{e}"

#Email summary
#Allows to read all emails in the user's Gmail, but not modify, delete or send
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

@mcp.tool()
async def fetch_inbox(n: int = 5) -> str:
    """Read the Gmail inbox and retrieve sender, subject, and brief content of the most recent N emails"""
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', maxResults=n).execute()
    messages = results.get('messages', [])

    summary_list = []

    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_detail['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(No sender')

        snippet = msg_detail.get('snippet', '')

        summary_list.append(f"📨 {subject}\nFrom: {sender}\nSummary: {snippet}\n")

    return "\n\n".join(summary_list) if summary_list else "📭 No emails found."

#calendar
SCOPES_CALENDAR = ['https://www.googleapis.com/auth/calendar']


# Add event on Google Calendar
@mcp.tool()
async def quick_add_event(
    text: str,
    calendar_id: str | None = None,
) -> str:
    
    try:
        cal_id = calendar_id or os.getenv("CALENDAR_ID", "primary")
        creds = get_google_creds(SCOPES_CALENDAR, 'token_calendar.json')
        service = build('calendar', 'v3', credentials=creds)


        event = service.events().quickAdd(calendarId=cal_id, text=text).execute()
        event_id = event.get("id", "")
        summary = event.get("summary", "(No title)")
        link = event.get("htmlLink", "")
        start = (event.get("start") or {}).get("dateTime") or (event.get("start") or {}).get("date")
        end = (event.get("end") or {}).get("dateTime") or (event.get("end") or {}).get("date")


        return {
                "status": "success",
                "event_id": event_id,
                "summary": summary,
                "start": start,
                "end": end,
                "link": link,
                "text": (
                    "✅ QuickAdd created\n"
                    f"🆔 Event ID: {event_id}\n"
                    f"🗓 {summary}\n"
                    f"   Start: {start}\n"
                    f"   End:   {end}\n"
                    f"🔗 {link}"
                )
            }




    except Exception as e:
        return f"❌ QuickAdd failed: {e}"

# Delete event on Google Calendar
@mcp.tool()
async def delete_event(event_id: str, calendar_id: str | None = None) -> str:
    try:
        cal_id = calendar_id or os.getenv("CALENDAR_ID", "primary")


        creds = get_google_creds(SCOPES_CALENDAR, 'token_calendar.json')
        service = build('calendar', 'v3', credentials=creds)


        service.events().delete(calendarId=cal_id, eventId=event_id).execute()
        return f"🗑️ Event deleted (Event ID: {event_id})"


    except Exception as e:
        return f"❌ Delete failed：{e}"


if __name__ == "__main__":

    mcp.run(transport="streamable-http")




