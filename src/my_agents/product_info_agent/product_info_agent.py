# src/agents/product_info_agent.py
from pydantic import BaseModel
from agents import Agent, function_tool, input_guardrail, GuardrailFunctionOutput, RunContextWrapper, Runner, InputGuardrailTripwireTriggered

# Import the specific tools for this agent
from .product_info_agent_tools import query_product_knowledge_base_tool, ProductKnowledgeQueryInput
from ..shared.guardrails import universal_guardrail

@function_tool
def _query_product_knowledge_base(query: str) -> str:
    """
    Queries the EcoHarvest product knowledge base to find answers about GrowPod features,
    app capabilities, seed pod varieties, pricing plans, compatibility, warranty, returns,
    and general sales inquiries. Use this tool for any factual question about EcoHarvest products.
    """
    return query_product_knowledge_base_tool(query)

# Fix: Properly define the instructions variable
instructions = """You are the EcoHarvest Product Information Agent. Your primary role is to provide detailed and accurate information about all EcoHarvest products, including the GrowPod models, app features, seed pod varieties, pricing, and general policies (warranty, returns, compatibility).

**Always use the `_query_product_knowledge_base` tool for any factual question about our products or policies.** Never invent information.
If the tool returns no relevant information, state that you cannot find the answer and suggest the user rephrase their question.
Be helpful and engaging, aiming to fully answer product-related queries.
Do NOT attempt to provide technical troubleshooting steps or assist with billing/subscription issues. If a user asks about these, politely redirect them by suggesting they speak to the "Customer Support Agent" (without performing a handoff yourself).
"""

# Fix: Remove the extra comma and use proper variable
productInfoAgent = Agent(
    name="Product Information Agent",
    instructions=instructions,
    tools=[_query_product_knowledge_base],
    model="gpt-4o-mini",
    input_guardrails=[universal_guardrail]
)