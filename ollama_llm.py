import asyncio
import aiohttp
from utils import logger
from sentence_transformers import SentenceTransformer  # Lightweight embedder
from sklearn.metrics.pairwise import cosine_similarity  # Needed for find_similar_context

class OllamaLLM:
    def __init__(self, base_url, model):
        self.base_url = base_url
        self.model = model
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight embedder

    async def query_llm(self, prompt, context=None):
        """
        Query the Ollama model.
        `context` can be a list of documents or a string.
        """

        # Convert context into a single string
        if isinstance(context, list):
            context_text = "\n".join([doc['text'] for doc in context])
        else:
            context_text = context or ""

        # Combine context and user prompt
        full_prompt = f"{context_text}\nUser: {prompt}" if context_text else prompt

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "temperature": 0.7,
            "max_tokens": 200,
            "stream": False
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/generate", json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "No response generated.")
                    else:
                        logger.error("LLM query failed", status=response.status)
                        return None
        except Exception as e:
            logger.error("Error querying LLM", error=str(e))
            return None

    # Optional wrapper for compatibility with existing TeamsBot code
    async def query(self, prompt, context=None):
        return await self.query_llm(prompt, context)

    async def embed_documents(self, documents):
        """
        Generate embeddings for document texts.
        Returns a dict: {index: {"text": ..., "embedding": ...}}
        """
        texts = [doc['text'] for doc in documents]
        try:
            embeddings = self.embedder.encode(texts)
            embedded_docs = {i: {"text": texts[i], "embedding": embeddings[i]} for i in range(len(texts))}
            logger.info("Documents embedded", count=len(embedded_docs))
            return embedded_docs
        except Exception as e:
            logger.error("Embedding failed", error=str(e))
            return {}

    async def find_similar_context(self, query, embedded_docs, top_k=3):
        """
        Retrieve most relevant document chunks based on cosine similarity.
        """
        query_embedding = self.embedder.encode([query])[0]
        similarities = []
        for idx, doc in embedded_docs.items():
            sim = cosine_similarity([query_embedding], [doc['embedding']])[0][0]
            similarities.append((idx, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)
        context_text = "\n".join([embedded_docs[idx]['text'] for idx, _ in similarities[:top_k]])
        return context_text
