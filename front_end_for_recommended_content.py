"""
title: Front-End for Recommended Data
description: Implements the front-end representation of items displayed by the RecSys. It aims to create elegant and informative components by combining Streamlit built-ins with custom styling.
"""

import hashlib
import html
import re
import time

import streamlit as st
from badges_for_item_data import apply_badges_to_item_title
from exceptional_ui import _custom_tooltip_html
from media_carrousel import flexible_file_discovery, html_for_media_carousel, dummy_media_list
from tooltip_canvas import TooltipCanvas
from front_end_utils import prettify_title, render_external_link_button,  html_for_container,html_for_github_button, ButtonFabric

# Instantiate the tooltip system
tooltip_system = TooltipCanvas()
button_fabric=ButtonFabric()


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

def html_for_item_data(
    rec,
    badge_rules=None,
    background_color="#f4f4f4",
    border_style="1px solid #ddd",
    card_height="150px",
    post_fix="_card",
    search_dir="assets"  # Default search directory for media files
):
    """
    Generate an HTML snippet for a recommended item card dynamically.

    Parameters:
    - rec (dict): Dictionary containing item metadata.
    - badge_rules (dict, optional): Rules for applying badges to the item title.
    - background_color (str, optional): Background color of the card.
    - border_style (str, optional): CSS border style.
    - card_height (str, optional): Height of the card.
    - post_fix (str, optional): Suffix for card ID.
    - search_dir (str, optional): Base directory for media file discovery.

    Returns:
    - tuple: (card_html, styles_html)
    """

    # Define the styles for the title
    title_style = {
        "font-weight": "bold",
        "text-align": "center"
    }

    # Define specific styles for the description tooltip
    description_style = {
        "text-align": "justify",
    }

    frosted_glass_style = {
        "background": "rgba(255, 255, 255, 0)",  # Fully transparent by default
        "backdrop-filter": "blur(4px)",  
        "border": "2px solid rgba(255, 255, 255, 0.9)",  
        "box-shadow": "0px 4px 20px rgba(255, 255, 255, 0.1)",  
        #"transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out, transform 0.3s ease-in-out",  
    }
    
    modern_dashboard_style = {
        **frosted_glass_style,  # Inherit frosted glass effect
        "background": "rgba(23, 33, 43, 0.4)",  # Override transparency with a dark tint
        "padding": "10px 5%",  
        "width": "100%",  
        "z-index": "9999",  
        "margin": "5px",  
        "font-weight": "normal",  
        "color": "#ffffff",  
        "border-radius": "8px",  
    }
    
    # Unique ID based on timestamp hash
    card_id = f"card_{hash(time.time())}"

    # Apply the badge system
    title = apply_badges_to_item_title(rec, badge_rules)
    
    # Wrap the title using the new function
    raw_title = html_for_container(f'<div class="item-tooltip title-tooltip">{title}</div>', title_style)

    # Escape description to prevent HTML injection
    description = (
        f'<div class="item-tooltip description-tooltip" style="text-align: justify; margin: 0 5%;">'
        f'{html.escape(rec.get("description", "No description available."))}'
        f'</div>'
    )

    # Merge modern_dashboard_style with title_style and set width to 300px
    tooltip_title = html_for_container(
        f'<div class="item-tooltip title-tooltip">{apply_badges_to_item_title(rec, badge_rules)}</div>',
        {**modern_dashboard_style, **title_style, "width": "300px"}
    )
    
    # Merge modern_dashboard_style with description_style and set width to 300px
    tooltip_description = html_for_container(
        f'<div class="item-tooltip description-tooltip">{html.escape(rec.get("description", "No description available."))}</div>',
        {**modern_dashboard_style, **description_style, "width": "300px"}
    )

    # Generate buttons for the tooltip
    buttons_html = []

    #
    # (1)
    #
    if "url" in rec and rec["url"]:
        buttons_html.append(html_for_github_button(rec["url"]))
    #
    # (2)
    #
    if False in rec and rec["report_url"]:
        buttons_html.append(
            f'<a href="{rec["report_url"]}" target="_blank" '
            f'style="display: block; margin: 5px 0; padding: 5px 10px; '
            f'background-color: #34A853; color: white; border-radius: 5px; '
            f'text-decoration: none;" class="item-tooltip button-tooltip">'
            f'Sheets</a>'
        )
    #
    # (3)
    #
    if False in rec and rec["colab_url"]:
        buttons_html.append(
            f'<a href="{rec["colab_url"]}" target="_blank" '
            f'style="display: block; margin: 5px 0; padding: 5px 10px; '
            f'background-color: #F9AB00; color: white; border-radius: 5px; '
            f'text-decoration: none;" class="item-tooltip button-tooltip">'
            f'Colab Notebook</a>'
        )

    buttons_html="\n".join(buttons_html)

    #
    # (1)
    #
    tooltip_content = [
        [
            tooltip_title,
            tooltip_description
        ]
    ]
    #
    # (2)
    #
    if buttons_html:
        tooltip_content=[
            tooltip_content[0]+
            [
            #'<div class="item-tooltip resources-tooltip">Resources:</div>', 
            #f'<div class="item-tooltip buttons-tooltip">{buttons_html}</div>'
            ]
        ]

    # If the card metadata includes an image path, discover media files
    if "image_path" in rec:
        discovered_media = flexible_file_discovery(rec["image_path"], search_dir=search_dir)
        if discovered_media:
            media_items = [{"src": path, "alt": f"Media {i+1}"} for i, path in enumerate(discovered_media)]
            media_carousel = html_for_media_carousel(media_items)
            tooltip_content.append([
                html_for_container(
                    f'<div class="item-tooltip media-carousel-tooltip">{media_carousel}</div>',
                    {"max-width": "800px"}
                )
            ])

    # Generate tooltip
    tooltip_html, tooltip_styles = tooltip_system.html_to_apply_tooltip(
        element_id=card_id,
        content=tooltip_content,
        visible_text="See more"
    )


    button_size=40
    card_html = f"""
    <style>
        .recommendation-card {{
            background-color: {background_color};
            border: {border_style};
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            height: {card_height};
            width: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 10px;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin: 10px;
            position: relative;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }}
    
        .recommendation-card:hover {{
            transform: scale(1.2);
            box-shadow: 0px 12px 24px rgba(0, 0, 0, 0.3);
            z-index: 20;
        }}
    
        .recommendation-title {{
            background-color: rgba(255, 255, 255, 0.7);
            padding: 5px 10px;
            border-radius: 10px;
            width: auto;
            max-width: 100%;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
    
        .github-btn, .colab-btn {{
            background-color: white;
            width: {button_size}px;
            height: {button_size}px;
            border-radius: 50%;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            justify-content: center;
            align-items: center;
            transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
            opacity: 0;
            transform: scale(0.8);
            display: none;
            margin-top: 5px;
        }}
    
        .github-btn img, .colab-btn img {{
            width: {button_size * 0.6}px;
            height: {button_size * 0.6}px;
        }}
    
        .recommendation-card:hover .github-btn,
        .recommendation-card:hover .colab-btn {{
            display: flex;
            opacity: 1;
            transform: scale(1);
        }}
    
        .github-btn:hover {{
            background-color: #f5f5f5;
            cursor: pointer;
        }}
    
        .colab-btn {{
            background-color: #f9ab00;
        }}
    
        .colab-btn:hover {{
            background-color: #e69900;
            cursor: pointer;
        }}
    </style>
    
    <div id="{card_id}" class="recommendation-card">
        <div class="recommendation-title">
            {raw_title}
        </div>  
        <div>
            <a href="{rec["url"] if "url" in rec else ""}" target="_blank" class="github-btn">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub">
            </a>
        </div>
        {f'<div><a href="{rec["colab_url"]}" target="_blank" class="colab-btn"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Google_Colaboratory_SVG_Logo.svg/512px-Google_Colaboratory_SVG_Logo.svg.png" alt="Colab"></a></div>' if "colab_url" in rec else ''}
    </div>
    """

    return card_html, tooltip_html, tooltip_styles


def html_for_milestones_from_project_metadata(milestones=None, project_metadata=None, milestone_type="achieved_milestones"):
    """
    Generates an HTML snippet for displaying milestones with a tooltip, including micro-interactions.
    """
    import html  # For escaping milestone text
    
    milestone_labels = {
        "achieved_milestones": {"label": "Achieved Milestones", "color": "#2E7D32", "pastel": "#A5D6A7", "icon": "https://img.icons8.com/?size=100&id=gbhGcQX6NZvT&format=png"},
        "next_milestones": {"label": "Upcoming Milestones", "color": "#C28F00", "pastel": "#FFECB3", "icon": "https://img.icons8.com/?size=100&id=46910&format=png"},
        "code_samples": {"label": "Code Samples", "color": "#1565C0", "pastel": "#BBDEFB", "icon": "https://img.icons8.com/?size=100&id=ZSyCgjqn5i8Y&format=png"}
    }

    milestone = milestone_labels.get(milestone_type, {"label": "Milestones", "color": "black", "pastel": "#E0E0E0", "icon": "https://icons8.com/icon/gbhGcQX6NZvT/milestones"})
    label, color, pastel, icon_url = milestone["label"], milestone["color"], milestone["pastel"], milestone["icon"]

    if milestones is None:
        milestones = project_metadata.get(milestone_type, []) if project_metadata else []

    milestone_count = len(milestones)
    summary = f"{milestone_count} {label.lower()}"

    tooltip_content = "".join(
        f'<div style="color:{color};">💡 {html.escape(m)}</div>' for m in milestones
    )
    
    element_id = f"tooltip-{milestone_type}"

    return f"""
    <div style="position: relative; display: inline-block; cursor: pointer;">
        <span id="{element_id}" style="border-bottom: 1px dashed gray; cursor: pointer;">
            <div style="color:{color}; text-align: center;">
                <img src="{icon_url}" alt="{label}" style="width: 30px; height: 30px;"/><br>
                <label>{summary}</label>
            </div>
        </span>
        <div id="{element_id}-tooltip" style="
            visibility: hidden; opacity: 0; transform: translateY(5px) scale(0.95);
            transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out, transform 0.3s ease-in-out;
            background-color: {pastel}; color: black; text-align: left;
            padding: 10px; border-radius: 5px; box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            position: absolute; left: 50%; transform: translateX(-50%) translateY(10px);
            min-width: 300px; max-width: 400px; z-index: 1; border: 1px solid rgba(200, 200, 200, 0.5);
            transform-origin: top center;">
            <strong>{label}:</strong>
            {tooltip_content}
        </div>
    </div>
    <script>
        document.getElementById('{element_id}').addEventListener('mouseenter', function() {{
            var tooltip = document.getElementById('{element_id}-tooltip');
            tooltip.style.visibility = 'visible';
            tooltip.style.opacity = '1';
            tooltip.style.transform = 'translateX(-50%) translateY(0px) scale(1.1)';
        }});
        document.getElementById('{element_id}').addEventListener('mouseleave', function() {{
            var tooltip = document.getElementById('{element_id}-tooltip');
            tooltip.style.visibility = 'hidden';
            tooltip.style.opacity = '0';
            tooltip.style.transform = 'translateX(-50%) translateY(10px) scale(0.95)';
        }});
    </script>
    """




