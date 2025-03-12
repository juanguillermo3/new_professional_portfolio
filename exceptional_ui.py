"""
title: Exceptional UI
description: Implements beautiful front-end components using Streamlit, HTML, and CSS to create a smooth and delightful user experience.  
"""

import streamlit as st
import time

#
# (0)
#
def _custom_tooltip_html(element_id: str, tooltip_text: str) -> str:
    """
    Generates the HTML + CSS for a tooltip applied to an existing component.
    
    Args:
        element_id (str): The ID of the element to attach the tooltip to.
        tooltip_text (str): The tooltip content.
    
    Returns:
        str: The formatted CSS and HTML for the tooltip.
    """
    return f"""
    <style>
    #{element_id} {{
        position: relative;
        display: inline-block;
    }}

    #{element_id}::after {{
        content: "{tooltip_text}";
        position: absolute;
        bottom: 120%;
        left: 50%;
        transform: translateX(-50%) scale(1);
        background-color: #333;
        color: white;
        padding: 6px 10px;
        border-radius: 5px;
        font-size: 14px;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: 
            opacity 0.3s ease-in-out, 
            visibility 0.3s, 
            transform 0.2s ease-in-out;
    }}

    #{element_id}:hover::after {{
        opacity: 1;
        visibility: visible;
        transform: translateX(-50%) scale(1.1); /* Slightly enlarges on hover */
    }}
    </style>
    """
#
# (1)
#
def apply_custom_tooltip(element_id: str, tooltip_text: str, sys_prompt: str = "Juan says:"):
    """
    Applies a tooltip to an existing Streamlit component with hover scaling.
    
    Args:
        element_id (str): The ID of the element to attach the tooltip to.
        tooltip_text (str): The tooltip content.
        sys_prompt (str, optional): A prefix for the tooltip text. Defaults to "Juan says:".
    
    Usage:
        apply_custom_tooltip("my_button", "Click to submit")
    """
    full_tooltip_text = f"{sys_prompt} {tooltip_text}"
    st.markdown(_custom_tooltip_html(element_id, full_tooltip_text), unsafe_allow_html=True)

#
# (2)
#
def _custom_tooltip_with_frost_glass_html(element_id: str, tooltip_text: str, **design_params) -> str:
    """
    Generates the HTML + CSS for a frosted glass tooltip with customizable design parameters.
    
    Args:
        element_id (str): The ID of the element to attach the tooltip to.
        tooltip_text (str): The tooltip content.
        **design_params: Dictionary containing aesthetic parameters to override defaults.
    
    Returns:
        str: The formatted CSS and HTML for the tooltip with a frosted glass effect.
    """
    
    # Default design parameters
    default_params = {
        "tooltip_bottom_pos": "120%",  
        "tooltip_left_pos": "50%",  
        "tooltip_top_pos": "auto",  
        "tooltip_bg": "rgba(240, 240, 240, 0.3)",
        "tooltip_blur": "10px",
        "text_color": "black",
        "padding": "12px",
        "border_radius": "12px",
        "font_size": "14px",
        "box_shadow": "0px 12px 30px rgba(0, 0, 0, 0.2), 0px 2px 4px rgba(255, 255, 255, 0.2)",
        "border": "1px solid rgba(200, 200, 200, 0.3)",
        "opacity": "0",
        "visibility": "hidden",
        "transition": "opacity 0.3s ease-in-out, transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)",
        "hover_opacity": "1",
        "hover_transform": "translateX(-50%) scale(1.08)",
        "default_transform": "translateX(-50%) scale(0.95) translateZ(0)",
        "tooltip_width": "66%",
        "background_gradient": "radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 100%)",
        "z_index": "9999",  # Ensures tooltip appears on top
    }
    
    # Override defaults with user-supplied values
    params = {**default_params, **design_params}
    
    return f"""
    <style>
    #{element_id} {{
        position: relative;
        display: inline-block;
        cursor: pointer;
    }}

    #{element_id}::after {{
        content: '{tooltip_text}';
        position: absolute;
        top: {params["tooltip_top_pos"]};
        bottom: {params["tooltip_bottom_pos"]};
        left: {params["tooltip_left_pos"]};
        transform: {params["default_transform"]};
        background: {params["tooltip_bg"]}, {params["background_gradient"]};
        backdrop-filter: blur({params["tooltip_blur"]});
        color: {params["text_color"]};
        padding: {params["padding"]};
        border-radius: {params["border_radius"]};
        font-size: {params["font_size"]};
        white-space: normal;
        word-wrap: break-word;
        width: {params["tooltip_width"]};
        text-align: center;
        box-shadow: {params["box_shadow"]};
        border: {params["border"]};
        opacity: {params["opacity"]};
        visibility: {params["visibility"]};
        transition: {params["transition"]};
        pointer-events: none;
        z-index: {params["z_index"]};  /* Tooltip stays on top */
    }}

    #{element_id}:hover::after {{
        opacity: {params["hover_opacity"]};
        visibility: visible;
        transform: {params["hover_transform"]};
    }}

    /* Subtle floating animation for tooltip */
    #{element_id}:hover::after {{
        animation: floatingTooltip 1.5s ease-in-out infinite alternate;
    }}

    @keyframes floatingTooltip {{
        0% {{
            transform: translateX(-50%) translateY(0) scale(1.06);
        }}
        100% {{
            transform: translateX(-50%) translateY(-1px) scale(1.06);
        }}
    }}
    </style>
    """
    
import html
import hashlib
import datetime
import streamlit as st

def html_for_tooltip_from_large_list(items, label, element_id, color="#007BFF", emoji=None):
    """
    Generates an HTML snippet displaying a summarized preview of a list with a tooltip that appears on hover.

    Parameters:
        - items (list of str): The list of items to display.
        - label (str): Describes the type of items being enumerated.
        - element_id (str): The base ID of the element.
        - color (str): Color for the summary text (default: #007BFF).
        - emoji (str, optional): Emoji prepended to each listed item.

    Returns:
        - str: HTML snippet containing the summarized text and a tooltip for full details.
    """
    if not items:
        return f'<div style="color:gray;">No {label.lower()} listed</div>'

    # Generate a unique ID by hashing element_id with the current date
    unique_hash = hashlib.md5(f"{element_id}_{datetime.datetime.now().isoformat()}".encode()).hexdigest()[:10]
    unique_id = f"{element_id}_{unique_hash}"

    first_item = html.escape(items[0])
    summary = f"(and {len(items) - 1} more {label.lower()})" if len(items) > 1 else ""
    visible_text = f'<span id="{unique_id}" style="color:{color}; border-bottom: 1px dashed {color}; cursor: pointer;">{first_item} {summary}</span>'

    tooltip_content = "".join(
        f'<div style="color:{color}; margin-bottom: 4px;">{(emoji + " " if emoji else "")}{html.escape(item)}</div>'
        for item in items
    )

    # Define tooltip HTML
    tooltip_html = f"""
        <div style="position: relative; display: inline-block; max-width: 100%;">
            {visible_text}
            <div class="skills_tooltip" style="
                visibility: hidden;
                opacity: 0;
                background: rgba(20, 20, 20, 0.9);
                color: #ffffff;
                padding: 12px;
                border-radius: 8px;
                box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.5);
                position: absolute;
                left: 50%;
                top: 120%;
                width: 300px;
                text-align: left;
                z-index: 10;
                border: 1px solid rgba(255, 255, 255, 0.2);
                transform: translateX(-50%) translateY(5px);
                transition: visibility 0.3s ease-out, opacity 0.3s ease-out, transform 0.3s ease-out;
            ">
                <strong>All {label} listed:</strong>
                {tooltip_content}
            </div>
        </div>
    """

    # Inject CSS for hover-triggering logic
    st.markdown(f"""
    <style>
        #{unique_id}:hover + .skills_tooltip {{
            visibility: visible;
            opacity: 1;
            transform: translateX(-50%) translateY(0px) scale(1.05);
        }}
    </style>
    """, unsafe_allow_html=True)

    return tooltip_html



#
# (0)
#
import html
import hashlib
import datetime
import streamlit as st
import hashlib
import datetime
import html
import streamlit as st
#
# (1)
#
def html_for_tooltip_from_large_list(items, label, element_id, color="#007BFF", emoji=None):
    """
    Generates an HTML snippet displaying a summarized preview of a list with a tooltip that appears on hover.

    Parameters:
        - items (list of str): The list of items to display.
        - label (str): Describes the type of items being enumerated.
        - element_id (str): The base ID of the element.
        - color (str): Color for the summary text (default: #007BFF).
        - emoji (str, optional): Emoji prepended to each listed item.

    Returns:
        - tuple: (HTML snippet, unique tooltip ID)
    """
    if not items:
        return f'<div style="color:gray;">No {label.lower()} listed</div>', None

    # Generate a unique ID
    unique_hash = hashlib.md5(element_id.encode()).hexdigest()[:10]
    unique_id = f"{element_id}_{unique_hash}"

    first_item = html.escape(items[0])
    summary = f"(and {len(items) - 1} more {label.lower()})" if len(items) > 1 else ""
    visible_text = f'<span id="{unique_id}" style="color:{color}; border-bottom: 1px dashed {color}; cursor: pointer;">{first_item} {summary}</span>'

    tooltip_content = "".join(
        f'<div style="color:{color}; margin-bottom: 4px;">{(emoji + " " if emoji else "")}{html.escape(item)}</div>'
        for item in items
    )

    # Tooltip HTML (without CSS)
    tooltip_html = f"""
        <span id="{unique_id}" style="color:{color}; border-bottom: 1px dashed {color}; cursor: pointer;">
            {first_item} {summary}
        </span>
        <div class="skills_tooltip-{unique_id}" style="
            visibility: hidden;
            opacity: 0;
            background: rgba(20, 20, 20, 0.9);
            color: #ffffff;
            padding: 12px;
            border-radius: 8px;
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.5);
            position: absolute;
            left: 50%;
            top: 120%;
            max-width: 350px;
            text-align: left;
            z-index: 10;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transform: translateX(-50%) translateY(5px);
            transition: visibility 0.2s ease-out, opacity 0.2s ease-out, transform 0.2s ease-out;
            overflow-wrap: break-word;
        ">
            <strong>All {label} listed:</strong>
            {tooltip_content}
        </div>
    """

    return tooltip_html, unique_id
#
# (2)
#
def setup_tooltip_behavior(unique_id):
    """
    Injects the required CSS and behavior into Streamlit to activate the tooltip.

    Parameters:
        - unique_id (str): The unique tooltip identifier.

    Returns:
        - None
    """
    if not unique_id:
        return

    tooltip_css = f"""
    <style>
        #{unique_id}:hover + .skills_tooltip-{unique_id} {{
            visibility: visible;
            opacity: 1;
            transform: translateY(0px) scale(1.1);
        }}
    </style>
    """
    return tooltip_css 







import hashlib
import html
from datetime import datetime

def html_for_tooltip_from_large_list(items, label, color="#007BFF", emoji=None):
    """
    Generates an HTML snippet displaying a summarized preview of a list with a tooltip that appears on hover.

    Parameters:
        - items (list of str): The list of items to display.
        - label (str): Describes the type of items being enumerated.
        - color (str): Color for the summary text (default: #007BFF).
        - emoji (str, optional): Emoji prepended to each listed item.

    Returns:
        - tuple: (HTML snippet, unique tooltip ID)
    """
    if not items:
        return f'<div style="color:gray;">No {label.lower()} listed</div>', None

    # Compute a runtime unique hash based on the current timestamp
    unique_id = hashlib.md5(datetime.now().isoformat().encode()).hexdigest()[:10]

    first_item = html.escape(items[0])
    summary = f"(and {len(items) - 1} more {label.lower()})" if len(items) > 1 else ""

    visible_text = f'<span id="{unique_id}" class="tooltip-trigger">{first_item} {summary}</span>'

    tooltip_content = "".join(
        f'<div class="tooltip-item">{(emoji + " " if emoji else "")}{html.escape(item)}</div>'
        for item in items
    )

    tooltip_html = f"""
        {visible_text}
        <div class="skills_tooltip-{unique_id}">
            <strong>All {label} listed:</strong>
            {tooltip_content}
        </div>
    """

    return tooltip_html, unique_id


def setup_tooltip_behavior(unique_id):
    """
    Injects the required CSS and behavior into Streamlit to activate the tooltip.

    Parameters:
        - unique_id (str): The unique tooltip identifier.

    Returns:
        - str: The CSS to be injected into Streamlit
    """
    if not unique_id:
        return ""

    tooltip_css = f"""
    <style>
        .tooltip-trigger {{
            color: #007BFF;
            border-bottom: 1px dashed #007BFF;
            cursor: pointer;
            position: relative;
        }}

        .skills_tooltip-{unique_id} {{
            visibility: hidden;
            opacity: 0;
            background: rgba(20, 20, 20, 0.9);
            color: #ffffff;
            padding: 12px;
            border-radius: 8px;
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.5);
            position: absolute;
            left: 50%;
            top: 120%;
            max-width: 350px;
            text-align: left;
            z-index: 10;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transform: translateX(-50%) translateY(5px);
            transition: visibility 0.2s ease-out, opacity 0.2s ease-out, transform 0.2s ease-out;
            overflow-wrap: break-word;
        }}

        .tooltip-trigger:hover + .skills_tooltip-{unique_id} {{
            visibility: visible;
            opacity: 1;
            transform: translateY(0px) scale(1.1);
        }}

        .tooltip-item {{
            color: #007BFF;
            margin-bottom: 4px;
        }}
    </style>
    """
    return tooltip_css

