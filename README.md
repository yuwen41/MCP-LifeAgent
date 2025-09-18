# 🚀 OmniAssist Project Guide

OmniAssist is an AI-powered assistant that integrates multiple tools into one system. It is designed to streamline information retrieval, communication, and productivity.

## ✨ Core Features

1. Google Search Integration

   - Perform real-time web searches using Google’s Custom Search API.

   - Retrieve accurate and up-to-date information directly from the internet.

2. Weather Information

   - Get current weather conditions and forecasts.

   - Useful for quick daily updates or travel planning.

3. Email Drafting & Sending

   - Automatically generate well-structured email drafts.

   - Send emails directly through Gmail using a secure App Password.

4. Email Summarization

   - Fetch received emails and summarize their content.

   - Helps users quickly understand the main points without reading full messages.

5. Managing Events on Google Calendar (Add & Delete)
   
   - Add a new event to Google Calendar
  
   - Delete an event from your Google Calendar

---

## 📂 Project Structure

- **`mcp_agent.py`**  
  Setup for creating the MCP agent *(you do not need to run this file)*  

- **`mcp_client.py`**  
  Main entry point for using the AI agent *(you need to run this file)*  
  1. Open a terminal and enter `wsl`  
  2. Set your OpenAI API key:  
     ```bash
     export OPENAI_API_KEY=''
     ```  
  3. Run the client:  
     ```bash
     python3 mcp_client.py
     ```

- **`server_multi_tools.py`**  
  Defines the tools available for the AI agent *(you need to run this file)*  
  1. Open a terminal and enter `wsl`  
  2. Set the following environment variables:  
     ```bash
     export GOOGLE_API_KEY=''
     export GOOGLE_CSE_ID=''
     export APP_PASSWORD=''
     ```  
  3. Set your Gmail address inside the `sender_email` field of the script.

---

## 🛠️ User Setup Guide

Before running the project, ensure the following:

1. **Install Python and Dependencies**  
   - Download Python from: [python.org/downloads](https://www.python.org/downloads/)
   - Download dependencies
     ```bash
     pip install -r requirements.txt
     ```

2. **OpenAI API Key**  
   - Get your key from: [OpenAI API](https://openai.com/api/)

3. **Google API Key (for Google Search)**  
   - Go to **Google Cloud Console**  
   - Navigate: **APIs & Services → Enabled APIs & services**  
   - Click **+ ENABLE APIS AND SERVICES**  
   - Search **Custom Search API** → **Enable**  
   - Click **Try this API** → **Get a Key**  

4. **Google CSE ID (Custom Search Engine)**  
   - Visit: [Programmable Search Engine](https://programmablesearchengine.google.com/about/)  
   - Click **Get started**  
   - Create your first search engine → obtain **CSE ID**

5. **Gmail App Password (for sending emails)**  
   - Enable **2-Step Verification**  
     - Go to: [Google Security Settings](https://myaccount.google.com/security)  
     - Enable **2-Step Verification**
     - Follow the instructions to turn it on
   - Generate an **App Password**  
     - Go to: [Google App Passwords](https://myaccount.google.com/apppasswords)  
     - Select **App: Mail**, **Device: Other (Custom name)** → type something like *PythonScript*  
     - Copy the generated 16-character App Password  

6. **`credentials.json` (shared OAuth tools for Google Calendar and Gmail)**
   - Gmail
     - Go to **Google Cloud Console**  
     - Navigate: **APIs & Services → Library**  
     - Search **Gmail API** → **Enable**  
     - Create **OAuth Client ID** → Select **Desktop app**  
     - Download the generated **`credentials.json`** file  
     - Place it in the same directory as `server_multi_tools.py`
   - Google Calendar
     - Go to **Google Cloud Console**  
     - Navigate: **APIs & Services → Library**  
     - Search **Gmail API** → **Enable**  
     - Create **OAuth Client ID** → Select **Desktop app**  
     - As you already downloaded  **`credentials.json`** file during the Gmail setup, you don’t need to download it again

7. **`token_gmail.json` (for Gmail)**  
   - When you run a Gmail-related tool for the first time, the authorization URL will be displayed in the output of **server_multi_tool.py**
   - You need to copy and paste the authorization URL into a browser and enter the verification code
   - Once authorization is complete, a **`token_gmail.json`** file will be generated in your project directory
   - For subsequent runs, the program will automatically use this file for authentication, so you won’t need to log in again
  
8. **`token_calendar.json` (for Google Calendar)**  
   - When you run a Calendar-related tool for the first time, the authorization URL will be displayed in the output of **server_multi_tool.py**
   - You need to copy and paste the authorization URL into a browser and enter the verification code
   - Once authorization is complete, a **`token_calendar.json`** file will be generated in your project directory
   - For subsequent runs, the program will automatically use this file for authentication, so you won’t need to log in again

---

✅ You’re now ready to run the MCP Agent with Google Search and Gmail integration!
