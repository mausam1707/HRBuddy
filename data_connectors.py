import asyncio
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from utils import logger, load_documents_from_directory
import os

class DataConnector:
    def __init__(self, site_url, credentials, documents_dir=None):
        self.site_url = site_url
        self.credentials = credentials
        self.ctx = ClientContext(site_url).with_credentials(credentials)
        self.documents_dir = documents_dir or os.getenv('DOCUMENTS_DIR', './documents')  # Local dir for files

    async def fetch_from_sharepoint(self, list_name):
        # Existing code remains
        try:
            list_obj = self.ctx.web.lists.get_by_title(list_name)
            items = list_obj.get_items().execute_query()
            return [item.properties for item in items]
        except Exception as e:
            logger.error("SharePoint fetch failed", error=str(e))
            return []

    async def fetch_from_excel(self, file_path):
        # Existing code remains
        import pandas as pd
        try:
            df = pd.read_excel(file_path)
            return df.to_dict('records')
        except Exception as e:
            logger.error("Excel fetch failed", error=str(e))
            return []

    async def load_custom_documents(self):
        # New: Load and return text from .pdf/.txt/.docx files
        documents = load_documents_from_directory(self.documents_dir)
        logger.info("Loaded documents", count=len(documents))
        return documents
