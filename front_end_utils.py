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
    # Generate styled hashtags (implement UI styling accordingly)
    return [f"<span style='color:{color}; font-weight:bold;'>#{tag}</span>"
            for tag, color in zip(tags, color_palette[:len(tags)])]


