import streamlit as st

def _generate_bureaucratic_html(details: dict) -> str:
    """
    Generates the HTML for a bureaucratic-style form using compact pills with hover effects.
    Now in grayscale.
    
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
        background: #4A4A4A;  /* Dark Gray */
        color: #FFFFFF;  
        font-size: 14px;
        white-space: nowrap;
        border: 1.5px solid #2E2E2E;  /* Darker Gray */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15); 
        transition: all 0.3s ease-in-out; /* Smooth animation */
        cursor: pointer;
    }
    .bureau-label {
        font-weight: bold;
        margin-right: 6px;
        color: #DADADA;  /* Light Gray */
        font-size: 90%;
    }
    
    /* Hover effect */
    .bureau-field:hover {
        background: #6A6A6A;  /* Medium Gray */
        color: #FFFFFF;
        transform: scale(1.1);
        box-shadow: 0 4px 10px rgba(100, 100, 100, 0.5); /* Soft gray glow effect */
        z-index: 10;
        cursor: pointer;
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
