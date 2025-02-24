# Tech Doc Diagram Builder

A Streamlit application that converts natural language descriptions into various technical diagrams using Mermaid syntax.

## Features

- Generate multiple types of diagrams from text descriptions
- Supported diagram types:
  - Sequence Diagrams
  - Flowcharts
  - Class Diagrams
  - Entity Relationship Diagrams
  - State Diagrams
  - Gantt Charts
- Validate generated Mermaid code
- Export diagrams as code or images

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
2. Open your browser at `http://localhost:8501`
3. Enter a description of your diagram
4. Select the diagram type
5. Click "Generate Diagram"

## Project Structure

- `app.py` - Main Streamlit application
- `diagram_generator.py` - AI-based diagram code generator
- `diagram_validator.py` - Mermaid syntax validator
- `requirements.txt` - Project dependencies
- `.env` - Environment variables (API keys)

## How It Works

The application uses OpenAI's API to convert natural language descriptions into Mermaid diagram syntax. The generated code is then validated for basic syntax correctness and rendered using Mermaid.js.

## Future Enhancements

- Add support for exporting diagrams as PNG/SVG
- Implement diagram editing capabilities
- Add more diagram types
- Implement local diagram rendering without requiring internet access