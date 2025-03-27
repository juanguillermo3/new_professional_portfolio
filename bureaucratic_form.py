import streamlit as st

import streamlit as st

def _generate_bureaucratic_html(details: dict) -> str:
    """
    Generates the HTML for a bureaucratic-style form using compact pills with hover effects.

    :param details: Dictionary containing field names as keys and corresponding values.
    :return: A string containing the HTML markup.
    """
    
    style = """
    <style>
    .bureau-field {
        display: inline-flex;
        align-items: center;
        padding: 6px 8px;
        margin: 2px;
        border-radius: 4px;
        background: #BFBFBF;  
        color: #FFF;  
        font-size: 14px;
        white-space: nowrap;
        border: 1.5px solid #DDD;  
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); 
        transition: all 0.3s ease-in-out; /* Smooth transition */
    }
    .bureau-label {
        font-weight: bold;
        margin-right: 4px;
        color: #FFF;  
        font-size: 90%;
    }
    
    /* Hover effect */
    .bureau-field:hover {
        background: #A6A6A6;  /* Darker gray */
        color: #FFF;
        transform: scale(1.1);  /* Slight scale up */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Floating effect */
        z-index: 10; /* Bring to front */
    }
    </style>
    """

    fields_html = []

    for field_name, field_value in details.items():
        # Create a label pill
        fields_html.append(f"<div class='bureau-field'><span class='bureau-label'>{field_name}:</span></div>")

        # Normalize values to a list
        if isinstance(field_value, str):
            field_value = [item.strip() for item in field_value.split(',')]  
        elif isinstance(field_value, list):
            field_value = [str(item).strip() for item in field_value]  
        else:
            field_value = [str(field_value)]  

        # Create a pill for each tokenized value
        fields_html.extend(f"<div class='bureau-field'>{value}</div>" for value in field_value)

    return style + " ".join(fields_html)

def render_bureaucratic_form(details: dict):
    """
    Renders a bureaucratic-style form in Streamlit with hover effects.
    
    :param details: Dictionary containing field names as keys and corresponding values.
    """
    st.markdown(_generate_bureaucratic_html(details), unsafe_allow_html=True)

