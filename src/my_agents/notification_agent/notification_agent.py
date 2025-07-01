from agents import Agent
from .notification_tool import notification_tool
from .notification_guardrail import name_guardrail
from ..shared.guardrails import universal_guardrail

instructions = """You are a push message formatter and sender. You receive the name of the person that wants to receive a message. 
You create a welcome message for the given person. Finally, you use the send_notification tool to send the welcome notification to the given person.

IMPORTANT RULES:
1. Only accept valid names (at least 2 characters)
2. Do not process inappropriate content
3. Keep the input focused on just the name
4. Always use the send_notification tool to send the message
"""

notification_agent = Agent(
    name="Email Manager",
    instructions=instructions,
    tools=[notification_tool],
    model="gpt-4o-mini",
    handoff_description="Create welcome message and send it",
    input_guardrails=[name_guardrail, universal_guardrail]) 