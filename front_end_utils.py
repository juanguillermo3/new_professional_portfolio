"""
title: Front-End Utils
description: Contains various utilities for design across portfolio sections.
"""

import html
import streamlit as st
import re
import random
from exceptional_ui import apply_custom_tooltip



#
def tags_in_twitter_style(tags, color_palette=None):
    """Generates styled hashtags with a refined navy-themed appearance."""
    if color_palette is None:
        color_palette = [
            "#1B1F3B",  # Deep Navy Blue (Elegant & Professional)
            "#2C3E50",  # Dark Blue-Gray (Subtle & Modern)
            "#34495E",  # Muted Navy (Sophisticated Look)
            "#22303C",  # Dark Steel Blue (Sleek & Low-key)
            "#1E3A8A",  # Bold Royal Blue (Accent Color)
            "#0F172A",  # Almost Black Blue (Sharp & Clean)
            "#3B4B74",  # Classic Navy (Trust & Stability)
            "#102A43",  # Twilight Navy (Calm & Focused)
        ]

    def format_tag(tag):
        """Formats multiword tags: lowercase, capitalize words, remove spaces."""
        cleaned = "".join(word.capitalize() for word in tag.lower().split())
        return f'<span style="color: {random.choice(color_palette)}; font-size: 0.9em; font-weight: 600;">#{cleaned}</span>'

    return " ".join(format_tag(tag) for tag in tags)

#
def render_section_separator():
  # 
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("<br>", unsafe_allow_html=True)


#
def html_for_container(content_html, style_dict):
    """
    Wraps an HTML string inside a <div> with inline styles.

    Parameters:
    - content_html (str): The HTML content to be wrapped.
    - style_dict (dict): A dictionary of CSS properties and values.

    Returns:
    - str: The formatted HTML string wrapped inside a styled <div>.
    """
    # Convert the style dictionary into an inline style string
    style_string = "; ".join(f"{key}: {value}" for key, value in style_dict.items())

    # Return the wrapped HTML
    return f'<div style="{style_string}">{content_html}</div>'

#
def render_external_link_button(url, label, bg_color):
    """Helper method to render an external link button with consistent styling."""
    return f"""
    <div style="display: flex; justify-content: center; margin-top: 5px;">
        <a href="{url}" target="_blank" 
           style="text-decoration: none; width: 200px; display: block; margin: 0 auto;">
            <button style="background-color: {bg_color}; color: white; 
                           border: none; padding: 10px 20px; 
                           text-align: center; text-decoration: none; 
                           font-size: 14px; cursor: pointer; 
                           border-radius: 5px; width: 100%; margin: 0 auto;">
                {label}
            </button>
        </a>
    </div>
    """



def html_for_github_button(github_url: str, button_size: int = 40) -> str:
    """
    Returns an HTML string for a GitHub button with a natural placement.

    Parameters:
        github_url (str): The GitHub repository or profile URL.
        button_size (int, optional): The size of the circular button in pixels (default: 40px).

    Returns:
        str: HTML code for the GitHub button.
    """
    if not github_url:
        return ""

    return f"""
        <style>
        .github-btn {{
            background-color: #333;
            width: {button_size}px;
            height: {button_size}px;
            border-radius: 50%;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            display: inline-flex;
            justify-content: center;
            align-items: center;
            transition: background-color 0.3s ease-in-out;
        }}

        .github-btn img {{
            width: {button_size * 0.6}px;
            height: {button_size * 0.6}px;
        }}

        .github-btn:hover {{
            background-color: #444;
            cursor: pointer;
        }}
        </style>

        <a href="{github_url}" target="_blank" class="github-btn">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub">
        </a>
    """



def html_for_github_button(url):
    """Generates a GitHub button with a floating-like style and hover effect."""
    return f"""
    <div style="display: flex; justify-content: center; margin-top: 5px;">
        <a href="{url}" target="_blank" 
           style="text-decoration: none; display: block; margin: 0 auto;">
            <button style="background-color: #333; color: white; 
                           border: none; padding: 12px; 
                           text-align: center; font-size: 14px; 
                           cursor: pointer; border-radius: 50%; 
                           width: 55px; height: 55px; display: flex; 
                           justify-content: center; align-items: center; 
                           box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
                           transition: transform 0.2s ease, box-shadow 0.2s ease;"
                    onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='4px 4px 15px rgba(0,0,0,0.3)';"
                    onmouseout="this.style.transform='scale(1.0)'; this.style.boxShadow='2px 2px 10px rgba(0,0,0,0.2)';">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" 
                     alt="GitHub" style="width: 32px; height: 32px;">
            </button>
        </a>
    </div>
    """

def html_for_github_button(url):
    """Generates a GitHub button with a floating-like style and hover effect."""
    return f"""
    <div style="display: flex; justify-content: center; margin-top: 5px;">
        <a href="{url}" target="_blank" 
           style="text-decoration: none; display: block; margin: 0 auto;">
            <button style="background-color: #333; color: white; 
                           border: none; padding: 12px; 
                           text-align: center; font-size: 14px; 
                           cursor: pointer; border-radius: 50%; 
                           width: 55px; height: 55px; display: flex; 
                           justify-content: center; align-items: center; 
                           box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
                           transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;"
                    onmouseover="this.style.transform='scale(1.1)'; 
                                 this.style.boxShadow='4px 4px 15px rgba(0,0,0,0.3)'; 
                                 this.style.backgroundColor='#24292E';"
                    onmouseout="this.style.transform='scale(1.0)'; 
                                this.style.boxShadow='2px 2px 10px rgba(0,0,0,0.2)'; 
                                this.style.backgroundColor='#333';">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" 
                     alt="GitHub" style="width: 32px; height: 32px;">
            </button>
        </a>
    </div>
    """

class ButtonFabric:
    """Fabric class to generate styled buttons dynamically."""

    BUTTON_STYLES = {
        "GitHub": {
            "bg_color": "#333",
            "icon": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        },
        "Sheets": {
            "bg_color": "#34A853",
            "icon": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Google_Sheets_logo.svg",
        },
        "Colab Notebook": {
            "bg_color": "#F9AB00",
            "icon": "https://colab.research.google.com/img/colab_favicon_256px.png",
        },
    }

    @staticmethod
    def render_button(label, url):
        """Generates a floating-like button with a hover effect."""
        if label not in ButtonFabric.BUTTON_STYLES:
            return ""  # Skip if button type is unknown
        
        style = ButtonFabric.BUTTON_STYLES[label]

        return f"""
        <a href="{url}" target="_blank" style="text-decoration: none; display: block; margin: 5px;">
            <button style="background-color: {style['bg_color']}; color: white; 
                           border: none; padding: 12px; 
                           text-align: center; font-size: 14px; 
                           cursor: pointer; border-radius: 50%; 
                           width: 55px; height: 55px; display: flex; 
                           justify-content: center; align-items: center; 
                           box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
                           transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;"
                    onmouseover="this.style.transform='scale(1.1)'; 
                                 this.style.boxShadow='4px 4px 15px rgba(0,0,0,0.3)';"
                    onmouseout="this.style.transform='scale(1.0)'; 
                                this.style.boxShadow='2px 2px 10px rgba(0,0,0,0.2)';">
                <img src="{style['icon']}" alt="{label}" style="width: 32px; height: 32px;">
            </button>
        </a>
        """

    @staticmethod
    def render_buttons_grid(button_data, max_per_row=3):
        """
        Generates a responsive grid layout for buttons.
        - button_data: List of (label, url) tuples
        - max_per_row: Max buttons per row before wrapping
        """
        if not button_data:
            return ""

        rows = []
        row = []

        for index, (label, url) in enumerate(button_data):
            button_html = ButtonFabric.render_button(label, url)
            if button_html:
                row.append(button_html)

            # If row is full, add to rows and reset
            if len(row) == max_per_row or index == len(button_data) - 1:
                rows.append(f'<div style="display: flex; justify-content: center;">' + "".join(row) + "</div>")
                row = []

        return "\n".join(rows)+"\n"

def prettify_title(title, cleanup_regex=r"[^a-zA-Z0-9]+"):
    """
    Prettify the title by removing undesired characters using a regex,
    splitting into words, and capitalizing them.

    Parameters:
    - title (str): The input title string.
    - cleanup_regex (str): A regex pattern to replace undesired characters. Defaults to non-alphanumerics.

    Returns:
    - str: Prettified title.
    """
    clean_title = re.sub(cleanup_regex, " ", title)
    return " ".join(word.capitalize() for word in clean_title.split())


