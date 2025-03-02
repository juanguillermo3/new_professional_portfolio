"""
title: Front-End Utils
description: Contains various utilities for design across portfolio sections.
"""

import streamlit as st
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
  
def render_section_separator():
  # 
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("<br>", unsafe_allow_html=True)

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
#
def prettify_title(title):
    """Prettify the title by removing underscores and capitalizing words."""
    return " ".join(word.capitalize() for word in title.replace("_", " ").split())

#
def render_external_link_button_as_train_ticket(url, label, bg_color):
    """Helper method to render an external link button styled like a train ticket."""
    return f"""
    <div style="display: flex; justify-content: center;">
        <a href="{url}" target="_blank" rel="noopener noreferrer"
           style="text-decoration: none;">
            <div style="
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                width: 120px;
                height: 180px;
                background-color: {bg_color};
                color: white;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                border-radius: 10px;
                position: relative;
                transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            " 
            onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 16px rgba(0, 0, 0, 0.3)';"
            onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 4px 8px rgba(0, 0, 0, 0.2)';">
                <div style="
                    padding: 20px 0;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    position: relative;">
                    {label}
                </div>
            </div>
        </a>
    </div>
    """



