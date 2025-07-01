from agents import Runner
from my_agents.context import UserContext
from my_agents.notification_agent.notification_agent import notification_agent

async def process_user_message(name: str, message: str):
    """
    Process a user message by creating appropriate context and running the notification agent.
    
    Args:
        name (str): The name of the user
        message (str): The message from the user
    """
    # Create context based on the user's name
    user_context = UserContext.create_from_name(name)
    
    # Run the notification agent with the context
    result = await Runner.run(
        notification_agent,
        name,  # Pass the name as the input message
        context=user_context
    )
    
    return result.final_output

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Example with a known user
        result = await process_user_message("John Smith", "John Smith")
        print(f"Known user result: {result}")
        
        # Example with an unknown user
        result = await process_user_message("New User", "New User")
        print(f"Unknown user result: {result}")
    
    asyncio.run(main()) 