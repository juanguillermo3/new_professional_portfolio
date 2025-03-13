"""
title: Front-End for Recommended Data
description: Implements the front-end representation of items displayed by the RecSys. It aims to create elegant and informative components by combining Streamlit built-ins with custom styling.
"""

import hashlib
import streamlit as st
from front_end_utils import prettify_title
import re
import hashlib
import html
from html import escape
from exceptional_ui import _custom_tooltip_html
from badges_for_item_data import apply_badges_to_item_title
from biotech_lab import frost_glass_mosaic, _custom_tooltip_with_frost_glass_html, frost_glass_mosaic
import time
import html


def id_from_item_data(rec, fields=["title", "description"]):
    """
    Generate a unique ID for an item based on specified fields.

    Parameters:
    - rec (dict): Dictionary containing item metadata.
    - fields (list): List of field names to be used for generating the ID.

    Returns:
    - str: A unique hashed ID for the item.

    Raises:
    - KeyError: If any required field is missing from `rec`.
    """
    missing_fields = [field for field in fields if field not in rec]
    if missing_fields:
        raise KeyError(f"Missing required fields: {', '.join(missing_fields)}")
    
    unique_string = "".join(str(rec[field]) for field in fields)
    unique_hash = hashlib.md5(unique_string.encode()).hexdigest()
    
    return unique_hash

import html

def html_for_milestones_from_project_metadata(project_metadata, milestone_type="achieved_milestones"):
    """
    Generates an HTML snippet for displaying milestones with a tooltip.
    
    Parameters:
        - project_metadata (dict): Contains milestone information.
        - milestone_type (str): The type of milestone to display ('achieved_milestones' or 'next_milestones').

    Returns:
        - str: HTML snippet containing the milestone and tooltip.
    """
    # Define milestone properties with optimized contrast
    milestone_labels = {
        "achieved_milestones": ("Achieved Milestones", "#2E7D32", "✅"),  # Dark green
        "next_milestones": ("Upcoming Milestones", "#C28F00", "🚧"),  # Gold-ish yellow
    }
    
    label, color, icon = milestone_labels.get(milestone_type, ("Milestones", "black", "📌"))
    milestones = project_metadata.get(milestone_type, [])

    # Handle empty milestone case
    if not milestones:
        return f'<div style="color:gray;">No {label.lower()}</div>'

    # Format milestone summary (first milestone + count)
    first_milestone = html.escape(milestones[0])
    summary = f"({len(milestones) - 1} more)" if len(milestones) > 1 else ""
    visible_milestone = f'<div style="color:{color};">{icon} {first_milestone} {summary}</div>'

    # Tooltip content (full milestone list)
    tooltip_content = "".join(
        f'<div style="color:{color};">{icon} {html.escape(m)}</div>' for m in milestones
    )

    # Unique ID for the tooltip
    element_id = f"tooltip-{milestone_type}"

    # Return formatted HTML with refined frosted effect
    return f"""
    <div style="position: relative; display: inline-block;">
        <span id="{element_id}" style="border-bottom: 1px dashed gray; cursor: pointer;" class="hover-trigger">
            {visible_milestone}
        </span>
        <div class="tooltip">
            <strong>{label}:</strong>
            {tooltip_content}
        </div>
    </div>
    <style>
        .tooltip {{
            visibility: hidden;
            opacity: 0;
            transform: translateY(5px) scale(0.95);
            transition: 
                opacity 0.3s ease-in-out, 
                visibility 0.3s ease-in-out, 
                transform 0.3s ease-in-out;
            background-color: rgba(240, 240, 240, 0.7); /* Softer frosted effect */
            backdrop-filter: blur(1px); /* Stronger blur for a glassy look */
            color: black;
            text-align: left;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            position: absolute;
            left: 75%;
            top: 120%;
            min-width: 100%;
            max-width: 400px;
            z-index: 1;
            border: 1px solid rgba(200, 200, 200, 0.5); /* Softer border */
            transform-origin: top center;
        }}

        #{element_id}:hover + .tooltip {{
            visibility: visible;
            opacity: 1;
            transform: translateY(0px) scale(1.1);
        }}
    </style>
    """


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

    visible_text = f'<span id="trigger-{unique_id}" class="tooltip-trigger">{first_item} {summary}</span>'

    tooltip_content = "".join(
        f'<div class="tooltip-item">{(emoji + " " if emoji else "")}{html.escape(item)}</div>'
        for item in items
    )

    tooltip_html = f"""
        <div style="position: relative; display: inline-block;">
            {visible_text}
            <div id="tooltip-{unique_id}" class="skills_tooltip">
                <strong>All {label} listed:</strong>
                {tooltip_content}
            </div>
        </div>
    """

    return tooltip_html, unique_id

def setup_tooltip_behavior(unique_id):
    """
    Injects the required CSS and behavior into Streamlit to activate the tooltip.
    """
    import time
    if not unique_id:
        return ""

    timestamp = int(time.time())  # Forces Streamlit to refresh styles

    tooltip_css = f"""
    <style>
        /* Timestamp {timestamp} to force refresh */
        .tooltip-trigger {{
            color: #007BFF;
            border-bottom: 1px dashed #007BFF;
            cursor: pointer;
            position: relative;
        }}

        #tooltip-{unique_id} {{
            visibility: hidden;
            opacity: 0;
            width: 400px;
            background: rgba(20, 20, 20, 0.9);
            color: white;
            padding: 12px;
            border-radius: 8px;
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.5);
            position: absolute;
            left: 50%;
            top: 100%;  /* Start just below trigger */
            text-align: left;
            z-index: 10;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transform: translateX(-50%) translateY(-5px);
            transition: 
                opacity 0.3s ease-in-out, 
                visibility 0.3s ease-in-out, 
                transform 0.3s ease-in-out;
            overflow-wrap: break-word;
        }}

        /* Floating animation */
        @keyframes floatTooltip {{
            0% {{ transform: translateX(-50%) translateY(0px); }}
            100% {{ transform: translateX(-50%) translateY(5px); }}
        }}

        #trigger-{unique_id}:hover + #tooltip-{unique_id},
        #tooltip-{unique_id}:hover {{
            visibility: visible;
            opacity: 1;
            transform: translateX(-50%) translateY(0px);
            animation: floatTooltip 2s infinite alternate ease-in-out;
        }}

        .tooltip-item {{
            color: #007BFF;
            margin-bottom: 4px;
        }}
    </style>
    """
    return tooltip_css










