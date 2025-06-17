from agents import input_guardrail, GuardrailFunctionOutput
from typing import Optional

@input_guardrail
def name_guardrail(input_text: str) -> Optional[GuardrailFunctionOutput]:
    """
    Validates that the input contains a name and is appropriate for a welcome message.
    
    Args:
        input_text (str): The input text to validate
        
    Returns:
        Optional[GuardrailFunctionOutput]: None if validation passes, or a GuardrailFunctionOutput with error details
    """
    if not input_text or len(input_text.strip()) < 2:
        return GuardrailFunctionOutput(
            is_valid=False,
            error_message="Input must contain a valid name (at least 2 characters)."
        )
    
    inappropriate_words = ["bad", "wrong", "error", "fail", "invalid"]
    if any(word in input_text.lower() for word in inappropriate_words):
        return GuardrailFunctionOutput(
            is_valid=False,
            error_message="Input contains inappropriate content for a welcome message."
        )
    
    if len(input_text) > 100:
        return GuardrailFunctionOutput(
            is_valid=False,
            error_message="Input is too long. Please provide just the name."
        )
    
    return None 