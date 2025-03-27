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

def _generate_bureaucratic_html(details: dict) -> str:
    """
    Generates the HTML for a bureaucratic-style form using compact pills with hover effects.
    Only 12 pills are visible initially, and the rest appear smoothly on hover.

    :param details: Dictionary containing field names as keys and corresponding values.
    :return: A string containing the HTML markup.
    """
    
    style = """
    <style>
    .bureau-container {
        display: flex;
        flex-wrap: wrap;
        max-width: 600px;  /* Prevents excessive stretching */
        padding: 10px;
        border-radius: 8px;
        background: #FAFAFA; /* Ultra-light gray for contrast */
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
        background: #E0E0E0;  /* Soft Light Gray */
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
        color: #5E5E5E;  /* Deep Gray */
        font-size: 90%;
    }

    /* Initially hidden pills */
    .hidden-pill {
        opacity: 0;
        max-width: 0;
        padding: 0;
        margin: 0;
        transition: opacity 0.5s ease-in-out, max-width 0.5s ease-in-out, padding 0.5s ease-in-out, margin 0.5s ease-in-out;
    }

    /* Reveal pills when the container is hovered */
    .bureau-container:hover .hidden-pill {
        opacity: 1;
        max-width: 200px;  /* Allows proper expansion */
        padding: 6px 10px;
        margin: 3px;
    }

    /* Hover effect for visible pills */
    .bureau-field:hover {
        background: #F5F5F5;  /* Bright Silver Gray */
        color: #333333;
        transform: scale(1.05);
        box-shadow: 0 4px 10px rgba(200, 200, 200, 0.7);
        z-index: 10;
        cursor: pointer;
    }
    </style>
    """

    fields_html = []
    visible_limit = 12  # Number of pills visible initially

    for i, (field_name, field_value) in enumerate(details.items()):
        # Create a label pill
        pill_class = "bureau-field"
        if i >= visible_limit:
            pill_class += " hidden-pill"

        fields_html.append(f"<div class='{pill_class}'><span class='bureau-label'>{field_name}:</span></div>")

        # Normalize values to a list
        if isinstance(field_value, str):
            field_value = [item.strip() for item in field_value.split(',')]  
        elif isinstance(field_value, list):
            field_value = [str(item).strip() for item in field_value]  
        else:
            field_value = [str(field_value)]  

        # Create a pill for each tokenized value
        for j, value in enumerate(field_value):
            pill_class = "bureau-field"
            if i + j >= visible_limit:  
                pill_class += " hidden-pill"
            
            fields_html.append(f"<div class='{pill_class}'>{value}</div>")

    return style + f"<div class='bureau-container'>{' '.join(fields_html)}</div>"


def render_bureaucratic_form(details: dict):
    """
    Renders a bureaucratic-style form in Streamlit with hover effects.
    
    :param details: Dictionary containing field names as keys and corresponding values.
    """
    st.markdown(_generate_bureaucratic_html(details), unsafe_allow_html=True)
