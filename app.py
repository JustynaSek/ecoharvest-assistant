import os
import gradio as gr
from dotenv import load_dotenv
import gdown
from src.my_agents.triage_agent.triage_agent import triage_agent
from src.my_agents.context import UserContext, UserRole

# Load environment variables
load_dotenv()

def download_database_files():
    """Download database files from Google Drive if they don't exist."""
    # Create directories if they don't exist
    os.makedirs("src/chroma_dbs/product_info_db", exist_ok=True)
    os.makedirs("src/chroma_dbs/support_info_db", exist_ok=True)

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
        dest_path = f"src/chroma_dbs/product_info_db/{filename}"
        if not os.path.exists(dest_path):
            print(f"Downloading product info DB file: {filename}")
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, dest_path, quiet=False)
            print(f"Downloaded {filename}")

    # Download Support Info DB file
    for filename, file_id in support_db_file.items():
        dest_path = f"src/chroma_dbs/support_info_db/{filename}"
        if not os.path.exists(dest_path):
            print(f"Downloading support info DB file: {filename}")
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, dest_path, quiet=False)
            print(f"Downloaded {filename}")

# Download database files before initializing the agent
download_database_files()

# Initialize the agent
agent = triage_agent

def process_message(message, user_name, user_role):
    """Process user message and return response."""
    # Create user context
    context = UserContext(
        user_name=user_name,
        role=UserRole[user_role.upper()],
        is_first_interaction=True  # You might want to implement persistence for this
    )
    
    # Process the message
    response = agent.run(message, context)
    return response

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# EcoHarvest Assistant")
    
    with gr.Row():
        with gr.Column():
            message = gr.Textbox(label="Your Message", placeholder="Type your message here...")
            user_name = gr.Textbox(label="Your Name", placeholder="Enter your name...")
            user_role = gr.Dropdown(
                choices=["CHAT_USER", "ADMIN", "DEVELOPER", "SUPPORT", "SALES"],
                label="Your Role",
                value="CHAT_USER"
            )
            submit_btn = gr.Button("Send")
        
        with gr.Column():
            output = gr.Textbox(label="Response")
    
    submit_btn.click(
        fn=process_message,
        inputs=[message, user_name, user_role],
        outputs=output
    )

# Launch the app
if __name__ == "__main__":
    demo.launch() 