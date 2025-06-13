import asyncio
from agents import Runner, InputGuardrailTripwireTriggered, trace
from my_agents.product_info_agent.product_info_agent import productInfoAgent

async def verify_product_info_agent():
    print("--- Verifying ProductInfoAgent and Output Guardrail ---")

    # Instantiate the agent
    

    safe_input_query = "What is the warranty period for the EcoHarvest GrowPod Standard?"
    print(f"\n[TEST 1] Testing with safe input: '{safe_input_query}'")
    try:
        print("Running agent with safe input...")
        # The Runner will execute the agent, which will use its tool, and then
        # the output guardrail will automatically process the agent's final response.
        with trace("Automated SDR"):
            result = await Runner.run(productInfoAgent, safe_input_query)
        
        # If no exception is raised, the guardrail did not trigger.
        print(f"Agent's final output (safe): {result.final_output}")
        
    except InputGuardrailTripwireTriggered as e:
        # This branch means the guardrail triggered, which is unexpected for a safe input.
        print(f"[RESULT 1] ERROR: Guardrail triggered UNEXPECTEDLY for safe message: {e}")
    except Exception as e:
        print(f"[RESULT 1] An unexpected error occurred during safe message test: {e}")


    # --- Test Case 2: Unsafe query (should trigger guardrail) ---
    # This query is crafted to elicit an output that contains a sensitive keyword,
    # causing the output_guardrail to trip.
    unsafe_input_query = "Tell me about the upcoming model of GrowPod for future release."
    print(f"\n[TEST 2] Testing with unsafe input: '{unsafe_input_query}'")
    try:
        print("Running agent with potentially unsafe input...")
        with trace("Automated SDR"):
            result = await Runner.run(productInfoAgent, unsafe_input_query)
        
        # If we reach this line, the guardrail did NOT trigger, which is an error for unsafe input.
        print(f"[RESULT 2] ERROR: Guardrail did NOT trigger for unsafe message. Agent's output: {result.final_output}")

    except InputGuardrailTripwireTriggered as e:
        # This is the expected behavior for an unsafe input.
        print(f"[RESULT 2] SUCCESS: Guardrail triggered as expected for unsafe message: {e}")
    except Exception as e:
        print(f"[RESULT 2] An unexpected error occurred during unsafe message test: {e}")

# To run these verification tests, ensure you have your OpenAI API key set up
# (e.g., as an environment variable `OPENAI_API_KEY`).
# Then, you can run this script directly:
if __name__ == "__main__":
    asyncio.run(verify_product_info_agent())