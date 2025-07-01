# src/my_agents/product_info_agent/product_info_agent_tools.py
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import chromadb


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
PRODUCT_CHROMA_PATH = os.path.join("src", "chroma_dbs", "product_info_db")
PRODUCT_COLLECTION_NAME = "product_info_collection"

# Global RAG components
_product_chroma_client: Optional[chromadb.PersistentClient] = None
_product_chroma_collection: Optional[chromadb.Collection] = None

def _initialize_product_rag_components() -> None:
    """Initializes RAG components for product info. Called once globally."""
    global _product_chroma_client, _product_chroma_collection
    if _product_chroma_client is None:
        print(f"Initializing Product Info RAG components from: {PRODUCT_CHROMA_PATH}...")
        try:
            # Check if database directory exists
            if not os.path.exists(PRODUCT_CHROMA_PATH):
                print(f"ERROR: Database directory does not exist: {PRODUCT_CHROMA_PATH}")
                raise FileNotFoundError(f"Database directory not found: {PRODUCT_CHROMA_PATH}")
            
            # Check if database file exists
            db_file = os.path.join(PRODUCT_CHROMA_PATH, "chroma.sqlite3")
            if not os.path.exists(db_file):
                print(f"ERROR: Database file does not exist: {db_file}")
                raise FileNotFoundError(f"Database file not found: {db_file}")
            
            print(f"Database file exists: {os.path.exists(db_file)}")
            print(f"Database file size: {os.path.getsize(db_file)} bytes")
            
            # Initialize the ChromaDB client
            _product_chroma_client = chromadb.PersistentClient(path=PRODUCT_CHROMA_PATH)
            print("ChromaDB client initialized successfully")
            
            # Get or create the collection
            _product_chroma_collection = _product_chroma_client.get_or_create_collection(
                name=PRODUCT_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"Collection '{PRODUCT_COLLECTION_NAME}' retrieved/created successfully")
            
            # Verify collection has data
            count = _product_chroma_collection.count()
            print(f"Collection contains {count} documents")
            if count == 0:
                print("WARNING: The product info collection is empty!")
            
        except Exception as e:
            print(f"Error initializing product info RAG components: {e}")
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
    
    print(f"Tool called: query_product_knowledge_base - Query: '{query}'")
    
    try:
        # Query the collection using text search instead of embeddings
        print(f"Querying collection '{PRODUCT_COLLECTION_NAME}'...")
        results = _product_chroma_collection.query(
            query_texts=[query],
            n_results=3, # Retrieve top 3 most relevant chunks
            include=['documents', 'distances', 'metadatas']
        )
        
        print(f"Query results: {results}")
        
        relevant_docs = []
        if results and results['documents']:
            for doc_list in results['documents']:
                for doc in doc_list:
                    relevant_docs.append(doc)
            
            # Format retrieved documents as context for the LLM
            context = "\n\n".join([f"--- Context Segment ---\n{doc}" for doc in relevant_docs])
            print(f"Retrieved {len(relevant_docs)} document chunks for '{query}'.")
            return context
        else:
            print("No relevant product documents found.")
            return "No specific information found in the product knowledge base for that query. " \
                   "The agent should state this or ask for clarification."
        
    except Exception as e:
        print(f"Error querying product knowledge base: {e}")
        return f"An error occurred while trying to retrieve product information: {str(e)}. " \
               "The agent should inform the user about this issue." 