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

def html_for_item_data(
    rec,
    badge_rules=None,
    background_color="#f4f4f4",
    border_style="1px solid #ddd",
    card_height="150px",
    overflow_style="overflow-y: auto;"
):
    """
    Generate an HTML snippet for a recommended item card dynamically.

    Parameters:
    - rec (dict): Dictionary containing item metadata.

    Returns:
    - str: A formatted HTML string representing the item card.
    """
    
    # Apply the badge system with default rules inside apply_badges_to_item_title
    title = apply_badges_to_item_title(rec, badge_rules)

    # Default description if missing
    description = html.escape(rec.get('description', 'No description available.'))  # Escape for safety

    # Return the HTML structure
    return f"""
        <div style="background-color: {background_color}; border: {border_style}; 
                    border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                    padding: 10px; height: {card_height}; {overflow_style}; 
                    display: flex; flex-direction: column; justify-content: space-between;">
            <div style="background-color: rgba(255, 255, 255, 0.7); 
                        padding: 5px 10px; border-radius: 10px 10px 0 0; 
                        font-size: 16px; font-weight: bold; text-align: center;">
                {title}
            </div>
            <div style="flex-grow: 1; padding: 10px; overflow-y: auto; text-align: justify;">
                {description}
            </div>
        </div>
    """

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
    # Define milestone properties
    milestone_labels = {
        "achieved_milestones": ("Achieved Milestones", "green", "✅"),
        "next_milestones": ("Upcoming Milestones", "#FFB300", "🚧")
    }
    
    label, color, icon = milestone_labels.get(milestone_type, ("Milestones", "black", "📌"))
    milestones = project_metadata.get(milestone_type, [])

    # Handle empty milestone case
    if not milestones:
        return f'<div style="color:gray;">No {label.lower()}</div>'

    # Format milestone summary (first milestone + count)
    first_milestone = html.escape(milestones[0])
    summary = f"({len(milestones) - 1} more)" if len(milestones) > 1 else ""
    visible_milestone = f'{icon} {first_milestone} {summary}'

    # Tooltip content (full milestone list)
    tooltip_content = "".join(
        f'<div style="color:{color};">{icon} {html.escape(m)}</div>' for m in milestones
    )

    # Unique ID for the tooltip
    element_id = f"tooltip-{milestone_type}"

    # Return formatted HTML with improved tooltip behavior
    return f"""
    <div style="position: relative; display: inline-block;">
        <div id="{element_id}" class="hover-trigger" style="border-bottom: 1px dashed gray; cursor: pointer;">
            {visible_milestone}
            <div class="tooltip">
                <strong>{label}:</strong>
                {tooltip_content}
            </div>
        </div>
    </div>
    <style>
        .tooltip {{
            visibility: hidden;
            opacity: 0;
            transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out, transform 0.3s ease-in-out;
            background-color: white;
            color: black;
            text-align: left;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
            position: absolute;
            left: 50%;
            top: 100%;
            min-width: 150px;
            max-width: 400px;
            z-index: 999;
            border: 1px solid #ddd;
            transform: translateX(-50%) translateY(5px) scale(0.95);
            transform-origin: top center;
        }}

        .hover-trigger:hover .tooltip {{
            visibility: visible;
            opacity: 1;
            transform: translateX(-50%) translateY(0px) scale(1);
        }}
    </style>
    """














