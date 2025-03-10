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
        "z_index": "99999",  # Ensures tooltip appears on top
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





