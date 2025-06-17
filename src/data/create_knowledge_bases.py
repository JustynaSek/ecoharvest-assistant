import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

DATA_DIR = "data"

PRODUCT_INFO_FILE = os.path.join(DATA_DIR, "product_info.txt")
SUPPORT_INFO_FILE = os.path.join(DATA_DIR, "support_info.txt")

CHROMA_DB_BASE_PATH = "chroma_dbs"
PRODUCT_CHROMA_PATH = os.path.join(CHROMA_DB_BASE_PATH, "product_info_db")
SUPPORT_CHROMA_PATH = os.path.join(CHROMA_DB_BASE_PATH, "support_info_db")

PRODUCT_COLLECTION_NAME = "product_info_collection"
SUPPORT_COLLECTION_NAME = "support_info_collection"

# Embedding model to use. 'all-MiniLM-L6-v2' is a good balance of size/performance.
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

SECTION_DELIMITER = "### SECTION:"
PARAGRAPH_DELIMITER = "\n\n" # Primary split within sections

def load_and_chunk_data(file_path: str) -> List[Dict[str, str]]:
    """
    Loads text from a file, splits it into sections, and then into chunks,
    returning a list of dictionaries with 'content' and 'source' metadata.
    """
    print(f"Loading and chunking data from: {file_path}")
    chunks_with_metadata = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            full_text = f.read()

        sections = full_text.split(SECTION_DELIMITER)
        
        # Process each section
        for section_id, section_content in enumerate(sections):
            if not section_content.strip():
                continue

            # Extract section title (e.g., " PRODUCT OVERVIEW ###")
            first_line_break = section_content.find('\n')
            if first_line_break != -1:
                title = section_content[:first_line_break].strip().replace("###", "").strip()
                content_after_title = section_content[first_line_break:].strip()
            else: # If no newline, assume the whole section_content is the title
                title = section_content.strip().replace("###", "").strip()
                content_after_title = ""

            # Split the section content into paragraphs or smaller chunks
            paragraphs = [p.strip() for p in content_after_title.split(PARAGRAPH_DELIMITER) if p.strip()]
            
            if not paragraphs and title: # If a section only had a title but no content, add the title itself as a chunk
                 chunks_with_metadata.append({
                    "content": title,
                    "metadata": {"source_file": os.path.basename(file_path), "section_title": title, "chunk_type": "title"}
                })
                 continue

            for i, paragraph in enumerate(paragraphs):
                chunks_with_metadata.append({
                    "content": paragraph,
                    "metadata": {
                        "source_file": os.path.basename(file_path),
                        "section_title": title,
                        "chunk_id_in_section": i
                    }
                })
        print(f"Finished chunking {len(chunks_with_metadata)} chunks from {file_path}.")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred while loading/chunking {file_path}: {e}")
    
    return chunks_with_metadata

def create_chroma_db(chunks: List[Dict[str, str]], db_path: str, collection_name: str, model: SentenceTransformer):
    """
    Creates or updates a ChromaDB collection with the given chunks.
    """
    print(f"Creating/updating Chroma DB at '{db_path}' for collection '{collection_name}'...")
    os.makedirs(db_path, exist_ok=True)
    
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name=collection_name)
    
    documents = [c['content'] for c in chunks]
    metadatas = [c['metadata'] for c in chunks]
    ids = [f"{collection_name}_{i}" for i in range(len(chunks))]

    print(f"Generating embeddings for {len(documents)} documents...")
    embeddings = model.encode(documents).tolist() # Convert numpy array to list for Chroma
    print("Embeddings generated.")

    print(f"Adding documents to collection '{collection_name}'...")
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Successfully added {len(documents)} documents to '{collection_name}'.")

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    
    print("Loading embedding model...")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print("Embedding model loaded.")

    product_chunks = load_and_chunk_data(PRODUCT_INFO_FILE)
    if product_chunks:
        create_chroma_db(product_chunks, PRODUCT_CHROMA_PATH, PRODUCT_COLLECTION_NAME, embedding_model)
    else:
        print(f"No chunks found for {PRODUCT_INFO_FILE}. Skipping DB creation for product info.")

    print("-" * 50)

    support_chunks = load_and_chunk_data(SUPPORT_INFO_FILE)
    if support_chunks:
        create_chroma_db(support_chunks, SUPPORT_CHROMA_PATH, SUPPORT_COLLECTION_NAME, embedding_model)
    else:
        print(f"No chunks found for {SUPPORT_INFO_FILE}. Skipping DB creation for support info.")

    print("\nKnowledge base creation process complete.")