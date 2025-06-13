import gradio as gr
import asyncio
from datetime import datetime

# Import agents
from my_agents.triage_agent.triage_agent import triage_agent

# Import runners
from agents import Runner, trace, InputGuardrailTripwireTriggered

async def process_query(message: str) -> str:
    return "bla bla"
    # """
    # Process user query through the triage agent system.
    # """
    # try:
    #     # Run through triage agent which will handle routing to appropriate agent
    #     with trace("Triage Agent Test") as tracer:
    #         result = await Runner.run(triage_agent, message)
        
    #     # Get the response
    #     response = result.final_output
        
    #     # Add metadata to history
    #     metadata = {
    #         "timestamp": datetime.now().isoformat(),
    #         "agent_used": result.last_agent.name,
    #         "raw_response": result.raw_responses,
    #         "trace": result.trace if hasattr(result, 'trace') else []
    #     }
        
    #     # Update history with the new exchange
    #     #history.append((message, response))
        
    #     return response#, history
    # except InputGuardrailTripwireTriggered as e:
    #     print(f"[RESULT 2] SUCCESS: Input Guardrail (from ProductInfoAgent) triggered as expected for unsafe query: {e}")   
    # except Exception as e:
    #     error_message = f"An error occurred: {str(e)}"
    #     #history.append((message, error_message))
    #     return error_message#, history

def create_interface():
    """
    Create and configure the Gradio interface.
    """
    with gr.Blocks(title="EcoHarvest AI Assistant", theme=gr.themes.Soft()) as demo:
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
                    avatar_images=("👤", "🤖")
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        show_label=False,
                        container=False,
                        scale=8
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
        ).then(
            lambda: "",
            None,
            msg,
            queue=False
        )
        
        msg.submit(
            process_query,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot],
            api_name="chat"
        ).then(
            lambda: "",
            None,
            msg,
            queue=False
        )
        
        clear.click(lambda: None, None, chatbot, queue=False)
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True
    ) 