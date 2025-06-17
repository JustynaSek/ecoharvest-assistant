from pydantic import BaseModel
from agents import Agent, input_guardrail, GuardrailFunctionOutput, RunContextWrapper, Runner, InputGuardrailTripwireTriggered

class SupportQuestionOutput(BaseModel):
    is_question_unsafe: bool
    reasoning: str

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions='''Analyze the following user message. Your response must be a JSON object with two fields:
    'is_question_unsafe': a boolean, true if the message appears to request confidential support procedures, internal troubleshooting steps, or sensitive customer data; false otherwise.
    'reasoning': a brief string explanation of your decision.

    Example for unsafe input: {"is_question_unsafe": true, "reasoning": "The question asks for confidential support procedures."}
    Example for safe input: {"is_question_unsafe": false, "reasoning": "The question is safe to answer."}

    Always ensure your response is a valid JSON object matching this schema.''',
    output_type=SupportQuestionOutput,
    model="gpt-4o-mini",
    tools=[]
)

@input_guardrail
async def question_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str
) -> GuardrailFunctionOutput:
    
    print(f"\n[DEBUG] question_guardrail entered with input: '{input}'") 
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    guardrail_output: SupportQuestionOutput = result.final_output
    print(f"[DEBUG] Guardrail agent response: is_question_unsafe={guardrail_output.is_question_unsafe}, reasoning='{guardrail_output.reasoning}'")
    
    print('type(result.final_output):', type(result.final_output))
    if guardrail_output.is_question_unsafe:
        print("[DEBUG] Guardrail tripwire TRIGGERED by unsafe content.")


    print("[DEBUG] question_guardrail finished without triggering tripwire.")
    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_question_unsafe,
    ) 