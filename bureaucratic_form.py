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
        padding: 6px 10px;
        margin: 3px;
        border-radius: 6px;
        background: #1E3A5F;  /* Navy Blue */
        color: #FFFFFF;  
        font-size: 14px;
        white-space: nowrap;
        border: 1.5px solid #294A70;  /* Darker navy border */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15); 
        transition: all 0.3s ease-in-out; /* Smooth animation */
        cursor: pointer;  /* Indicates interactivity */
    }
    .bureau-label {
        font-weight: bold;
        margin-right: 6px;
        color: #DDEEFF;  /* Light Crystal Blue */
        font-size: 90%;
    }
    
    /* Hover effect */
    .bureau-field:hover {
        background: #3A5F9E;  /* Crystal Blue */
        color: #FFFFFF;
        transform: scale(1.1);  /* Slight scale-up */
        box-shadow: 0 4px 10px rgba(58, 95, 158, 0.5); /* Soft glow effect */
        z-index: 10; /* Brings hovered element to front */
        cursor: pointer;   /* Special cursor */
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


