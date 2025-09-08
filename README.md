# 🚀 MCP Agent Project Guide

This repository contains the setup for an MCP (Model Context Protocol) agent, client, and multi-tool server.

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

1. **Install Python**  
   - Download from: [python.org/downloads](https://www.python.org/downloads/)  
   - Install dependencies:  
     ```bash
     pip install -r requirements.txt
     ```

2. **Install WSL (Windows Subsystem for Linux)**  
   - Open terminal  
   - Run:  
     ```bash
     wsl --install
     ```  
   - [WSL official installation guide](https://learn.microsoft.com/en-us/windows/wsl/install)

3. **OpenAI API Key**  
   - Get your key from: [OpenAI API](https://openai.com/api/)

4. **Google API Key (for Google Search)**  
   - Go to **Google Cloud Console**  
   - Navigate: **APIs & Services → Enabled APIs & services**  
   - Click **+ ENABLE APIS AND SERVICES**  
   - Search **Custom Search API** → **Enable**  
   - Click **Try this API** → **Get a Key**  

5. **Google CSE ID (Custom Search Engine)**  
   - Visit: [Programmable Search Engine](https://programmablesearchengine.google.com/about/)  
   - Click **Get started**  
   - Create your first search engine → obtain **CSE ID**

6. **Gmail App Password (for sending emails)**  
   - Enable **2-Step Verification**  
     - Go to: [Google Security Settings](https://myaccount.google.com/security)  
     - Enable **2-Step Verification**  
   - Generate an **App Password**  
     - Go to: [Google App Passwords](https://myaccount.google.com/apppasswords)  
     - Select **App: Mail**, **Device: Other (Custom name)** → e.g., *PythonScript*  
     - Copy the generated 16-character App Password  

7. **`credentials.json` (for Gmail summarization)**  
   - Go to **Google Cloud Console**  
   - Navigate: **APIs & Services → Library**  
   - Search **Gmail API** → **Enable**  
   - Create **OAuth Client ID** → Select **Desktop app**  
   - Download the generated **`credentials.json`** file  
   - Place it in the same directory as `server_multi_tools.py`

8. **`token.json` (for Gmail summarization)**  
   - This file will be **auto-generated** by the code in `server_multi_tools.py` upon first authentication.

---

✅ You’re now ready to run the MCP Agent with Google Search and Gmail integration!
