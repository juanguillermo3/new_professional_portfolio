"""
title: Exceptional UI
description: Implements beautiful front-end components using Streamlit, HTML, and CSS to create a smooth and delightful user experience.  
"""

import streamlit as st

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
def _custom_tooltip_with_frost_glass_html(element_id: str, tooltip_text: str) -> str:
    """
    Generates the HTML + CSS for a frosted glass tooltip applied to an existing component.
    
    Args:
        element_id (str): The ID of the element to attach the tooltip to.
        tooltip_text (str): The tooltip content.
    
    Returns:
        str: The formatted CSS and HTML for the tooltip with a frosted glass effect.
    """
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
        bottom: 120%;
        left: 50%;
        transform: translateX(-50%) scale(0.95);
        background: rgba(240, 240, 240, 0.7); /* Frosted effect */
        backdrop-filter: blur(3px); /* Stronger blur for a glassy look */
        color: black;
        padding: 10px;
        border-radius: 8px;
        font-size: 14px;
        white-space: nowrap;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(200, 200, 200, 0.5);
        opacity: 0;
        visibility: hidden;
        transition: 
            opacity 0.3s ease-in-out, 
            visibility 0.3s ease-in-out, 
            transform 0.3s ease-in-out;
        pointer-events: none; /* Prevents accidental hover issues */
    }}

    #{element_id}:hover::after {{
        opacity: 1;
        visibility: visible;
        transform: translateX(-50%) scale(1.05); /* Slightly enlarges on hover */
    }}
    </style>
    """

