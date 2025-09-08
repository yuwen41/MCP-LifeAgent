# Langchain_FastMCP

## 🚀 mcp_agent

An AI Agent powered by MCP (Model Context Protocol) that integrates multiple tools including OpenAI, Google Search, and Gmail.  
This repository contains the setup for the MCP agent, client, and multi-tool server.

---

## 📂 Project Structure

- **mcp_agent.py**  
  Setup for creating the MCP agent *(you do not need to run this file)*  

- **mcp_client.py**  
  Main entry point to use the AI agent *(you need to run this file)*  

- **server_multi_tools.py**  
  Defines the tools that can be used by the AI agent *(you need to run this file)*  

---

## ⚙️ Installation & Setup

### 1. Install WSL (Windows Subsystem for Linux)
To access the power of both Windows and Linux on a Windows machine:

```bash
wsl --install
📖 WSL official installation guide

### 2. Install Python
Download and install Python from: python.org/downloads

Then, in your project directory, install required dependencies:

bash
Copy code
pip install -r requirements.txt
### 3. Environment Variables
You can either export them manually in terminal, or use a .env file for convenience.

Manual Export (WSL terminal)
bash
Copy code
export OPENAI_API_KEY="your_api_key_here"
export GOOGLE_API_KEY="your_google_api_key_here"
export GOOGLE_CSE_ID="your_cse_id_here"
export APP_PASSWORD="your_generated_app_password_here"
.env.example (recommended)
Create a file named .env.example (copy it to .env and fill in your values):

### ini
Copy code
# .env.example

# OpenAI API Key (from https://openai.com/api/)
OPENAI_API_KEY=your_api_key_here

# Google Custom Search API Key
GOOGLE_API_KEY=your_google_api_key_here

# Google Custom Search Engine ID (CSE ID)
GOOGLE_CSE_ID=your_cse_id_here

# Gmail App Password (generated after enabling 2FA)
APP_PASSWORD=your_generated_app_password_here

# Gmail address used in server_multi_tools.py
SENDER_EMAIL=your_email@gmail.com
4. Gmail API (for email summarization)
4.1 Get credentials.json
In Google Cloud Console, search for Gmail API → Enable

Click Create Credentials → OAuth Client ID

Choose Desktop app as the application type

Download the credentials.json file

Place it in the same directory as server_multi_tools.py

4.2 Get token.json
token.json will be automatically generated when you run server_multi_tools.py for the first time.

It stores your OAuth authentication tokens.

▶️ Usage
Step 1: Run the Multi-Tool Server
Open a terminal (WSL) and run:

bash
Copy code
python3 server_multi_tools.py
Step 2: Run the MCP Client
Open another terminal (WSL) and run:

bash
Copy code
python3 mcp_client.py
✅ Quick Commands
Set environment variables manually:

bash
Copy code
export OPENAI_API_KEY="..."
export GOOGLE_API_KEY="..."
export GOOGLE_CSE_ID="..."
export APP_PASSWORD="..."
Run tools:

bash
Copy code
python3 server_multi_tools.py
Run AI agent:

bash
Copy code
python3 mcp_client.py
🛠 Requirements
Python 3.8+

WSL (for Windows users)

Packages in requirements.txt

Install all dependencies:

bash
Copy code
pip install -r requirements.txt
📌 Notes
Make sure WSL is installed and you are running commands inside WSL terminal.

API keys and credentials should remain private (do not commit them to GitHub).

mcp_agent.py is only for setup reference — you don’t need to run it directly.

Always copy .env.example → .env and update values before running.
