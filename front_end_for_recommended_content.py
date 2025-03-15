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
import time
import html

from exceptional_ui import _custom_tooltip_html
from badges_for_item_data import apply_badges_to_item_title
from tooltip_canvas import TooltipCanvas

# Instantiate the tooltip system
tooltip_system = TooltipCanvas()


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


def html_for_milestones_from_project_metadata(milestones=None, project_metadata=None, milestone_type="achieved_milestones"):
    """
    Generates an HTML snippet for displaying milestones with a tooltip.

    Parameters:
        - milestones (list, optional): An explicit list of milestones to display.
        - project_metadata (dict, optional): Contains milestone information (used if milestones is not provided).
        - milestone_type (str): The type of milestone to display ('achieved_milestones', 'next_milestones', or 'code_samples').

    Returns:
        - str: HTML snippet containing the milestone and tooltip.
    """
    # Define milestone properties with optimized contrast
    milestone_labels = {
        "achieved_milestones": ("Achieved Milestones", "#2E7D32", "✅"),  # Dark green
        "next_milestones": ("Upcoming Milestones", "#C28F00", "🚧"),  # Gold-ish yellow
        "code_samples": ("Code Samples", "#1565C0", "💾")  # Deep blue for code-related milestones
    }
    
    label, color, icon = milestone_labels.get(milestone_type, ("Milestones", "black", "📌"))
    
    # Use explicitly provided milestones or fall back to project_metadata
    if milestones is None:
        milestones = project_metadata.get(milestone_type, []) if project_metadata else []

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



import time
import html

def html_for_item_data(
    rec,
    badge_rules=None,
    background_color="#f4f4f4",
    border_style="1px solid #ddd",
    card_height="150px",
    post_fix="_card"
):
    """
    Generate an HTML snippet for a recommended item card dynamically.

    Parameters:
    - rec (dict): Dictionary containing item metadata.

    Returns:
    - tuple: (card_html, styles_html)
    """

    # Unique ID based on timestamp hash
    card_id = f"card_{hash(time.time())}"

    # Apply the badge system
    title = apply_badges_to_item_title(rec, badge_rules)

    # Escape description to prevent HTML injection
    description = html.escape(rec.get("description", "No description available."))

    # Generate tooltip
    tooltip_html, tooltip_styles = tooltip_system.html_to_apply_tooltip(
        element_id=card_id,
        content=[[title, description]],
        visible_text="See more"
    )

    # Card HTML with tooltip embedded at the bottom center
    card_html = f"""
        <div id="{card_id}" style="background-color: {background_color}; border: {border_style}; 
                    border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                    height: {card_height}; width: 200px;
                    display: flex; flex-direction: column; align-items: center; 
                    justify-content: center; padding: 10px; text-align: center; 
                    font-size: 16px; font-weight: bold; cursor: pointer; margin: 10px; 
                    position: relative;">
            <div style="background-color: rgba(255, 255, 255, 0.7); 
                        padding: 5px 10px; border-radius: 10px; width: auto; max-width: 100%;">
                {title}
            </div>
            
            {tooltip_html}

        </div>
    """

    # Return card HTML and styles
    return card_html, tooltip_styles



    










