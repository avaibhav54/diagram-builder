import re
import json
import requests
import os
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("OPENAI_API_KEY")
def validate_diagram(mermaid_code):
    """
    Validate the generated Mermaid code
    
    Args:
        mermaid_code (str): Mermaid syntax code to validate
        
    Returns:
        tuple: (is_valid, feedback)
    """
    # Basic validation checks
    if not mermaid_code or len(mermaid_code) < 10:
        return False, "Generated code is too short or empty"
    
    # Basic syntax validation based on diagram type
    first_line = mermaid_code.strip().split('\n')[0].strip()
    
    diagram_validators = {
        "sequenceDiagram": validate_sequence_diagram,
        "flowchart": validate_flowchart,
        "classDiagram": validate_class_diagram,
        "erDiagram": validate_er_diagram,
        "stateDiagram-v2": validate_state_diagram,
        "gantt": validate_gantt_chart
    }
    
    # Find the appropriate validator
    for diagram_type, validator_func in diagram_validators.items():
        if diagram_type in first_line:
            return validator_func(mermaid_code)
    
    # If diagram type not recognized, use AI to validate
    return validate_with_ai(mermaid_code)


def validate_sequence_diagram(code):
    """Validate sequence diagram syntax"""
    # Check for basic sequence diagram elements
    if not re.search(r'participant\s+\w+', code, re.IGNORECASE):
        return False, "Sequence diagram should define at least one participant"
    
    if not re.search(r'[-=]>>', code):
        return False, "Sequence diagram should have at least one message/action"
    
    return True, "Sequence diagram looks valid"


def validate_flowchart(code):
    """Validate flowchart syntax"""
    # Check for node definitions and connections
    if not re.search(r'\w+\s*(\[.*?\]|\(.*?\)|\{.*?\}|<.*?>)', code):
        return False, "Flowchart should define at least one node"
    
    if not re.search(r'-->', code):
        return False, "Flowchart should have at least one connection"
    
    return True, "Flowchart looks valid"


def validate_class_diagram(code):
    """Validate class diagram syntax"""
    if not re.search(r'class\s+\w+\s*\{', code):
        return False, "Class diagram should define at least one class"
    
    return True, "Class diagram looks valid"


def validate_er_diagram(code):
    """Validate entity relationship diagram syntax"""
    if not re.search(r'\w+\s+\|[|o]?--[|o]?\{\s+\w+', code):
        return False, "ER diagram should define at least one relationship"
    
    return True, "ER diagram looks valid"


def validate_state_diagram(code):
    """Validate state diagram syntax"""
    if not re.search(r'\[*\]\s*-->', code) and not re.search(r'-->\s*\[*\]', code):
        return False, "State diagram should have at least a start or end state"
    
    return True, "State diagram looks valid"


def validate_gantt_chart(code):
    """Validate Gantt chart syntax"""
    if not re.search(r'title\s+', code, re.IGNORECASE):
        return False, "Gantt chart should have a title"
    
    if not re.search(r'section\s+', code, re.IGNORECASE):
        return False, "Gantt chart should have at least one section"
    
    return True, "Gantt chart looks valid"


def validate_with_ai(mermaid_code):
    """
    Use AI to validate the Mermaid code if standard validation fails
    
    Args:
        mermaid_code (str): Mermaid syntax code to validate
        
    Returns:
        tuple: (is_valid, feedback)
    """
    try:
        if not API_KEY:
            # If no API key, assume it's valid but warn
            return True, "Could not perform deep validation (API key missing)"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        prompt = f"""
        Validate if the following Mermaid diagram code is syntactically correct.
        Return ONLY a JSON object with two fields:
        1. "is_valid": a boolean (true/false)
        2. "feedback": a string with validation feedback
        
        Mermaid code:
        ```
        {mermaid_code}
        ```
        """
        
        payload = {
            "model": "gpt-4-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 300,
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = json.loads(result["choices"][0]["message"]["content"])
            return ai_response["is_valid"], ai_response["feedback"]
        else:
            # If API call fails, assume it might be valid
            return True, "Could not perform deep validation (API error)"
    
    except Exception as e:
        print(f"Error validating with AI: {e}")
        return True, "Could not perform deep validation (exception)"
