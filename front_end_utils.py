import streamlit as st
import random

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

def tags_in_twitter_style(tags, color_palette=None):
    """Generates styled hashtags with a Twitter-like appearance."""
    if color_palette is None:
        color_palette = [
            "#1E3A8A",  # Deep Blue (Tech/Professional)
            "#065F46",  # Dark Green (Trust/Innovation)
            "#9333EA",  # Purple (Creative/Modern)
            "#0EA5E9",  # Cyan Blue (Fresh/Innovative)
            "#B91C1C",  # Deep Red (Bold/Strong)
            "#7C3AED",  # Vibrant Indigo (Techy Feel)
            "#2563EB",  # Solid Blue (Corporate/Stable)
            "#059669",  # Teal Green (Sophisticated)
        ]
    
    return " ".join(
        f'<span style="color: {random.choice(color_palette)}; font-size: 0.9em; font-weight: 600;">#{tag}</span>'
        for tag in tags
    )

