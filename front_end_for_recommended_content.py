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

# File-type to icon mapping (URL-based or local file paths)
FILE_TYPE_ICONS = {
    ".r": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/R_logo.svg/50px-R_logo.svg.png",
    ".py": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/50px-Python-logo-notext.svg.png",
    ".ipynb": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/50px-Jupyter_logo.svg.png",
    ".csv": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/CSV_Icon.svg/50px-CSV_Icon.svg.png",
}

def apply_badges_to_item_title(metadata, badge_rules=None):
    """
    Applies multiple badges (emoji + file icons) to the title based on metadata.

    Parameters:
    - metadata (dict): Dictionary containing item metadata.
    - badge_rules (list of tuples, optional): Each tuple contains:
        (regex (str), emoji (str), keys (list of str))
        - regex: Regex pattern to match values in metadata.
        - emoji: Emoji badge to prepend when condition is met.
        - keys: List of metadata keys to check.

    Returns:
    - str: Title string with appropriate badges (including HTML img for file icons).
    """
    if badge_rules is None:
        badge_rules = [
            (".*", "⭐", ["galleria", "highlighted_content", "image_path"]),  # Outstanding content
        ]

    title = prettify_title(metadata.get('title', 'Untitled'))
    badges = []

    # Process emoji-based badges
    for regex, emoji, keys in badge_rules:
        if any(key in metadata and re.search(regex, str(metadata[key])) for key in keys):
            badges.append(emoji)

    # Process file-type badges (icons)
    file_type = metadata.get("file_type", "").lower()
    if file_type in FILE_TYPE_ICONS:
        icon_url = FILE_TYPE_ICONS[file_type]
        file_icon = f'<img src="{icon_url}" style="width: 16px; height: 16px; vertical-align: middle;">'
        badges.append(file_icon)

    # Generate the final decorated title
    return f"{' '.join(badges)} {title}" if badges else title

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




