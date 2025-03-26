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
        padding: 6px 12px;
        margin: 2px;
        border-radius: 5px;
        background: #f4f4f4;  /* Subtle gray background */
        font-size: 15px;
        white-space: nowrap;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .bureau-label {
        font-weight: bold;
        margin-right: 6px;
        color: #555;
        font-size: 75%;
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

def render_bureaucratic_form(details: dict):
    """
    Renders a bureaucratic-style form in Streamlit.
    
    :param details: Dictionary containing field names as keys and corresponding values.
    """
    st.markdown(_generate_bureaucratic_html(details), unsafe_allow_html=True)
