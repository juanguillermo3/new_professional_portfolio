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

import hashlib
import html

import html

import html

def html_for_tooltip_from_large_list(items, label, element_id, style_prefix="", color="#007BFF", emoji=None):
    """
    Generates an HTML tooltip for displaying a large list with a summarized preview.

    Parameters:
        - items (list of str): The list of items to display.
        - label (str): Describes the type of items being enumerated.
        - element_id (str): The ID of the element that will trigger the tooltip.
        - style_prefix (str): Prefix for tooltip CSS class to allow variations in design.
        - color (str): Color for the tooltip text (default: navigable blue #007BFF).
        - emoji (str, optional): Emoji prepended to each listed item.

    Returns:
        - str: HTML snippet containing the summarized text.
    """
    if not items:
        return f'<div style="color:gray;">No {label.lower()} listed</div>'
    
    # Escape and format first item
    first_item = html.escape(items[0])
    summary = f"(and {len(items) - 1} more {label.lower()})" if len(items) > 1 else ""
    
    # Updated visible text styling
    visible_text = f"""
    <span id="{element_id}" style="
        color: {color};
        border-bottom: 1px dashed {color};
        cursor: pointer;
        font-weight: bold;
        display: inline-block;
        transition: color 0.3s ease-in-out;">
        {first_item} {summary}
    </span>
    """

    return f"""
    <div style="position: relative; display: inline-block;">
        {visible_text}
    </div>
    """




def install_tooltip_triggering_logic(element_id, style_prefix=""):
    """
    Generates the CSS logic for triggering a tooltip when hovering over the given element.

    Parameters:
        - element_id (str): The ID of the element that will trigger the tooltip.
        - style_prefix (str): Prefix for tooltip CSS class to allow variations in design.

    Returns:
        - str: A CSS style block that enables hover-based tooltip visibility.
    """
    tooltip_class = f".{style_prefix}-tooltip" if style_prefix else ".tooltip"

    return f"""
    <style>
        #{element_id}:hover + {tooltip_class} {{
            visibility: visible;
            opacity: 1;
            transform: translateY(0px) scale(1.1);
        }}
    </style>
    """

def install_tooltip_styling(style_prefix="", **design_params):
    """
    Returns a CSS block defining the general appearance of tooltips with an enhanced depth effect.
    
    Args:
        style_prefix (str): A prefix to prepend to the tooltip class for styling multiple tooltip variations.
        **design_params: Dictionary of CSS properties to override default styling.
        
    Returns:
        str: A CSS style block for consistent tooltip styling.
    """
    
    tooltip_class = f".{style_prefix}-tooltip" if style_prefix else ".tooltip"
    
    default_params = {
        "tooltip_visibility": "hidden",
        "tooltip_opacity": "0",
        "tooltip_transform": "translateX(-25%) translateY(5px) scale(0.95)",  # 25% left offset
        "tooltip_transition": "opacity 0.4s ease-out, transform 0.4s ease-out, visibility 0.4s ease-out",
        "tooltip_bg": "rgba(20, 20, 20, 0.75)",  # Darker and slightly more opaque
        "text_color": "#ffffff",  # Bright contrast
        "text_align": "left",
        "padding": "14px",
        "border_radius": "10px",
        "box_shadow": "0px 12px 30px rgba(0, 0, 0, 0.6)",  # Stronger shadow for depth
        "position": "absolute",
        "left": "25%",  # Tooltip starts shifted left
        "top": "110%",  # Tooltip is positioned below the element
        "tooltip_width": "auto",
        "tooltip_max_width": "420px",
        "z_index": "15",
        "border": "1px solid rgba(255, 255, 255, 0.2)",  # Subtle highlight border
        "transform_origin": "top center",
        "bg_blur": "18px",  # Stronger blur effect
        "glow_effect": "0px 0px 8px rgba(255, 255, 255, 0.4)",  # Light glow around text
        "hover_scale": "scale(1.05)",  # Expands slightly when active
        "animation_intensity": "6px"  # More pronounced floating effect
    }
    
    params = {**default_params, **design_params}
    
    return f"""
    <style>
        {tooltip_class} {{
            visibility: {params["tooltip_visibility"]};
            opacity: {params["tooltip_opacity"]};
            transform: {params["tooltip_transform"]};
            transition: {params["tooltip_transition"]};
            background: {params["tooltip_bg"]};
            color: {params["text_color"]};
            text-align: {params["text_align"]};
            padding: {params["padding"]};
            border-radius: {params["border_radius"]};
            box-shadow: {params["box_shadow"]};
            position: {params["position"]};
            left: {params["left"]};
            top: {params["top"]};
            min-width: {params["tooltip_width"]};
            max-width: {params["tooltip_max_width"]};
            z-index: {params["z_index"]};
            border: {params["border"]};
            transform-origin: {params["transform_origin"]};
            overflow: hidden;
            animation: floatEffect 5s ease-in-out infinite;
            text-shadow: {params["glow_effect"]};
        }}

        {tooltip_class}:hover {{
            transform: {params["hover_scale"]};
        }}

        {tooltip_class}::before {{
            content: "";
            position: absolute;
            top: -15px;
            left: -15px;
            width: calc(100% + 30px);
            height: calc(100% + 30px);
            background: inherit;
            filter: blur({params["bg_blur"]});
            z-index: -1;
            border-radius: inherit;
        }}

        @keyframes floatEffect {{
            0% {{ transform: translateX(-25%) translateY({params["animation_intensity"]}); }}
            50% {{ transform: translateX(-25%) translateY(-{params["animation_intensity"]}); }}
            100% {{ transform: translateX(-25%) translateY({params["animation_intensity"]}); }}
        }}
    </style>
    """


def html_for_tooltip_from_large_list(items, label, element_id, style_prefix="", color="#007BFF", emoji=None):
    """
    Generates an HTML tooltip for displaying a large list with a summarized preview.

    Parameters:
        - items (list of str): The list of items to display.
        - label (str): Describes the type of items being enumerated.
        - element_id (str): The ID of the element that will trigger the tooltip.
        - style_prefix (str): Prefix for tooltip CSS class to allow variations in design.
        - color (str): Color for the tooltip text (default: neutral gray #555).
        - emoji (str, optional): Emoji prepended to each listed item.

    Returns:
        - str: HTML snippet containing the summarized text and a tooltip for full details.
    """
    if not items:
        return f'<div style="color:gray;">No {label.lower()} listed</div>'
    
    # Escape and format first item
    first_item = html.escape(items[0])
    summary = f"(and {len(items) - 1} more {label.lower()})" if len(items) > 1 else ""
    visible_text = f'<div style="color:{color}; border-bottom: 1px dashed {color};">{first_item} {summary}</div>'


    
    # Generate full tooltip content
    tooltip_content = "".join(
        f'<div style="color:{color};">{(emoji + " " if emoji else "")}{html.escape(item)}</div>'
        for item in items
    )

    tooltip_class = f"{style_prefix}-tooltip" if style_prefix else "tooltip"

    return f"""
    <div style="position: relative; display: inline-block;">
        <span id="{element_id}" style="border-bottom: 1px dashed gray; cursor: pointer; display: inline-block; transition: color 0.3s ease-in-out;" class="hover-trigger">
            {visible_text}
        </span>
        <div class="{tooltip_class}">
            <strong>All {label} listed:</strong>
            {tooltip_content}
        </div>
    </div>
    """

        
        
