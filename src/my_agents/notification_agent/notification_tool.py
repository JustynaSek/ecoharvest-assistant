from typing import Dict, Any
from agents import function_tool

@function_tool
def create_and_send_welcome_message(name: str) -> Dict[str, Any]:
    """
    Creates a welcome message for a person and mocks sending it.
    
    Args:
        name (str): The name of the person to send the welcome message to
        
    Returns:
        Dict[str, Any]: A dictionary containing the message details and status
    """
    welcome_message = f"Welcome {name}! We're excited to have you join our community. We hope you'll find everything you need here."
    
    # Mock sending the message
    print(f"[MOCK] Sending welcome message to {name}")
    print(f"[MOCK] Message content: {welcome_message}")
    
    return {
        "status": "success",
        "recipient": name,
        "message": welcome_message,
        "sent_at": "2024-03-19T12:00:00Z"  # Mock timestamp
    }

# Export the decorated function
notification_tool = create_and_send_welcome_message 