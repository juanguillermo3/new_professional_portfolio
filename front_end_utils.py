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
    """Render an external link button styled like a train ticket with a hover effect."""
    return f"""
    <div style="display: flex; justify-content: center; margin: 0;">
        <a href="{url}" target="_blank" rel="noopener noreferrer"
           style="text-decoration: none;">
            <div style="
                width: 60px;
                height: 120px;
                background-color: {bg_color};
                border-radius: 12px;
                position: relative;
                transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            " 
            onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 6px 12px rgba(0, 0, 0, 0.3)';"
            onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 2px 6px rgba(0, 0, 0, 0.2)';">
                
                <!-- Top cut-out -->
                <div style="
                    position: absolute;
                    top: -6px;
                    left: 50%;
                    width: 20px;
                    height: 12px;
                    background-color: white;
                    border-radius: 50%;
                    transform: translateX(-50%);
                    box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
                "></div>
                
                <!-- Middle dashed line -->
                <div style="
                    width: 80%;
                    height: 1px;
                    background: repeating-linear-gradient(
                        to right, 
                        white, white 3px, transparent 3px, transparent 6px
                    );
                    position: absolute;
                    top: 50%;
                    transform: translateY(-50%);
                "></div>
                
                <!-- Bottom cut-out -->
                <div style="
                    position: absolute;
                    bottom: -6px;
                    left: 50%;
                    width: 20px;
                    height: 12px;
                    background-color: white;
                    border-radius: 50%;
                    transform: translateX(-50%);
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                "></div>
            </div>
        </a>
    </div>
    """


def html_for_paragraph_with_expandable_details(visible_text, details_text, summary_label=" See more"):
    """
    Returns HTML for an inline expandable paragraph section where the "See more" label 
    always appears at the end of the full text (visible + hidden content).
    
    :param visible_text: The portion of text that remains visible.
    :param details_text: The portion hidden inside the expandable section.
    :param summary_label: The text for the clickable "See more" button.
    :return: HTML string for an inline expandable section.
    """
    full_text = f"{visible_text} {details_text}" if details_text else visible_text

    return f"""
    <p style="display: inline;">
        {full_text}
        <details style="display: inline;">
            <summary style="display: inline; cursor: pointer; color: #0073e6; 
                           text-decoration: underline; margin: 0; padding: 0; white-space: nowrap;">
                {summary_label}
            </summary>
        </details>
    </p>
    """

def html_for_paragraph_with_expandable_details(visible_text, details_text, summary_label=" See more"):
    """
    Returns HTML for an inline expandable paragraph section where the "See more" label 
    always appears at the end of the full text (visible + hidden content), and expands on click.

    :param visible_text: The portion of text that remains visible.
    :param details_text: The portion hidden inside the expandable section.
    :param summary_label: The text for the clickable "See more" button.
    :return: HTML string for an inline expandable section.
    """
    if not details_text:  # If no hidden content, return only the visible text
        return f"<p>{visible_text}</p>"

    return f"""
    <p style="display: inline;">
        {visible_text}
        <details style="display: inline;">
            <summary style="display: inline; cursor: pointer; color: #0073e6; 
                           text-decoration: underline; margin: 0; padding: 0; white-space: nowrap;">
                {summary_label}
            </summary>
            <span style="display: inline;"> {details_text} </span>
        </details>
    </p>
    """













