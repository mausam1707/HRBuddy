from botbuilder.core import ActivityHandler, TurnContext
from office365.runtime.auth.user_credential import UserCredential
from ollama_llm import OllamaLLM
from data_connectors import DataConnector
from config import SHAREPOINT_SITE_URL, DOCUMENTS_DIR, OLLAMA_BASE_URL, DEFAULT_MODEL
import os

class TeamsBot(ActivityHandler):
    def __init__(self):
        super().__init__()
        self.ollama_llm = OllamaLLM(OLLAMA_BASE_URL, DEFAULT_MODEL)
        self.data_connector = DataConnector(
            SHAREPOINT_SITE_URL, 
            UserCredential(
                os.getenv("SHAREPOINT_USER", "your_username"), 
                os.getenv("SHAREPOINT_PASS", "your_password")
            )
        )

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text

        # Load custom documents as context
        context_docs = await self.data_connector.load_custom_documents()

        # Query Ollama
        response = await self.ollama_llm.query(user_message, context_docs)

        # Send response back to user
        await turn_context.send_activity(f"**Response:**\n{response}")

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hello! I'm your IT/HR assistant. Ask me anything!"
                )
