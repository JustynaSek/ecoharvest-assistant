import asyncio
from agents import Runner, Agent, InputGuardrailTripwireTriggered, trace
from my_agents.product_info_agent.product_info_agent import productInfoAgent
from src.my_agents.triage_agent import triage_agent_instruction

print("Testing product agent import and tool creation...")
product_agent_tool = productInfoAgent.as_tool(
            tool_name="product_agent", 
            tool_description='Handles all inquiries related to EcoHarvest product features, specifications, pricing, warranty, returns, and general sales.'
)
print("✓ Product agent tool created successfully")


async def test_direct_tool_invocation():
    print("=== Testing Direct Tool Invocation ===")
    
    try:
        # The tool expects a structured input, not just a string
        # Let's check what the tool expects
        print(f"Tool schema: {product_agent_tool.params_json_schema}")
        
        # Try invoking with proper structure
        tool_input = {"input": "What is the warranty period for the EcoHarvest GrowPod Standard?"}
        tool_result = await product_agent_tool.on_invoke_tool(tool_input)
        print(f"✓ Direct tool invocation successful: {tool_result}")
        return True
    except Exception as e:
        print(f"✗ Direct tool invocation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# Also add this function to test the tool invocation mechanism
async def test_tool_invocation_methods():
    print("=== Testing Different Tool Invocation Methods ===")
    
    # Method 1: Try with structured input
    try:
        print("Method 1: Structured input")
        tool_input = {"input": "What is the warranty period for the EcoHarvest GrowPod Standard?"}
        result1 = await product_agent_tool.on_invoke_tool(tool_input)
        print(f"✓ Method 1 successful: {result1}")
    except Exception as e:
        print(f"✗ Method 1 failed: {e}")
    
    # Method 2: Try calling the underlying function directly
    try:
        print("\nMethod 2: Direct function call")
        # This should work since your product agent works standalone
        result2 = await Runner.run(productInfoAgent, "What is the warranty period for the EcoHarvest GrowPod Standard?")
        print(f"✓ Method 2 successful: {result2.final_output}")
    except Exception as e:
        print(f"✗ Method 2 failed: {e}")
    
    # Method 3: Check if the tool wrapper is working
    try:
        print("\nMethod 3: Tool wrapper test")
        # Let's see what happens when we create a simple agent that uses tools
        simple_tool_agent = Agent(
            name="Simple Tool Agent",
            instructions="Use the product_agent tool to answer questions.",
            tools=[product_agent_tool],  # Use as regular tool, not handoff
            model="gpt-4o-mini"
        )
        result3 = await Runner.run(simple_tool_agent, "What is the warranty period?")
        print(f"✓ Method 3 successful: {result3.final_output}")
        print(f"Last agent: {result3.last_agent.name}")
    except Exception as e:
        print(f"✗ Method 3 failed: {e}")
        import traceback
        traceback.print_exc()

async def use_triage_agent():
    print("=== Starting Triage Agent Test ===")
    
    # First verify the product agent can be imported and used as a tool
    
    # Create triage agent
    triage_agent = Agent(
        name="Triage Agent",
        instructions=triage_agent_instruction,
        handoffs=[product_agent_tool],
        model="gpt-4o-mini"
    )
    print("✓ Triage agent created successfully")
    
    message = "What is the warranty period for the EcoHarvest GrowPod Standard?"
    print(f"✓ Processing message: {message}")
    
    try:
        with trace("Automated SDR"):
            result = await Runner.run(triage_agent, message)
        
        print("\n=== RESULTS ===")
        print(f"Final Output: {result.final_output}")
        print(f"Last Agent: {result.last_agent.name}")
        
        # Check if handoff occurred by looking at raw responses
        print(f"\n=== RAW RESPONSES ({len(result.raw_responses)} total) ===")
        for i, response in enumerate(result.raw_responses):
            print(f"\nResponse {i+1}:")
            if hasattr(response, 'output') and response.output:
                for j, output_msg in enumerate(response.output):
                    print(f"  Message {j+1}: {getattr(output_msg, 'content', 'No content')}")
                    # Check for tool calls
                    if hasattr(output_msg, 'tool_calls') and output_msg.tool_calls:
                        print(f"    Tool calls: {output_msg.tool_calls}")
            else:
                print(f"  Raw content: {response}")
        
        # Additional debugging info
        print(f"\n=== ADDITIONAL DEBUG INFO ===")
        print(f"Input: {result.input}")
        if hasattr(result, 'new_items'):
            print(f"New items: {result.new_items}")
        
        return result
        
    except Exception as e:
        print(f"✗ Error during triage execution: {e}")
        import traceback
        traceback.print_exc()
        return None

# Also add this function to test the handoff mechanism more directly
async def test_handoff_mechanism():
    print("=== Testing Handoff Mechanism Directly ===")
    
    # Create a simple test to see if handoffs work at all
    simple_agent = Agent(
        name="Simple Test Agent",
        instructions="You are a test agent. When you receive any message, use the product_agent tool to handle it.",
        handoffs=[product_agent_tool],
        model="gpt-4o-mini"
    )
    
    try:
        result = await Runner.run(simple_agent, "Test message")
        print(f"Simple handoff test result: {result.final_output}")
        print(f"Last agent: {result.last_agent.name}")
        return result.last_agent.name != "Simple Test Agent"  # True if handoff worked
    except Exception as e:
        print(f"Handoff mechanism test failed: {e}")
        return False

async def test_direct_tool_invocation():
    print("=== Testing Direct Tool Invocation ===")
    
    try:
        # Try to invoke the tool directly
        tool_result = product_agent_tool.on_invoke_tool("What is the warranty period for the EcoHarvest GrowPod Standard?")
        print(f"✓ Direct tool invocation successful: {tool_result}")
        return True
    except Exception as e:
        print(f"✗ Direct tool invocation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
async def test_direct_tool_invocation():
    print("=== Testing Direct Tool Invocation ===")
    
    try:
        # Try to invoke the tool directly
        tool_result = product_agent_tool.on_invoke_tool("What is the warranty period for the EcoHarvest GrowPod Standard?")
        print(f"✓ Direct tool invocation successful: {tool_result}")
        return True
    except Exception as e:
        print(f"✗ Direct tool invocation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
# Modified main function
if __name__ == "__main__":
    print("Testing direct tool invocation...")
    tool_works = asyncio.run(test_direct_tool_invocation())
    
    print("\nTesting different invocation methods...")
    asyncio.run(test_tool_invocation_methods())
    
    if not tool_works:
        print("\n" + "="*50)
        print("DIAGNOSIS: The tool invocation mechanism has issues.")
        print("Let's try using the product agent as a regular tool instead of handoff...")
        
