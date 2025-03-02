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
    - rec (dict): A dictionary containing item metadata with the following fields:
        - "title" (str, optional): The title of the recommended item. Defaults to "Untitled".
        - "description" (str, optional): A short descriptive text for the item. Defaults to "No description available."
        - "galleria" (bool, optional, legacy): Marks outstanding content (deprecated).
        - "highlighted_content" (bool, optional, preferred): Marks outstanding content.

    - outstanding_content_regex (re.Pattern): A regex pattern to detect keys marking outstanding content.
    - background_color (str): Background color of the card.
    - border_style (str): CSS style for the border.
    - card_height (str): Height of the card.
    - overflow_style (str): CSS for overflow handling.

    Returns:
    - str: A formatted HTML string representing the item card.
    """
    
    # Check for outstanding content using the provided regex
    is_outstanding = any(outstanding_content_regex.match(key) and rec.get(key) for key in rec)

    # Apply title transformation with a default value
    title = prettify_title(rec.get('title', 'Untitled'))
    if is_outstanding:
        title = f"⭐ {title}"  # Highlight special items
    
    # Default description if missing
    description = rec.get('description', 'No description available.')

    # Return the HTML structure
    return f"""
        <div style="background-color: {background_color}; border: {border_style}; 
                    border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                    padding: 10px; text-align: center; height: {card_height}; {overflow_style}; 
                    position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; 
                        background-color: rgba(255, 255, 255, 0.7); 
                        padding: 5px 10px; border-radius: 10px 10px 0 0; 
                        font-size: 16px; font-weight: bold; z-index: 10;">
                {title}
            </div>
            <div style="margin-top: 40px; padding: 0 10px; overflow-y: auto; 
                        height: calc(100% - 40px); text-align: justify;">
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




