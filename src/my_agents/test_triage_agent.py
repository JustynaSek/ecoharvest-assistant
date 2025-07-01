import asyncio
from agents import Runner, trace
from .triage_agent.triage_agent import triage_agent

async def test_triage_agent():
    # Test cases
    test_cases = [
        "What is future release of GrowPod?",  # Not a serious product query
    ]

    for query in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing query: {query}")
        print(f"{'='*50}")

        with trace("Triage Agent Test") as tracer:
            result = await Runner.run(triage_agent, query)
        
        print("\n=== Final Output ===")
        print(result.final_output)
        
        print("\n=== Raw Responses ===")
        for i, response in enumerate(result.raw_responses):
            print(f"Response {i+1}:")
            print(response)
            print("-" * 50)
        
        print("\n=== Last Agent ===")
        print(result.last_agent)

if __name__ == "__main__":
    asyncio.run(test_triage_agent()) 