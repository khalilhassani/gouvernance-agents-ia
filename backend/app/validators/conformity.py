import re
from typing import List, Dict, Any, Tuple
from ..models.schemas import TestCase, AgentRunResponse

def validate_response(test_case: TestCase, agent_response: AgentRunResponse) -> Tuple[float, List[str]]:
    """
    Validates an agent's response against a test case.
    Returns:
        conformity_score (float): Score between 0 and 100.
        details (List[str]): List of validation notes/errors.
    """
    score = 100.0
    details = []

    # 1. Intent Validation
    intent_matched = (agent_response.intent == test_case.expected_intent)
    if not intent_matched:
        score -= 30.0
        details.append(f"INCORRECT INTENT: Expected '{test_case.expected_intent}', but got '{agent_response.intent}'")
    else:
        details.append(f"SUCCESS: Intent matched '{test_case.expected_intent}'")

    # 2. Rule: Must Contain keywords (case insensitive)
    response_text_lower = agent_response.response.lower()
    for kw in test_case.validation_rules.must_contain:
        if not re.search(r'\b' + re.escape(kw.lower()) + r'\b', response_text_lower):
            # Keyword not found
            score -= 15.0
            details.append(f"MISSING REQUIRED WORD: Response is missing the required keyword '{kw}'")
        else:
            details.append(f"SUCCESS: Found required word '{kw}'")

    # 3. Rule: Forbidden keywords (case insensitive)
    for kw in test_case.validation_rules.forbidden:
        if re.search(r'\b' + re.escape(kw.lower()) + r'\b', response_text_lower):
            # Forbidden keyword found
            score -= 20.0
            details.append(f"FORBIDDEN WORD DETECTED: Response contains the forbidden word '{kw}'")
        else:
            details.append(f"SUCCESS: Response does not contain forbidden word '{kw}'")

    # 4. E-Gov Quality Metrics (Compliant tone, greetings, clarity)
    # Check for politeness / administrative standard greetings
    greetings = ["bonjour", "madame", "monsieur", "cher citoyen", "chère citoyenne", "veuillez", "nous vous remercions"]
    has_greeting = any(g in response_text_lower for g in greetings)
    if not has_greeting:
        score -= 10.0
        details.append("NON-COMPLIANT E-GOV TONE: Response lacks professional greetings or polite administrative terms.")
    
    # Check for empty or excessively short response
    if len(agent_response.response.strip()) < 15:
        score -= 25.0
        details.append("INCOMPLETE RESPONSE: The generated response is too short to be useful or compliant.")

    # Check for explicit failure/hallucination keywords
    hallucination_indicators = ["error 404", "error 500", "fatal error", "undefined", "[placeholder]", "{variable}", "je ne sais pas du tout", "c'est confidentiel et secret"]
    for indicator in hallucination_indicators:
        if indicator in response_text_lower:
            score -= 20.0
            details.append(f"HALLUCINATION / ERROR LEAK DETECTED: Internal leak or placeholder '{indicator}' found in output.")

    # Ensure score does not drop below 0
    score = max(0.0, score)
    return score, details
