# src/my_agents/product_info_agent/product_info_agent_tools.py
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
import logging
import chromadb
import numpy as np

# Set up logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(override=True)

import requests

# --- General Utility Tool (Pushover) ---
def push(text: str) -> None:
    """Sends a notification to Pushover."""
    # Ensure PUSHOVER_TOKEN and PUSHOVER_USER are set in your .env
    token = os.getenv("PUSHOVER_TOKEN")
    user = os.getenv("PUSHOVER_USER")
    if not token or not user:
        logger.warning("Pushover API keys not set in .env. Skipping notification.")
        return
    
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": token,
                "user": user,
                "message": text,
            },
            timeout=10  # Add timeout for reliability
        )
        response.raise_for_status()
        logger.info("Pushover notification sent successfully")
    except requests.RequestException as e:
        logger.error(f"Failed to send Pushover notification: {e}")

# --- Configuration for Product Info RAG ---
PRODUCT_CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "chroma_dbs", "product_info_db")
PRODUCT_COLLECTION_NAME = "product_info_collection"

# Global RAG components
_product_chroma_client: Optional[chromadb.PersistentClient] = None
_product_chroma_collection: Optional[chromadb.Collection] = None

def _initialize_product_rag_components() -> None:
    """Initializes RAG components for product info. Called once globally."""
    global _product_chroma_client, _product_chroma_collection
    if _product_chroma_client is None:
        logger.info(f"Initializing Product Info RAG components from: {PRODUCT_CHROMA_PATH}...")
        try:
            _product_chroma_client = chromadb.PersistentClient(path=PRODUCT_CHROMA_PATH)
            _product_chroma_collection = _product_chroma_client.get_or_create_collection(name=PRODUCT_COLLECTION_NAME)
            logger.info("Product Info RAG components initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize RAG components: {e}")
            raise

# --- Tool for ProductInfoAgent: RAG Query ---
class ProductKnowledgeQueryInput(BaseModel):
    """Input schema for querying the product knowledge base."""
    query: str = Field(description="The user's specific question about EcoHarvest products, features, pricing, or policies.")

def query_product_knowledge_base_tool(query: str) -> str:
    """
    Queries the EcoHarvest product knowledge base to find answers about GrowPod features,
    app capabilities, seed pod varieties, pricing plans, compatibility, warranty, returns,
    and sales inquiries. Returns relevant factual context.
    """
    _initialize_product_rag_components() # Ensure RAG components are ready before querying
    
    logger.info(f"Tool called: query_product_knowledge_base - Query: '{query}'")

    try:
        # Query the collection using text search instead of embeddings
        results = _product_chroma_collection.query(
            query_texts=[query],
            n_results=3, # Retrieve top 3 most relevant chunks
            include=['documents', 'distances', 'metadatas']
        )
        
        relevant_docs = []
        if results and results['documents']:
            for doc_list in results['documents']:
                for doc in doc_list:
                    relevant_docs.append(doc)
            
            # Format retrieved documents as context for the LLM
            context = "\n\n".join([f"--- Context Segment ---\n{doc}" for doc in relevant_docs])
            logger.info(f"Retrieved {len(relevant_docs)} document chunks for '{query}'.")
            return context
        else:
            logger.warning("No relevant product documents found.")
            return "No specific information found in the product knowledge base for that query. " \
                   "The agent should state this or ask for clarification."
                   
    except Exception as e:
        logger.error(f"Error querying product knowledge base: {e}")
        return f"An error occurred while trying to retrieve product information: {str(e)}. " \
               "The agent should inform the user about this issue." 