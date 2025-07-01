# src/agents/support_info_agent.py
from pydantic import BaseModel
from agents import Agent, function_tool, input_guardrail, GuardrailFunctionOutput, RunContextWrapper, Runner, InputGuardrailTripwireTriggered

# Import the specific tools for this agent
from .support_info_agent_tools import query_support_knowledge_base_tool, SupportKnowledgeQueryInput
from ..shared.guardrails import universal_guardrail

@function_tool
def _query_support_knowledge_base(query: str) -> str:
    """
    Queries the EcoHarvest support knowledge base to find answers about troubleshooting,
    technical support, maintenance, and general assistance. Use this tool for any factual
    question about EcoHarvest support and technical assistance.
    """
    return query_support_knowledge_base_tool(query)

instructions = """You are the EcoHarvest Support Information Agent. Your primary role is to provide detailed and accurate information about EcoHarvest support services, troubleshooting steps, maintenance procedures, and technical assistance.

**Always use the `_query_support_knowledge_base` tool for any factual question about our support services or technical assistance.** Never invent information.
If the tool returns no relevant information, state that you cannot find the answer and suggest the user rephrase their question.
Be helpful and engaging, aiming to fully answer support-related queries.
Do NOT attempt to provide product information or handle sales inquiries. If a user asks about these, politely redirect them by suggesting they speak to the "Product Information Agent" (without performing a handoff yourself).
"""

supportInfoAgent = Agent(
    name="Support Information Agent",
    instructions=instructions,
    tools=[_query_support_knowledge_base],
    model="gpt-4o-mini",
    input_guardrails=[universal_guardrail]
) 