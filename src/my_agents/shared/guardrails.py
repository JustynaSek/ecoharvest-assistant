from pydantic import BaseModel
from agents import Agent, input_guardrail, GuardrailFunctionOutput, RunContextWrapper, Runner, InputGuardrailTripwireTriggered

class GuardrailOutput(BaseModel):
    is_question_unsafe: bool
    reasoning: str

guardrail_instructions = '''Analyze the following user message. Your response must be a JSON object with two fields:
'is_question_unsafe': a boolean, true if the message is unsafe; false otherwise.
'reasoning': a brief string explanation of your decision.

A message is considered unsafe if it:
1. Asks to write, generate, or produce any kind of code (e.g., Python, SQL, HTML).
2. Requests information about unannounced products, features, or confidential business strategy.
3. Asks for confidential support procedures, internal troubleshooting steps, or sensitive customer data.
4. Contains harmful, unethical, or inappropriate content.

Example for unsafe input: {"is_question_unsafe": true, "reasoning": "The user is asking to write a Python script."}
Example for safe input: {"is_question_unsafe": false, "reasoning": "The question is a safe product-related query."}

Always ensure your response is a valid JSON object matching this schema.'''

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions=guardrail_instructions,
    output_type=GuardrailOutput,
    model="gpt-4o-mini",
    tools=[]
)

@input_guardrail
async def universal_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str
) -> GuardrailFunctionOutput:
    
    print(f"\n[DEBUG] universal_guardrail entered with input: '{input}'") 
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    guardrail_output: GuardrailOutput = result.final_output
    print(f"[DEBUG] Guardrail agent response: is_question_unsafe={guardrail_output.is_question_unsafe}, reasoning='{guardrail_output.reasoning}'")
    
    if guardrail_output.is_question_unsafe:
        print("[DEBUG] Guardrail tripwire TRIGGERED by unsafe content.")
        raise InputGuardrailTripwireTriggered(
            f"I'm sorry, I cannot process this request. Reason: {guardrail_output.reasoning}"
        )

    print("[DEBUG] universal_guardrail finished without triggering tripwire.")
    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=guardrail_output.is_question_unsafe,
    ) 