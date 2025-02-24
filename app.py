import streamlit as st
import os
from diagram_generator import *
from diagram_validator import *


st.set_page_config(page_title="Tech Doc Diagram Builder", layout="wide")

st.title("Tech Doc Diagram Builder")
st.markdown("Convert your tech explanations into beautiful diagrams")

# Sidebar for app navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", ["Diagram Generator", "About"])

if page == "Diagram Generator":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input")
        description = st.text_area(
            "Describe your diagram in detail:",
            height=300,
            placeholder="Example: Create a sequence diagram showing how a user logs in to a website. The user sends credentials to the front-end, which validates the format and sends them to the auth service. The auth service checks the database and returns a token if valid."
        )
        
        diagram_type = st.selectbox(
            "Select diagram type:",
            ["Sequence Diagram", "Flowchart", "Class Diagram", "Entity Relationship", "State Diagram", "Gantt Chart"]
        )
        
        generate_button = st.button("Generate Diagram")
        
        if generate_button and description:
            with st.spinner("Generating diagram..."):
                # Call the diagram generator function
                mermaid_code = generate_diagram(description, diagram_type)
                
                # Validate the generated code
                is_valid, feedback = validate_diagram(mermaid_code)
                
                if not is_valid:
                    st.error(f"Generated diagram has issues: {feedback}")
                    st.session_state.mermaid_code = mermaid_code  # Store for editing
                else:
                    st.success("Diagram generated successfully!")
                    st.session_state.mermaid_code = mermaid_code
        
        # Add editable text area for the Mermaid code
        if 'mermaid_code' in st.session_state:
            st.subheader("Edit Mermaid Code")
            edited_code = st.text_area(
                "Edit the generated code directly:",
                value=st.session_state.mermaid_code, 
                height=300,
                key="editable_mermaid"
            )
            
            # Update the mermaid code in session state when edited
            if edited_code != st.session_state.mermaid_code:
                # Validate the edited code
                is_valid, feedback = validate_diagram(edited_code)
                
                if not is_valid:
                    st.warning(f"Warning: {feedback}")
                
                # Update the code regardless of validation result so user can fix it
                st.session_state.mermaid_code = edited_code
            
            # Add an explicit update button for clarity
            if st.button("Update Diagram"):
                st.success("Diagram updated!")
                
            # Download button for the code
            st.download_button(
                label="Download Mermaid Code",
                data=st.session_state.mermaid_code,
                file_name="diagram.mmd",
                mime="text/plain"
            )
    
    with col2:
        st.subheader("Output")
        
        # Calculate diagram height based on code complexity
        def estimate_diagram_height(code):
            # Count the number of lines
            line_count = code.count('\n') + 1
            
            # Estimate based on diagram type
            if "sequenceDiagram" in code:
                # Sequence diagrams tend to be taller
                return max(600, line_count * 35)
            elif "flowchart" in code:
                # Flowcharts can be wide or tall depending on direction
                if "LR" in code or "RL" in code:
                    return max(500, line_count * 25)
                else:
                    return max(600, line_count * 35)
            elif "classDiagram" in code:
                # Class diagrams with lots of methods need more height
                return max(600, line_count * 30)
            elif "gantt" in code:
                # Gantt charts are usually wider than tall
                return max(400, line_count * 25)
            else:
                # Default height calculation
                return max(500, line_count * 30)
        
        # Always display current diagram based on session state
        if 'mermaid_code' in st.session_state:
            # Estimate appropriate height for the diagram
            estimated_height = estimate_diagram_height(st.session_state.mermaid_code)
            
            # Create container with scrollbar for very large diagrams
            with st.container():
                # Display the diagram using HTML and JavaScript with responsive sizing
                html_content = f"""
                <div style="width: 100%; overflow: auto;">
                    <div class="mermaid">
                    {st.session_state.mermaid_code}
                    </div>
                </div>
                <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                <script>
                    mermaid.initialize({{
                        startOnLoad: true,
                        theme: 'default',
                        securityLevel: 'loose',
                        logLevel: 'error'
                    }});
                </script>
                """
                st.components.v1.html(html_content, height=estimated_height, scrolling=True)
            
            # Display zoom controls
            zoom_col1, zoom_col2, zoom_col3 = st.columns([1, 1, 2])
            with zoom_col1:
                if st.button("Zoom In"):
                    if 'zoom_level' not in st.session_state:
                        st.session_state.zoom_level = 1
                    st.session_state.zoom_level = min(2.0, st.session_state.zoom_level + 0.2)
            
            with zoom_col2:
                if st.button("Zoom Out"):
                    if 'zoom_level' not in st.session_state:
                        st.session_state.zoom_level = 1
                    st.session_state.zoom_level = max(0.5, st.session_state.zoom_level - 0.2)
            
            with zoom_col3:
                if 'zoom_level' not in st.session_state:
                    st.session_state.zoom_level = 1
                st.text(f"Zoom level: {st.session_state.zoom_level:.1f}x")
            
            # Export options
            st.subheader("Export Options")
            col_png, col_svg = st.columns(2)
            with col_png:
                st.button("Export as PNG", disabled=True, help="This feature requires additional setup")
            with col_svg:
                st.button("Export as SVG", disabled=True, help="This feature requires additional setup")

        else:
            st.info("Generate a diagram to see the preview here")

# elif page == "About":
#     st.header("About Tech Doc Diagram Builder")
#     st.markdown("""
#     This tool helps you create technical diagrams from text descriptions. Simply:
    
#     1. Enter a detailed description of what you want to visualize
#     2. Select the diagram type
#     3. Click 'Generate Diagram'
#     4. Edit the generated Mermaid code directly if needed
    
#     The app will convert your description into a Mermaid diagram, which you can then edit, download or export.
    
#     ### Supported Diagram Types
#     - Sequence Diagrams
#     - Flowcharts
#     - Class Diagrams
#     - Entity Relationship Diagrams
#     - State Diagrams
#     - Gantt Charts
    
#     ### How It Works
#     The app uses AI to convert your natural language description into Mermaid syntax,
#     validates the generated code, and renders the diagram for preview. You can also
#     manually edit the Mermaid code to customize your diagram further.
#     """)