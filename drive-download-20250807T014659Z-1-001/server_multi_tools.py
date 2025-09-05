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


mcp = FastMCP("Email/Weather/GoogleSearch", port=8001)

#google search
@mcp.tool()
async def google_search(input: str) -> str:
    '''Use the Google Search API to conduct a search (only when the agent cannot answer using its existing knowledge), and return the results'''
    print('[Google Search tool used]: Search query is', input)

    # 從環境變數讀取金鑰
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cse_id = os.getenv("GOOGLE_CSE_ID")

    if not google_api_key or not google_cse_id:
        return "[錯誤] 未設定 GOOGLE_API_KEY 或 GOOGLE_CSE_ID 環境變數"

    search = GoogleSearchAPIWrapper(
    google_api_key = google_api_key,
    google_cse_id = google_cse_id
    )
    result = search.run(input)
    return result

#撰寫郵件草稿
@mcp.tool()
async def prepare_email(username: str, subject: str, message: str) -> str:
    """預覽電子郵件內容，請使用者確認是否寄出"""
    email_preview = (
        "[📨 Email Preview]\n"
        f"To: {username}\n"
        f"Subject: {subject}\n"
        "-------------------------\n"
        f"{message}\n"
        "-------------------------\n"
        "請確認是否要寄出此郵件。若需要修改內容，請直接說明修改內容；若要寄出，請說『是』。"
    )
    print("[Email preview created]")
    return email_preview

#請使用者確認郵件資訊並寄出
@mcp.tool()
async def confirm_send_email(receiver_email: str, subject: str, message: str) -> str:
    """在使用者確認後，實際發送郵件"""
    print('[Send email tool used] Recipient email:', receiver_email)
    print(f"To: {receiver_email}\nMessage:\n{message}")

    # 從環境變數讀取金鑰
    app_password = os.getenv("APP_PASSWORD")

    # 信件內容設定
    sender_email = "vywntnu@gmail.com"
    app_password = app_password

    # 使用 UTF-8 編碼建立郵件
    message = MIMEText(message, "plain", "utf-8")
    message["Subject"] = Header(subject, "utf-8")
    message["From"] = sender_email
    message["To"] = receiver_email

    # 建立與 Gmail SMTP 的安全連線
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, [receiver_email], message.as_string())
        print("✅ 郵件已成功寄出！")
        return f"✅ 郵件已成功寄出給 {receiver_email}!"
    except Exception as e:
        print("❌ 郵件寄出失敗：", e)
        return f"❌ 郵件寄出失敗：{e}"

#查詢天氣 
@mcp.tool()
async def get_weather(city: str) -> str:
    """查詢指定城市的即時天氣，顯示溫度與天氣狀況"""
    try:
        # 使用 Open-Meteo 的地理座標 API 取得城市的緯經度
        geo_resp = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "zh", "format": "json"}
        )
        geo_data = geo_resp.json()
        if "results" not in geo_data or not geo_data["results"]:
            return f"❌ 找不到城市 {city}，請確認名稱是否正確。"

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        location_name = geo_data["results"][0]["name"]

        # 查詢即時天氣
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
        desc = f"{weather.get('weathercode', '未知代碼')}"
        wind = weather.get("windspeed")

        return (
            f"🌤️ {location_name} 的即時天氣：\n"
            f"溫度：{temp}°C\n"
            f"風速：{wind} km/h\n"
            f"天氣代碼：{desc}（可參考對照表）"
        )
    except Exception as e:
        return f"⚠️ 查詢過程中發生錯誤：{e}"

#郵件摘要
#允許應用程式讀取使用者 Gmail 中的所有郵件，但不能修改、刪除、寄信
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

@mcp.tool()
async def fetch_inbox(n: int = 5) -> str:
    """讀取 Gmail 收件匣，取得最近 N 封郵件的寄件人、主旨與簡要內容"""
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
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(無主旨)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(無寄件人)')

        snippet = msg_detail.get('snippet', '')

        summary_list.append(f"📨 {subject}\nFrom: {sender}\nSummary: {snippet}\n")

    return "\n\n".join(summary_list) if summary_list else "📭 沒有找到信件。"

if __name__ == "__main__":

    mcp.run(transport="streamable-http")
