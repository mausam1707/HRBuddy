IT/HR Assistant Bot
A Python-based Microsoft Teams bot that uses the Ollama LLM via LangChain to provide IT and HR assistance. The bot runs locally and uses ngrok to expose the local server, enabling testing with Microsoft Teams or Bot Framework Emulator without needing Azure portal access.

Features
AI-powered responses using Ollama LLM.
Runs locally with easy setup.
Uses ngrok for tunneling to expose local bot endpoint.
Compatible with Microsoft Teams and Bot Framework Emulator.
No Azure portal access required for local development.
Prerequisites
Python 3.8 or higher
ngrok installed
Ollama LLM installed and running locally (or accessible remotely)
Bot Framework Emulator (optional, for local testing)
Microsoft Teams (for real chat testing)
Setup and Usage
1. Clone the repository
git clone https://github.com/yourusername/it-hr-assistant-bot.git
cd it-hr-assistant-bot
2. Install dependencies
pip install -r requirements.txt
3. Configure the bot
In your bot configuration (e.g., config.py), leave Microsoft App ID and Password empty for local testing:
TEAMS_APP_ID = ""
TEAMS_APP_PASSWORD = ""
Ensure the Ollama model name in your bot code is correct:
from langchain.llms import Ollama

ollama_llm = Ollama(model="llama2")
4. Run your bot locally
python app.py
5. Start ngrok to expose your bot
ngrok http 3978
Copy the HTTPS forwarding URL (e.g., https://abcd1234.ngrok.io)
6. Connect Bot Framework Emulator or Microsoft Teams
In Bot Framework Emulator:

Open your bot
Use the endpoint: https://abcd1234.ngrok.io/api/messages
Leave App ID and Password blank
In Microsoft Teams:

If you have access to the Azure Bot registration, update the messaging endpoint to the ngrok URL + /api/messages
Otherwise, test with the Emulator as above
7. Test your bot
Send a message like "Hi"
The bot should reply with AI-generated text from Ollama
Example LLM Call Code Snippet
Make sure you extract the generated text properly from the Ollama response:

from langchain.llms import Ollama

ollama_llm = Ollama(model="llama2")

def get_bot_response(user_input: str) -> str:
    response = ollama_llm.generate(user_input)
    return response.generations[0].text
Common Errors and Troubleshooting
1. Error:
The bot is remote, but the service URL is localhost. Without tunneling software you will not receive replies.
Cause: Your bot is running locally but the service URL in incoming messages is localhost, which is unreachable remotely.

Fix:

Use ngrok to expose your bot publicly.
Run ngrok http 3978 and update your bot endpoint in Emulator or Teams to the ngrok URL.
Keep ngrok running during testing.
2. Error:
'OllamaLLM' object has no attribute 'query'
Cause: You are calling .query() on the Oll