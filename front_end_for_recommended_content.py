"""
title: Front-End for Recommended Data
description: Implements the front-end representation of items displayed by the RecSys. It aims to create elegant and informative components by combining Streamlit built-ins with custom styling.
"""

import hashlib
import streamlit as st
from front_end_utils import prettify_title
import re
import hashlib
from html import escape
from exceptional_ui import _custom_tooltip_html

import re
import html

def prettify_title(title):
    """Helper function to format titles properly."""
    return html.escape(title.title())  # Escape HTML for safety and capitalize words

def apply_badges_to_item_title(metadata, outstanding_content_regex):
    """
    Applies the outstanding content badge (⭐) to the title based on metadata conditions.

    Parameters:
    - metadata (dict): Dictionary containing item metadata.
    - outstanding_content_regex (re.Pattern): Regex pattern to detect outstanding content keys.

    Returns:
    - str: Title string with appropriate badges prepended.
    """
    # Check if any key matches the regex AND has a truthy value
    is_outstanding = any(outstanding_content_regex.search(key) and metadata.get(key) for key in metadata)

    # Get the title and format it
    title = prettify_title(metadata.get('title', 'Untitled'))

    # Prepend badge if outstanding content is detected
    return f"⭐ {title}" if is_outstanding else title

def html_for_item_data(
    rec,
    outstanding_content_regex=re.compile(r"^(galleria|highlighted_content|image_path)$", re.IGNORECASE),
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
    
    # Apply the badge system for outstanding content
    title = apply_badges_to_item_title(rec, outstanding_content_regex)

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




