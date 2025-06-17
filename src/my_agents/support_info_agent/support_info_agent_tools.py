import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import chromadb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(override=True)

SUPPORT_CHROMA_PATH = os.path.join("src", "chroma_dbs", "support_info_db")
SUPPORT_COLLECTION_NAME = "support_info_collection"

_support_chroma_client: Optional[chromadb.PersistentClient] = None
_support_chroma_collection: Optional[chromadb.Collection] = None

def _initialize_support_rag_components() -> None:
    """Initializes RAG components for support info. Called once globally."""
    global _support_chroma_client, _support_chroma_collection
    if _support_chroma_client is None:
        print(f"Initializing Support Info RAG components from: {SUPPORT_CHROMA_PATH}...")
        try:
              if not os.path.exists(SUPPORT_CHROMA_PATH):
                print(f"ERROR: Database directory does not exist: {SUPPORT_CHROMA_PATH}")
                raise FileNotFoundError(f"Database directory not found: {SUPPORT_CHROMA_PATH}")
            
                 db_file = os.path.join(SUPPORT_CHROMA_PATH, "chroma.sqlite3")
            if not os.path.exists(db_file):
                print(f"ERROR: Database file does not exist: {db_file}")
                raise FileNotFoundError(f"Database file not found: {db_file}")
            
            print(f"Database file exists: {os.path.exists(db_file)}")
            print(f"Database file size: {os.path.getsize(db_file)} bytes")
            
            _support_chroma_client = chromadb.PersistentClient(path=SUPPORT_CHROMA_PATH)
            print("ChromaDB client initialized successfully")
            
            _support_chroma_collection = _support_chroma_client.get_or_create_collection(
                name=SUPPORT_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"Collection '{SUPPORT_COLLECTION_NAME}' retrieved/created successfully")
            
            count = _support_chroma_collection.count()
            print(f"Collection contains {count} documents")
            if count == 0:
                print("WARNING: The support info collection is empty!")
            
        except Exception as e:
            print(f"Error initializing support info RAG components: {e}")
            raise

# --- Tool for SupportInfoAgent: RAG Query ---
class SupportKnowledgeQueryInput(BaseModel):
    """Input schema for querying the support knowledge base."""
    query: str = Field(description="The user's specific question about EcoHarvest support, troubleshooting, or technical assistance.")

def query_support_knowledge_base_tool(query: str) -> str:
    """
    Queries the EcoHarvest support knowledge base to find answers about troubleshooting,
    technical support, maintenance, and general assistance. Returns relevant factual context.
    """
    _initialize_support_rag_components()
    
    print(f"Tool called: query_support_knowledge_base - Query: '{query}'")
    
    try:
        print(f"Querying collection '{SUPPORT_COLLECTION_NAME}'...")
        results = _support_chroma_collection.query(
            query_texts=[query],
            n_results=3,
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
            print("No relevant support documents found.")
            return "No specific information found in the support knowledge base for that query. " \
                   "The agent should state this or ask for clarification."
        
    except Exception as e:
        print(f"Error querying support knowledge base: {e}")
        return f"An error occurred while trying to retrieve support information: {str(e)}. " \
               "The agent should inform the user about this issue." 