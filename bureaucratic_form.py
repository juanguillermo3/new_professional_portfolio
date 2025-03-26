import streamlit as st

def _generate_bureaucratic_html(details: dict) -> str:
    """
    Generates the HTML for a bureaucratic-style form using compact pills with responsive font sizes.

    :param details: Dictionary containing field names as keys and corresponding values.
    :return: A string containing the HTML markup.
    """
    style = """
    <style>
    .bureau-container {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;  /* Space between pills */
        padding: 10px;
        max-width: 100%;
    }
    
    .bureau-field {
        display: inline-flex;
        align-items: center;
        padding: clamp(6px, 1vw, 12px) clamp(8px, 2vw, 16px);
        margin: 2px;
        border-radius: 8px;
        background: #f4f4f4;  /* Subtle gray background */
        font-size: clamp(12px, 2vw, 16px);
        white-space: nowrap;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease-in-out;
    }

    .bureau-label {
        font-weight: bold;
        margin-right: 6px;
        color: #555;
        font-size: clamp(11px, 1.8vw, 14px);
    }

    /* Hover effect for a subtle interactive feel */
    .bureau-field:hover {
        background: #e0e0e0;
        transform: scale(1.05);
    }

    @media (max-width: 600px) {
        .bureau-container {
            flex-direction: column;
            align-items: flex-start;
        }
        .bureau-field {
            width: auto; /* Adjust for smaller screens */
        }
    }
    </style>
    """
    
    fields_html = ["<div class='bureau-container'>"]
    
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
    
    fields_html.append("</div>")  # Close container div
    return style + " ".join(fields_html)


def render_bureaucratic_form(details: dict):
    """
    Renders a bureaucratic-style form in Streamlit.
    
    :param details: Dictionary containing field names as keys and corresponding values.
    """
    st.markdown(_generate_bureaucratic_html(details), unsafe_allow_html=True)
