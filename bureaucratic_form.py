import streamlit as st

def _generate_bureaucratic_html(details: dict) -> str:
    """
    Generates the HTML for a bureaucratic-style form using compact pills with hover effects.
    Now with a light gray, positive aesthetic.

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
        background: #E0E0E0;  /* Soft Light Gray */
        color: #333333;  /* Dark Text for readability */
        font-size: 14px;
        white-space: nowrap;
        border: 1.5px solid #BDBDBD;  /* Slightly Darker Gray */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); 
        transition: all 0.3s ease-in-out; /* Smooth animation */
        cursor: pointer;
    }
    .bureau-label {
        font-weight: bold;
        margin-right: 6px;
        color: #5E5E5E;  /* Deep Gray for contrast */
        font-size: 90%;
    }
    
    /* Hover effect */
    .bureau-field:hover {
        background: #F5F5F5;  /* Bright Silver Gray */
        color: #333333;
        transform: scale(1.05);  /* Slight scale-up */
        box-shadow: 0 4px 10px rgba(200, 200, 200, 0.7); /* Soft white glow */
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
    """
    st.markdown(_generate_bureaucratic_html(details), unsafe_allow_html=True)
