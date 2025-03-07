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

def html_for_milestones_from_project_metadata(project_metadata, num_displayed=3 ):
    milestone_html = []

    if 'achieved_milestones' in project_metadata:
        achieved = [f'<div style="color:green;">✅ {m}</div>' for m in project_metadata['achieved_milestones']]
        if len(achieved) > num_displayed:  # Cap initial display to 5
            achieved_preview = achieved[:num_displayed]
            achieved_hidden = achieved[num_displayed:]  # Only hidden milestones go inside <details>
            milestone_html.extend(achieved_preview)
            milestone_html.append(
                f"<details><summary style='cursor: pointer; margin-left:1.5%;'>See all achieved milestones...</summary>{''.join(achieved_hidden)}</details>"
            )
        else:
            milestone_html.extend(achieved)

    if 'next_milestones' in project_metadata:
        next_milestones = [f'<div style="color:#FFB300;">🚧 {m}</div>' for m in project_metadata['next_milestones']]
        if len(next_milestones) > num_displayed:  # Cap initial display to 5
            next_preview = next_milestones[:num_displayed]
            next_hidden = next_milestones[num_displayed:]  # Only hidden milestones go inside <details>
            milestone_html.extend(next_preview)
            milestone_html.append(
                f"<details><summary style='cursor: pointer; margin-left:1.5%;'>See all upcoming milestones...</summary>{''.join(next_hidden)}</details>"
            )
        else:
            milestone_html.extend(next_milestones)

    return ''.join(milestone_html)


import html

def html_for_milestones_from_project_metadata(project_metadata, milestone_type="achieved_milestones"):
    # Define milestone properties
    milestone_config = {
        "achieved_milestones": {"color": "green", "icon": "✅", "label": "Achieved Milestones"},
        "next_milestones": {"color": "#FFB300", "icon": "🚧", "label": "Upcoming Milestones"}
    }
    
    config = milestone_config.get(milestone_type, milestone_config["achieved_milestones"])
    
    # Extract the correct milestone list
    milestones = project_metadata.get(milestone_type, [])

    # Define the tooltip content (full milestone lists with details)
    def format_full_milestone_list(milestones, color, icon, label):
        if not milestones:
            return ""
        safe_milestones = [f'<div style="color:{color};">{icon} {html.escape(m)}</div>' for m in milestones]
        return f"<strong>{label}:</strong>" + "".join(safe_milestones)

    tooltip_content = format_full_milestone_list(milestones, config["color"], config["icon"], config["label"])

    # Precompute summarizing label
    summary_label = f"{len(milestones) - 1} more {config['label'].lower()}" if len(milestones) > 1 else "only milestone"

    # Define the summary text (first milestone with parenthesized summary)
    milestone_summary = (
        f'<span style="color:{config["color"]};">{config["icon"]} {html.escape(milestones[0])} ({summary_label})</span>'
        if milestones else f"No {config['label'].lower()}"
    )

    # Tooltip hoverable component
    return f"""
    <div style="position: relative; display: inline-block;">
        <span style="border-bottom: 1px dashed gray; cursor: pointer;" class="hover-trigger">
            {milestone_summary}
        </span>
        <div class="tooltip">
            {tooltip_content}
        </div>
    </div>
    <style>
        .tooltip {{
            visibility: hidden;
            background-color: white;
            color: black;
            text-align: left;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            position: absolute;
            left: 0;
            top: 120%;
            min-width: 100%;
            max-width: 400px;
            z-index: 1;
            border: 1px solid #ddd;
        }}
        .hover-trigger:hover + .tooltip {{
            visibility: visible;
            width: auto;
            min-width: 100%;
        }}
    </style>
    """









