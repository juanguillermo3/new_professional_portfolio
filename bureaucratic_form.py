import streamlit as st

#
# (0)
#
def _generate_bureaucratic_html(details: dict) -> str:
    """
    Generates the HTML for a bureaucratic-style form using compact pills with hover effects.
    Only 5 pills are visible initially, with more appearing smoothly on hover.
    A special hint pill is visible at first but disappears on hover.

    :param details: Dictionary containing field names as keys and corresponding values.
    :return: A string containing the HTML markup.
    """
    
    style = """
    <style>
    .bureau-container {
        display: flex;
        flex-wrap: wrap;
        width: 100%;
        padding: 10px;
        margin: 15px 0;
        border-radius: 8px;
        background: #FAFAFA;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        transition: max-height 0.5s ease-in-out;
    }

    .bureau-field {
        display: inline-flex;
        align-items: center;
        padding: 6px 10px;
        margin: 3px;
        border-radius: 6px;
        background: #E0E0E0;
        color: #333333;
        font-size: 14px;
        white-space: nowrap;
        border: 1.5px solid #BDBDBD;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
        cursor: pointer;
    }

    .bureau-label {
        font-weight: bold;
        margin-right: 6px;
        color: #5E5E5E;
        font-size: 90%;
    }

    .hidden-pill {
        opacity: 0;
        max-width: 0;
        padding: 0;
        margin: 0;
        transition: opacity 0.5s ease-in-out, max-width 0.5s ease-in-out, padding 0.5s ease-in-out, margin 0.5s ease-in-out;
    }

    .bureau-container:hover .hidden-pill {
        opacity: 1;
        max-width: 200px;
        padding: 6px 10px;
        margin: 3px;
    }

    .bureau-field:hover {
        background: #F5F5F5;
        transform: scale(1.05);
        box-shadow: 0 4px 10px rgba(200, 200, 200, 0.7);
        z-index: 10;
    }

    .hint-pill {
        background: #BBDEFB;
        color: #1E88E5;
        font-weight: bold;
    }

    .bureau-container:hover .hint-pill {
        opacity: 0;
        max-width: 0;
        padding: 0;
        margin: 0;
    }
    </style>
    """

    fields_html = []
    visible_limit = 5  # Number of pills visible initially

    for i, (field_name, field_value) in enumerate(details.items()):
        pill_class = "bureau-field"
        if i >= visible_limit:
            pill_class += " hidden-pill"

        if i == visible_limit:
            fields_html.append(f"<div class='{pill_class}'><span class='bureau-label'>{field_name}:</span></div>")

        if isinstance(field_value, str):
            field_value = [item.strip() for item in field_value.split(',')]
        elif isinstance(field_value, list):
            field_value = [str(item).strip() for item in field_value]
        else:
            field_value = [str(field_value)]

        for j, value in enumerate(field_value):
            pill_class = "bureau-field"
            if i + j >= visible_limit:
                pill_class += " hidden-pill"
            fields_html.append(f"<div class='{pill_class}'>{value}</div>")

    
    return style + f"<div class='bureau-container'>{' '.join(fields_html)}</div>"



#
# (1)
#
def render_bureaucratic_form(details: dict):
    """
    Renders a bureaucratic-style form in Streamlit with hover effects.
    
    :param details: Dictionary containing field names as keys and corresponding values.
    """
    st.markdown(_generate_bureaucratic_html(details), unsafe_allow_html=True)
