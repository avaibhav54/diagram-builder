import requests
import json
import os
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

# Get API key from environment variable

API_KEY = "add your API key here"
def generate_diagram(description, diagram_type):
    """
    Generate Mermaid diagram code from text description using AI
    
    Args:
        description (str): Text description of the diagram
        diagram_type (str): Type of diagram to generate
    
    Returns:
        str: Mermaid syntax code for the requested diagram
    """
    # Convert diagram type to Mermaid syntax type
    diagram_type_map = {
        "Sequence Diagram": "sequenceDiagram",
        "Flowchart": "flowchart TD",
        "Class Diagram": "classDiagram",
        "Entity Relationship": "erDiagram",
        "State Diagram": "stateDiagram-v2",
        "Gantt Chart": "gantt"
    }
    
    mermaid_type = diagram_type_map.get(diagram_type, "sequenceDiagram")
    
    # System prompt to guide AI behavior
    system_prompt = """
    You are an expert in technical diagrams and Mermaid syntax. Your job is to accurately convert text descriptions into valid Mermaid diagrams. Follow these rules:
    - Identify the diagram type (e.g., sequence, flowchart, class, ER, state, or Gantt).
    - Analyze the provided description to extract key entities, relationships, and interactions.
    - Generate the correct Mermaid code by structuring it logically and maintaining readability.
    - Avoid unnecessary explanations—output only the Mermaid syntax, starting directly with '{mermaid_type}'.
    """.strip()
    
    # User prompt with detailed instructions
    user_prompt = f"""
    Convert the following description into a valid Mermaid diagram of type '{diagram_type}'.
    Return ONLY the Mermaid code without any explanation, markdown formatting, or code blocks.
    Start with '{mermaid_type}'.
    
    Description: {description}
    """.strip()
    
    try:
        # Call OpenAI API
        if API_KEY:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }
            
            payload = {
                "model": "gpt-4-turbo",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 1000
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            )
            
            if response.status_code == 200:
                result = response.json()
                mermaid_code = result["choices"][0]["message"]["content"].strip()
                return mermaid_code
            else:
                return fallback_diagram(diagram_type)
        else:
            return fallback_diagram(diagram_type)
    
    except Exception as e:
        print(f"Error generating diagram: {e}")
        return fallback_diagram(diagram_type)


def fallback_diagram(diagram_type):
    """Provide a fallback diagram when API call fails"""
    diagram_type_map = {
        "Sequence Diagram": """sequenceDiagram
    participant User
    participant System
    User->>System: Action
    System->>User: Response""",
        
        "Flowchart": """flowchart TD
    A[Start] --> B[Process]
    B --> C[End]""",
        
        "Class Diagram": """classDiagram
    class Example {
        +attribute: type
        +method(): return_type
    }""",
        
        "Entity Relationship": """erDiagram
    ENTITY1 ||--o{ ENTITY2 : relationship""",
        
        "State Diagram": """stateDiagram-v2
    [*] --> State1
    State1 --> [*]""",
        
        "Gantt Chart": """gantt
    title Example Gantt
    section Section
    Task1 :a1, 2023-01-01, 30d
    Task2 :after a1, 20d"""
    }
    
    return diagram_type_map.get(diagram_type, "sequenceDiagram\nparticipant A\nparticipant B\nA->>B: Hello")
