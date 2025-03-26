import streamlit as st

def _generate_bureaucratic_html(details: dict) -> str:
    """
    Generates the HTML for a bureaucratic-style form using compact pills.
    
    :param details: Dictionary containing field names as keys and corresponding values.
    :return: A string containing the HTML markup.
    """
    style = """
    <style>
    .bureau-field {
        display: inline-flex;
        align-items: center;
        padding: 6px 6px;
        margin: 4px;
        border-radius: 2px;
        background: #f4f4f4;  /* Subtle gray background */
        font-size: 14px;
        white-space: nowrap;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);
    }
    .bureau-label {
        font-weight: bold;
        margin-right: 6px;
        color: #555;
        font-size: 90%;
    }
    </style>
    """
    
    fields_html = []
    
    for field_name, field_value in details.items():
        if isinstance(field_value, str) and ',' in field_value:
            field_value = [item.strip() for item in field_value.split(',')]
        
        if isinstance(field_value, list):
            fields_html.append(f"<div class='bureau-field'><span class='bureau-label'>{field_name}:</span></div>")
            fields_html.extend(
                [f"<div class='bureau-field'>{value}</div>" for value in field_value]
            )
        else:
            fields_html.append(
                f"<div class='bureau-field'><span class='bureau-label'>{field_name}:</span> {field_value}</div>"
            )
    
    return style + " ".join(fields_html)

def _generate_bureaucratic_html(details: dict) -> str:
    """
    Generates the HTML for a bureaucratic-style form using compact pills.

    :param details: Dictionary containing field names as keys and corresponding values.
    :return: A string containing the HTML markup.
    """
    
    style = """
    <style>
    .bureau-field {
        display: inline-flex;
        align-items: center;
        padding: 6px 8px;
        margin: 2px;  /* Keeps pills compact */
        border-radius: 4px;
        background: #D6D6D6;  /* Soft gray */
        color: #333;  /* Dark gray text for readability */
        font-size: 14px;
        white-space: nowrap;
        border: 1.5px solid #EEE;  /* Softer border */
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); /* Gentle shadow */
    }
    .bureau-label {
        font-weight: bold;
        margin-right: 4px;
        color: #333;  /* Dark gray for consistency */
        font-size: 90%;
    }
    </style>
    """




    fields_html = []

    for field_name, field_value in details.items():
        # Always create a label pill
        fields_html.append(f"<div class='bureau-field'><span class='bureau-label'>{field_name}:</span></div>")

        # Normalize values to a list (tokenizing opportunity)
        if isinstance(field_value, str):
            field_value = [item.strip() for item in field_value.split(',')]  # Tokenize by comma
        elif isinstance(field_value, list):
            field_value = [str(item).strip() for item in field_value]  # Ensure all list items are strings
        else:
            field_value = [str(field_value)]  # Convert single values to string-wrapped lists

        # Create a pill for each tokenized value
        fields_html.extend(f"<div class='bureau-field'>{value}</div>" for value in field_value)

    return style + " ".join(fields_html)



def render_bureaucratic_form(details: dict):
    """
    Renders a bureaucratic-style form in Streamlit.
    
    :param details: Dictionary containing field names as keys and corresponding values.
    """
    st.markdown(_generate_bureaucratic_html(details), unsafe_allow_html=True)
