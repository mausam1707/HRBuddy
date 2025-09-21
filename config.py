import os

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')  # Default local Ollama server
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gemma:2b')  # Current model: Gemma:2b

# Bot Configuration
BOT_PORT = int(os.getenv('BOT_PORT', 3978))  # Default port for the bot server (e.g., for Emulator)

# Microsoft Teams Configuration (for later deployment)
TEAMS_APP_ID = os.getenv('TEAMS_APP_ID', 'your_bot_id')  # Placeholder for now
TEAMS_APP_PASSWORD = os.getenv('TEAMS_APP_PASSWORD', 'your_bot_password')  # Placeholder for now

# Data and SharePoint Configuration
DOCUMENTS_DIR = os.getenv('DOCUMENTS_DIR', './documents')  # Folder for .pdf/.txt/.docx files
SHAREPOINT_SITE_URL = os.getenv('SHAREPOINT_SITE_URL', 'https://yourcompany.sharepoint.com/sites/yoursite')  # Update if needed

# config.py
TEAMS_APP_ID = ""  # e.g., "test_app_id"
TEAMS_APP_PASSWORD = ""  # e.g., "test_password"
BOT_PORT = 3978
SHAREPOINT_SITE_URL = "https://yourcompany.sharepoint.com"  # e.g., "https://yourcompany.sharepoint.com"
DOCUMENTS_DIR = r"D:\Agent\documents"  # e.g., "./documents"

