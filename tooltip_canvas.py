"""
title: Tooltip mosaic
description: 
debrier: Architecturally, is organized around a couple of steps: (1) forging and (2) styling the tooltip. The former
         defines the tooltip content, while the second defines aesthetics and triggering logic. The class is built on
         the assumption of applying tootips for existing elements, a self-container dummy case is provided.
"""

import hashlib
import time
import html
import streamlit as st
import time
import streamlit as st
from typing import Union, List

# Default tooltip content styling
DEFAULT_TOOLTIP_STYLES = {
"visibility": "hidden",
"opacity": "0",
"width": "300px",
"background": "rgba(23, 33, 43, 0.5)",
"color": "#ffffff",
"padding": "10px",
"border-radius": "8px",
"box-shadow": "0px 4px 20px rgba(255, 255, 255, 0.1)",
"position": "absolute",
"left": "50%",
"top": "100%",
"transform": "translateX(-50%) translateY(-5px)",
"transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out, transform 0.3s ease-in-out",
"backdrop-filter": "blur(6px)",
"z-index": "10",
"border": "2px solid rgba(255, 255, 255, 0.9)"
}

# Default animation styles
DEFAULT_ANIMATION_STYLES = {
"name": "floatTooltip",
"keyframes": """
@keyframes floatTooltip {
   0%   { transform: translateX(-50%) translateY(0px); }
   50%  { transform: translateX(-50%) translateY(4px); }
   100% { transform: translateX(-50%) translateY(0px); }
}
""",
"animation": "floatTooltip 2s infinite ease-in-out"
}

class TooltipCanvas:

    def __init__(self, tooltip_styles=None, animation_styles=None):
        """
        Initializes the TooltipCanvas with optional styling overrides.
        :param tooltip_styles: Dictionary of CSS properties for .tc-tooltip-content.
        :param animation_styles: Dictionary to override tooltip animation styles.
        """
        self.timestamp = int(time.time())  # Forces CSS refresh
        self.tooltip_styles = {**DEFAULT_TOOLTIP_STYLES, **(tooltip_styles or {})}
        self.animation_styles = {**DEFAULT_ANIMATION_STYLES, **(animation_styles or {})}

    def _define_tooltip(self, content: Union[str, List[str]], element_id: str):
        """Generates the tooltip HTML, supporting multiple content items in a grid."""
        
        # Ensure content is a list
        if isinstance(content, str):
            content = [content]
    
        # Generate the grid items for the tooltip
        grid_items = "".join(
            f'<div class="tc-tooltip-item">{item}</div>' for item in content
        )
    
        return f"""
        <div class="tc-tooltip-container">
            <span id="{element_id}" class="tc-tooltip-trigger">Hover me</span>
            <div class="tc-tooltip-content tc-tooltip-{element_id}">
                <div class="tc-tooltip-grid">
                    {grid_items}
                </div>
            </div>
        </div>
        """


    def _generate_tooltip_css(self, element_id: str):
        """Generates the CSS styles, applying user-defined overrides."""
        tooltip_styles = "; ".join(f"{k}: {v}" for k, v in self.tooltip_styles.items())
        animation_styles = self.animation_styles["animation"]
        keyframes = self.animation_styles["keyframes"]

        return f"""
        <style>
            /* Timestamp {self.timestamp} to force refresh */
            {keyframes}

            .tc-tooltip-container {{
                display: inline;
                position: relative;
            }}

            .tc-tooltip-trigger {{
                color: rgb(0, 115, 177);
                border-bottom: 1px dashed rgb(0, 115, 177);
                cursor: pointer;
            }}

            .tc-tooltip-content {{
                {tooltip_styles};
                animation: {animation_styles};
            }}

            .tc-tooltip-container:hover .tc-tooltip-{element_id} {{
                visibility: visible;
                opacity: 1;
                transform: translateX(-50%) translateY(0px);
            }}
        </style>
        """

    def apply_tooltip(self, element_id: str, content: str):
        """Applies a tooltip to an existing element by injecting the required HTML & CSS."""
        tooltip_html = self._define_tooltip(content, element_id)
        tooltip_css = self._generate_tooltip_css(element_id)

        st.markdown(tooltip_css, unsafe_allow_html=True)
        st.markdown(tooltip_html, unsafe_allow_html=True)

    def render_test_case(self):
        """Renders a test case for visual verification of tooltips."""
        test_id = "test-tooltip"

        # Render a visible component
        st.markdown(
            f'<div id="{test_id}" class="tc-test-box">I have a tooltip attached</div>',
            unsafe_allow_html=True
        )

        # Apply tooltip to the test element
        self.apply_tooltip(test_id, "I am the tooltip!")

        # Additional styling for the test box
        st.markdown(
            """
            <style>
                .tc-test-box {
                    background: #ddd;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    color: #333;
                    font-weight: bold;
                    display: inline-block;
                    margin-top: 20px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
