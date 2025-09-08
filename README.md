🌐 MCP Agent

An AI Agent powered by MCP (Model Context Protocol) that integrates multiple tools, including OpenAI, Google Search, and Gmail.

This repository contains the setup for the MCP agent, client, and multi-tool server.

📂 Project Structure

mcp_agent.py
Setup file for creating the MCP agent (no need to run this file directly).

mcp_client.py
Main entry point to use the AI agent.

Run this file to interact with the MCP Agent.

server_multi_tools.py
Defines the tools available to the AI agent.

Run this file to enable Google Search and Gmail tools.

⚙️ Installation & Setup
1. Install WSL (Windows Subsystem for Linux)

To use Linux tools on Windows:

wsl --install


👉 Official WSL installation guide

2. Install Python & Dependencies

Download Python: python.org/downloads

Install required dependencies:

pip install -r requirements.txt

3. Environment Variables

Before running the scripts, set up the following environment variables:

# OpenAI
export OPENAI_API_KEY="your_openai_api_key"

# Google Search
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_CSE_ID="your_google_cse_id"

# Gmail
export APP_PASSWORD="your_gmail_app_password"


Also set your Gmail address in sender_email inside server_multi_tools.py.

🔑 How to Get Keys & Credentials
1. OpenAI API Key

Get your API key: OpenAI API

2. Google API Key

Go to Google Cloud Console

Navigate to: APIs & Services → Enabled APIs & services

Click + ENABLE APIS AND SERVICES

Search for Custom Search API, enable it

Click Get a Key to generate your API key

3. Google CSE ID (Custom Search Engine)

Go to Google Programmable Search Engine

Click Get started → Create your first search engine!

Copy your CSE ID

4. Gmail App Password

Enable 2-Step Verification

Google Security Settings

Generate an App Password

Go to App Passwords

Choose App: Mail and Device: Other (Custom name)

Copy the 16-character password

5. Gmail API (for Email Summarization)
(a) Get credentials.json

In Google Cloud Console

Go to APIs & Services → Library

Search Gmail API, enable it

Create credentials → OAuth Client ID

Choose Desktop App as application type

Download credentials.json

Place it in the same folder as server_multi_tools.py

(b) Generate token.json

When you run server_multi_tools.py for the first time,
it will prompt you to authenticate and automatically generate token.json

🚀 Usage
Run MCP Client
# Open WSL
wsl

# Run client
python3 mcp_client.py

Run Multi-Tool Server
# Open WSL
wsl

# Run server
python3 server_multi_tools.py

✅ Summary

Install WSL and Python

Install dependencies (pip install -r requirements.txt)

Get API keys & credentials (OpenAI, Google, Gmail)

Run mcp_client.py (main client)

Run server_multi_tools.py (multi-tool server)
