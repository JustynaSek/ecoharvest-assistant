import gradio as gr
import asyncio
from datetime import datetime
import os
import gdown
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import agents
from src.my_agents.triage_agent.triage_agent import triage_agent
from src.my_agents.product_info_agent.product_info_agent_tools import _initialize_product_rag_components
from src.my_agents.support_info_agent.support_info_agent_tools import _initialize_support_rag_components

# Import runners
from agents import Runner, trace, InputGuardrailTripwireTriggered

# Load environment variables
load_dotenv()

# Set OpenAI API key from environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in Hugging Face Spaces secrets.")

def download_database_files():
    """Download database files from Google Drive if they don't exist."""
    # Print current working directory
    print(f"\nCurrent working directory: {os.getcwd()}")
    
    # Create directories if they don't exist
    product_db_dir = "src/chroma_dbs/product_info_db"
    support_db_dir = "src/chroma_dbs/support_info_db"
    
    print(f"\nCreating directories:")
    print(f"Product DB directory: {os.path.abspath(product_db_dir)}")
    print(f"Support DB directory: {os.path.abspath(support_db_dir)}")
    
    os.makedirs(product_db_dir, exist_ok=True)
    os.makedirs(support_db_dir, exist_ok=True)

    # Product Info DB file
    product_db_file = {
        "chroma.sqlite3": "1kNEJQswOZuLnZGGIHTSfKBrQHB-vB7S_"
    }

    # Support Info DB file
    support_db_file = {
        "chroma.sqlite3": "17ZfKQxuQyN1s3zJ_Fn3RTVQv32A7e1v3"
    }

    # Download Product Info DB file
    for filename, file_id in product_db_file.items():
        dest_path = os.path.join(product_db_dir, filename)
        print(f"\nChecking Product DB file:")
        print(f"Destination path: {os.path.abspath(dest_path)}")
        print(f"File exists: {os.path.exists(dest_path)}")
        
        if not os.path.exists(dest_path):
            print(f"\nDownloading product info DB file:")
            print(f"File: {filename}")
            print(f"From: https://drive.google.com/uc?id={file_id}")
            print(f"To: {os.path.abspath(dest_path)}")
            
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, dest_path, quiet=False)
            
            print(f"\nDownload complete:")
            print(f"File exists: {os.path.exists(dest_path)}")
            print(f"File size: {os.path.getsize(dest_path) if os.path.exists(dest_path) else 'N/A'} bytes")

    # Download Support Info DB file
    for filename, file_id in support_db_file.items():
        dest_path = os.path.join(support_db_dir, filename)
        print(f"\nChecking Support DB file:")
        print(f"Destination path: {os.path.abspath(dest_path)}")
        print(f"File exists: {os.path.exists(dest_path)}")
        
        if not os.path.exists(dest_path):
            print(f"\nDownloading support info DB file:")
            print(f"File: {filename}")
            print(f"From: https://drive.google.com/uc?id={file_id}")
            print(f"To: {os.path.abspath(dest_path)}")
            
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, dest_path, quiet=False)
            
            print(f"\nDownload complete:")
            print(f"File exists: {os.path.exists(dest_path)}")
            print(f"File size: {os.path.getsize(dest_path) if os.path.exists(dest_path) else 'N/A'} bytes")

# Download database files before initializing the agent
print("\n=== Starting Database Download Process ===")
download_database_files()
print("=== Database Download Process Complete ===\n")

# Initialize the databases
try:
    print("\n=== Starting Database Initialization ===")
    _initialize_product_rag_components()
    _initialize_support_rag_components()
    print("=== Database Initialization Complete ===\n")
except Exception as e:
    print(f"\nERROR: Failed to initialize database: {e}")
    raise

async def process_query(message: str, history: list) -> tuple:
    """
    Process user query through the triage agent system.
    
    Args:
        message: The user's message
        history: The chat history
    
    Returns:
        tuple: (empty string, updated history)
    """
    try:
        # Run through triage agent which will handle routing to appropriate agent
        with trace("Triage Agent Test") as tracer:
            result = await Runner.run(triage_agent, message)
        
        # Get the response
        response = result.final_output
        
        # Add metadata to history
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "agent_used": result.last_agent.name,
            "raw_response": result.raw_responses,
            "trace": result.trace if hasattr(result, 'trace') else []
        }
        
        # Update history with the new exchange
        history.append((message, response))
        return "", history
    except InputGuardrailTripwireTriggered as e:
        logger.warning(f"Input guardrail triggered: {e}")
        history.append((message, "I apologize, but I cannot process that request."))
        return "", history
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        error_message = f"An error occurred: {str(e)}"
        history.append((message, error_message))
        return "", history

def create_interface():
    """
    Create and configure the Gradio interface.
    """
    with gr.Blocks(
        title="EcoHarvest AI Assistant", 
        theme=gr.themes.Default(
            primary_hue="green", 
            secondary_hue="blue"
        ),
        css=".gradio-container {background-color: #f5f5f5;}"
    ) as demo:
        gr.Markdown("""
        # 🌱 EcoHarvest AI Assistant
        
        Welcome to the EcoHarvest AI Assistant! I can help you with:
        - Product information and features
        - Technical support and troubleshooting
        - Account notifications and alerts
        
        How can I assist you today?
        """)
        
        with gr.Row():
            with gr.Column(scale=4):
                chatbot = gr.Chatbot(
                    height=600,
                    show_copy_button=True,
                    show_share_button=True,
                    bubble_full_width=False,
                    elem_id="chatbot"
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        show_label=False,
                        container=False,
                        scale=8,
                        elem_id="chat-input" 
                    )
                    submit = gr.Button("Send", variant="primary", scale=1)
                
                with gr.Row():
                    clear = gr.Button("Clear Chat")
            
            with gr.Column(scale=1):
                gr.Markdown("""
                ### Quick Links
                - [Product Documentation](https://ecoharvest.com/docs)
                - [Support Portal](https://ecoharvest.com/support)
                - [Account Settings](https://ecoharvest.com/account)
                """)
        
        # Event handlers
        submit.click(
            process_query,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot],
            api_name="chat"
        )
        
        msg.submit(
            process_query,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot],
            api_name="chat"
        )
        
        clear.click(lambda: None, None, chatbot, queue=False)
    
    # Add custom CSS to style the chat input
    demo.css = """
    #chat-input textarea { 
        background-color: #f0f0f0 !important; 
        border: 1px solid #ccc !important;
    }
    """
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True
    ) 