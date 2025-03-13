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

# Default tooltip content styling
DEFAULT_TOOLTIP_STYLES = {
    "visibility": "hidden",
    "opacity": "0",
    "width": "300px",
    "background": "rgba(23, 33, 43, 0.5)",
    "color": "#ffffff",
    "padding": "10px",
    "position": "absolute",
    "border": "1px solid rgba(255, 255, 255, 0.9)",
    "border-radius": "5px",
    "box-shadow": "0px 4px 20px rgba(255, 255, 255, 0.1)",
    "left": "50%",
    "top": "100%",
    "transform": "translateX(-50%) translateY(-5px)",
    "transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out, transform 0.3s ease-in-out",
    "opacity": "0",
    "position": "absolute",
}

# Default animation styles
DEFAULT_ANIMATION_STYLES = {
    "name": "tooltip-fade",
    "animation": "floatTooltip 1.5s ease-in-out infinite",
    "keyframes": """
    @keyframes tooltipFloat {
        0%   { transform: translateX(-50%) translateY(0px); }
        50%  { transform: translateX(-50%) translateY(4px); }
        100% { transform: translateX(-50%) translateY(0px); }
    }
    """
}

class TooltipCanvas:
    def __init__(
        self, 
        tooltip_styles=DEFAULT_TOOLTIP_STYLES, 
        animation_styles=DEFAULT_ANIMATION_STYLES
    ):
        """
        Initializes the TooltipCanvas with optional styling overrides.
        :param tooltip_styles: Dictionary of CSS properties for .tc-tooltip elements.
        :param animation_styles: Dictionary of animation styles.
        """
        self.timestamp = int(time.time())  # Forces CSS refresh
        self.tooltip_styles = {**DEFAULT_TOOLTIP_STYLES, **(tooltip_styles or {})}
        self.animation_styles = {**DEFAULT_ANIMATION_STYLES, **(animation_styles or {})}

    def _define_tooltip(self, content, unique_id):
        """Private method to generate the tooltip HTML."""
        return f"""
        <div class="tc-tooltip-container">
            <span id="{unique_id}" class="tc-tooltip-trigger">Hover me</span>
            <div class="tc-tooltip-content tc-tooltip-{unique_id}">
                {content}
            </div>
        </div>
        """
    
    def _generate_tooltip_css(self, element_id):
        """Generates the CSS styles for the tooltip."""
        tooltip_styles = "\n".join(
            [f".tc-tooltip-{element_id} {{ {k}: {v}; }}" for k, v in self.tooltip_styles.items()]
        )
        keyframes = self.animation_styles["keyframes"]
        animation_styles = f".tc-tooltip-{element_id} {{ animation: {self.animation_styles['name']} 1s ease-in-out infinite alternate; }}"
        
        return f"""
        <style>
            {keyframes}
            {tooltip_css}
            {animation_styles}
            .tc-tooltip-container {{ position: relative; display: inline-block; cursor: pointer; }}
            .tc-tooltip-trigger {{ color: rgb(0, 115, 177); border-bottom: 1px dashed rgb(0, 115, 177); }}
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
        
        st.markdown(
            f"""<div class="tc-tooltip-container">
                <span id="{test_id}" class="tc-tooltip-trigger">I am a tooltip trigger</span>
                <div class="tc-tooltip-{test_id}">I am a tooltip attached</div>
            </div>""",
            unsafe_allow_html=True
        )
        
        st.markdown(self._generate_tooltip_css(test_id), unsafe_allow_html=True)
        
        st.markdown(
            """
            <style>
                .tc-tooltip-container {{ position: relative; display: inline-block; cursor: pointer; }}
                .tc-test-tooltip {{
                    background: #ddd;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    color: #333;
                    font-weight: bold;
                    text-align: center;
                    margin-top: 20px;
                }}
            </style>
            <div class="tc-test-tooltip">Hover over me to see tooltip</div>
            """,
            unsafe_allow_html=True
        )
        
        # Apply tooltip to the test element
        self.apply_tooltip(test_id, "I am a tooltip attached")
