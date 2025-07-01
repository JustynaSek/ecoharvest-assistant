from pydantic import BaseModel, Field
from agents import Agent
from ..product_info_agent.product_info_agent import productInfoAgent 
from ..support_info_agent.support_info_agent import supportInfoAgent
from ..notification_agent import notification_agent

class TriageOutput(BaseModel):
    agent_name: str = Field(
        description="The name of the specialized agent selected to handle the request. "
                    "Must be one of the names defined in the 'handoffs' list (e.g., 'Email Manager') or use the product_agent tool for product queries."
    )
    reasoning: str = Field(
        description="A concise explanation for why this particular specialized agent was selected."
    )
    original_query: str = Field(
        description="The user's original query, which should be passed along to the selected agent for processing."
    )

product_agent_tool = productInfoAgent.as_tool(tool_name="product_agent", tool_description='''
                            Handles all inquiries related to EcoHarvest product features, specifications, pricing, warranty, returns, and general sales.''')

support_agent_tool = supportInfoAgent.as_tool(tool_name="support_agent", tool_description='''
                            Handles all inquiries related to EcoHarvest support services, troubleshooting, maintenance, and technical assistance.''')

triage_agent_instruction = """You are the central Triage Agent for EcoHarvest customer inquiries. Your job is to analyze requests and delegate them to the appropriate specialized agent. If a user's query is not related to EcoHarvest products, support, or notifications, you must state that you can only answer questions about EcoHarvest.

Here are the specialized agents you can delegate to:
- **Product Information Agent**: Use the 'product_agent' tool for any questions strictly related to EcoHarvest products. This includes GrowPod models, app features, seed pod varieties, pricing, compatibility, warranty, returns, and general sales inquiries.
- **Support Information Agent**: Use the 'support_agent' tool for any questions about troubleshooting, technical support, maintenance procedures, and general assistance.
- **Email Manager**: Use this handoff when you need to send welcome messages to new users. This agent will create and send personalized welcome messages.

IMPORTANT: You MUST use the appropriate method to handle each request:
- For product-related questions, use the 'product_agent' tool
- For support-related questions, use the 'support_agent' tool
- For welcome messages, use the 'Email Manager' handoff

If the query is not related to any of the above, respond with: "I can only answer questions about EcoHarvest products, support, and services."
Do not just explain what you would do - actually use the appropriate tool or handoff to handle the user's request.
"""                       

triage_agent = Agent(
        name="Triage Agent",
        instructions=triage_agent_instruction,
        tools=[product_agent_tool, support_agent_tool],
        model="gpt-4o-mini",
        handoffs=[notification_agent]) 