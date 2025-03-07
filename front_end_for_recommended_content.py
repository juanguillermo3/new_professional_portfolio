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

import html

def html_for_milestones_tooltip(project_metadata):
    # Extract milestone lists safely
    achieved_milestones = project_metadata.get("achieved_milestones", [])
    pending_milestones = project_metadata.get("next_milestones", [])

    # Function to format both visible and hidden milestone elements
    def format_milestone(milestone, color, icon):
        return f'<div style="color:{color};">{icon} {html.escape(milestone)}</div>'

    # Function to generate the tooltip content
    def format_tooltip(milestones, color, icon, label):
        if not milestones:
            return ""
        formatted_milestones = "".join(format_milestone(m, color, icon) for m in milestones)
        return f"<strong>{label}:</strong> {formatted_milestones}"

    # Handle Achieved Milestones
    if achieved_milestones:
        first_achieved = format_milestone(achieved_milestones[0], "green", "✅")
        achieved_label = f'and a {len(achieved_milestones) - 1} more achieved milestones' if len(achieved_milestones) > 1 else ""
        achieved_tooltip = format_tooltip(achieved_milestones, "green", "✅", "Achieved Milestones")
    else:
        first_achieved = "No achieved milestones"
        achieved_label = ""
        achieved_tooltip = ""

    # Handle Pending Milestones
    if pending_milestones:
        first_pending = format_milestone(pending_milestones[0], "#FFB300", "🚧")
        pending_label = f'and a {len(pending_milestones) - 1} more pending milestones' if len(pending_milestones) > 1 else ""
        pending_tooltip = format_tooltip(pending_milestones, "#FFB300", "🚧", "Upcoming Milestones")
    else:
        first_pending = "No pending milestones"
        pending_label = ""
        pending_tooltip = ""

    return f"""
    <div style="display: flex; gap: 15px; align-items: center;">
        <!-- Achieved Milestones Section -->
        <div style="position: relative; display: inline-block;">
            <span class="hover-trigger">{first_achieved} {achieved_label}</span>
            <div class="tooltip">{achieved_tooltip}</div>
        </div>

        <!-- Pending Milestones Section -->
        <div style="position: relative; display: inline-block;">
            <span class="hover-trigger">{first_pending} {pending_label}</span>
            <div class="tooltip">{pending_tooltip}</div>
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
            max-width: 300px;
            z-index: 1;
            border: 1px solid #ddd;
        }}
        .hover-trigger {{
            border-bottom: 1px dashed gray;
            cursor: pointer;
            display: inline-block;
        }}
        .hover-trigger:hover + .tooltip {{
            visibility: visible;
        }}
    </style>
    """




