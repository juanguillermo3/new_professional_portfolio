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

import streamlit as st
import time

class TooltipCanvas:
    def __init__(self):
        """Initializes the tooltip canvas system."""
        self.timestamp = int(time.time())  # Forces CSS refresh

    def _define_tooltip(self, content: str, unique_id: str):
        """Private method to generate the tooltip HTML."""
        return f"""
        <div class="tc-tooltip-container">
            <span id="{unique_id}" class="tc-tooltip-trigger">Hover me</span>
            <div class="tc-tooltip-content tc-tooltip-{unique_id}">
                {content}
            </div>
        </div>
        """

    def apply_tooltip(self, element_id: str, content: str):
        """Applies a tooltip to an existing element by injecting the required HTML & CSS."""
        tooltip_html = self._define_tooltip(content, element_id)
        tooltip_css = f"""
        <style>
            /* Timestamp {self.timestamp} to force refresh */
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
                visibility: hidden;
                opacity: 0;
                width: 300px;
                background: rgba(23, 33, 43, 0.5);
                color: #ffffff;
                padding: 10px;
                border-radius: 8px;
                box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.1);
                position: absolute;
                left: 50%;
                top: 100%;
                transform: translateX(-50%) translateY(-5px);
                transition: opacity 0.3s ease-in-out, 
                            visibility 0.3s ease-in-out, 
                            transform 0.3s ease-in-out;
                backdrop-filter: blur(6px);
                z-index: 10;
                border: 2px solid rgba(255, 255, 255, 0.9);
            }}

            .tc-tooltip-container:hover .tc-tooltip-{element_id} {{
                visibility: visible;
                opacity: 1;
                transform: translateX(-50%) translateY(0px);
            }}
        </style>
        """
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

import streamlit as st
import time

class TooltipCanvas:
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

    def __init__(self, tooltip_styles=None, animation_styles=None):
        """
        Initializes the TooltipCanvas with optional styling overrides.
        :param tooltip_styles: Dictionary of CSS properties for .tc-tooltip-content.
        :param animation_styles: Dictionary to override tooltip animation styles.
        """
        self.timestamp = int(time.time())  # Forces CSS refresh
        self.tooltip_styles = {**self.DEFAULT_TOOLTIP_STYLES, **(tooltip_styles or {})}
        self.animation_styles = {**self.DEFAULT_ANIMATION_STYLES, **(animation_styles or {})}

    def _define_tooltip(self, content: str, unique_id: str):
        """Private method to generate the tooltip HTML."""
        return f"""
        <div class="tc-tooltip-container">
            <span id="{unique_id}" class="tc-tooltip-trigger">Hover me</span>
            <div class="tc-tooltip-content tc-tooltip-{unique_id}">
                {content}
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


import streamlit as st
import time

class TooltipCanvas:
    # Default tooltip content styling
    DEFAULT_TOOLTIP_STYLES = {
        "background": "rgba(23, 33, 43, 0.85)",
        "color": "#ffffff",
        "padding": "10px",
        "border-radius": "8px",
        "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.3)",
        "position": "absolute",
        "left": "50%",
        "top": "100%",
        "transform": "translateX(-50%)",
        "z-index": "10",
        "display": "grid",
        "grid-template-columns": "repeat(auto-fill, minmax(120px, 1fr))",
        "gap": "4px",
        "animation": "floatTooltip 1.5s infinite ease-in-out",
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
        "animation": "floatTooltip 1.5s infinite ease-in-out",
    }

    def __init__(self, tooltip_styles=None, animation_styles=None):
        """
        Initializes the TooltipCanvas with optional styling overrides.
        :param tooltip_styles: Dictionary of CSS properties for .tc-tooltip-content.
        :param animation_styles: Dictionary for custom animations.
        """
        self.tooltip_styles = {**self.DEFAULT_TOOLTIP_STYLES, **(tooltip_styles or {})}
        self.animation_styles = {**self.DEFAULT_ANIMATION_STYLES, **(animation_styles or {})}

    def _define_tooltip(self, content, unique_id):
        """Private method to generate the HTML structure for a single or multiple tooltips."""
        if isinstance(content, str):  
            # Single tooltip
            tooltip_content = f'<div class="tc-tooltip-content">{content}</div>'
        elif isinstance(content, list):
            # Create a column-major grid for multiple tooltips
            tooltip_content = '<div class="tc-tooltip-grid">'
            tooltip_content += "".join(
                f'<div class="tc-tooltip-item">{item}</div>' for item in content
            )
            tooltip_content += "</div>"
        else:
            raise ValueError("Content should be either a string or a list of strings.")

        return f"""
        <div class="tc-tooltip-container">
            <span id="{content}" class="tc-tooltip-trigger">Hover me</span>
            {tooltip_content}
        </div>
        """

    def _generate_tooltip_css(self, element_id: str):
        """Generates the CSS styles, applying user-defined tooltip and animation settings."""
        tooltip_styles = "; ".join(f"{k}: {v}" for k, v in self.tooltip_styles.items())
        animation_name = self.animation_styles["name"]
        keyframes = self.animation_styles["keyframes"]
        grid_columns = self.tooltip_styles.get("grid-template-columns", "repeat(auto-fill, minmax(100px, 1fr))")

        return f"""
        <style>
            /* Force refresh with timestamp */
            {keyframes}

            .tc-tooltip-container {{
                position: relative;
                display: inline-block;
                cursor: pointer;
            }}

            .tc-tooltip-trigger {{
                text-decoration: underline;
                color: #0077cc;
                cursor: pointer;
            }}

            .tc-tooltip-content {{
                {tooltip_styles}
                animation: {animation_name};
            }}

            .tc-tooltip-item {{
                background: rgba(0, 0, 0, 0.7);
                padding: 8px;
                margin: 2px;
                border-radius: 4px;
                text-align: center;
                font-size: 14px;
            }}

            .tc-tooltip-container:hover .tc-tooltip-content {{
                visibility: visible;
                opacity: 1;
                transform: translateX(-50%) translateY(0px);
            }}
        </style>
        """

    def apply_tooltip(self, element_id, content):
        """Applies the tooltip with user-defined content."""
        tooltip_html = self._define_tooltip(content, element_id)
        tooltip_css = self._generate_tooltip_css(element_id)

        st.markdown(tooltip_css, unsafe_allow_html=True)
        st.markdown(tooltip_html, unsafe_allow_html=True)

    def render_test_case(self, test_content=None):
        """Renders a test case for debugging tooltips visually."""
        test_id = "test-tooltip"
        if test_content is None:
            test_content = ["Tooltip part 1", "Tooltip part 2"]

        # Render the test box
        st.markdown(
            f'<div class="tc-test-box">I have a tooltip attached</div>',
            unsafe_allow_html=True
        )

        # Apply tooltip using the provided content
        self.apply_tooltip(test_id, test_content)

        # Additional test box styling
        st.markdown(
            """
            <style>
                .tc-test-box {
                    background: #ccc;
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


import streamlit as st
import time

class TooltipCanvas:
    # Default tooltip styles
    DEFAULT_TOOLTIP_STYLES = {
        "width": "300px",
        "background": "rgba(23, 33, 43, 0.5)",
        "color": "#ffffff",
        "padding": "5px",
        "border-radius": "5px",
        "position": "absolute",
        "left": "50%",
        "transform": "translateX(-50%)",
        "visibility": "hidden",
        "opacity": "0",
        "transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out"
    }

    # Default animation styles
    DEFAULT_ANIMATION_STYLES = {
        "name": "floatTooltip",
        "animation": "floatTooltip 1.5s infinite",
        "keyframes": """
            @keyframes floatTooltip {
                0%   { transform: translateX(-50%) translateY(0px); }
                50%  { transform: translateX(-50%) translateY(4px); }
                100% { transform: translateX(-50%) translateY(0px); }
            }
        """
    }

    def __init__(self, tooltip_styles=None, animation_styles=None):
        """
        Initializes the TooltipCanvas with optional styling overrides.
        :param tooltip_styles: Dictionary with CSS styles for the tooltip content.
        :param animation_styles: Dictionary with animation styles.
        """
        self.timestamp = int(time.time())  # Force CSS refresh
        self.tooltip_styles = {**self.DEFAULT_TOOLTIP_STYLES, **(tooltip_styles or {})}
        self.animation_styles = {**self.DEFAULT_ANIMATION_STYLES, **(animation_styles or {})}

    def _generate_tooltip_css(self, element_id: str):
        """Generates the CSS styles for tooltips."""
        tooltip_styles = "".join([f"{key}: {value};" for key, value in self.tooltip_styles.items()])
        animation_styles = self.animation_styles["animation"]
        keyframes = self.animation_styles["keyframes"]

        return f"""
        <style>
            /* Tooltip Container */
            .tc-tooltip-container-{element_id} {{
                position: relative;
                display: inline-block;
            }}

            /* Tooltip Styling */
            .tc-tooltip-{element_id} {{
                {tooltip_styles}
                display: none;
            }}

            .tc-tooltip-container-{element_id}:hover .tc-tooltip-content-{element_id} {{
                visibility: visible;
                opacity: 1;
                transform: translateX(-50%) translateY(4px);
                animation: {animation_styles};
            }}

            {self.animation_styles["keyframes"]}
        </style>
        """

    def _define_tooltips(self, contents, element_id: str):
        """Generates multiple tooltip spans inside the same container."""
        if isinstance(content, str):
            contents = [content]
        else:
            contents = content  # Assume it's already a list

        tooltip_spans = "".join(f'<span class="tc-tooltip-content-{element_id}" style="{self._style_inline()}">{c}</span>' for c in contents)
        return f"""
        <div class="tc-tooltip-container-{element_id}">
            {tooltip_spans}
        </div>
        """

    def _get_style_string(self):
        return f"/* Timestamp: {self.timestamp} */" + self._generate_tooltip_css("tooltip")

    def apply_tooltips(self, element_id: str, content):
        """
        Applies tooltips to an element.
        :param element_id: Unique identifier for the target element.
        :param content: List of tooltip texts or a single string.
        """
        if isinstance(content, str):
            content = [content]
        
        tooltip_html = self._define_tooltips(content, element_id)
        
        st.markdown(self._generate_tooltip_css(element_id), unsafe_allow_html=True)
        st.markdown(tooltip_html, unsafe_allow_html=True)
    
    def render_test_case(self):
        """Renders a test case for visual verification of tooltips.""
        test_id = "test"
        st.markdown(f'<div id="{test_id}" class="tc-test-box">Hover over me for multiple tooltips</div>', unsafe_allow_html=True)
        self.apply_tooltips(test_id, ["First Tooltip", "Second Tooltip", "Third Tooltip"])

        # Test box styles
        st.markdown("""
            <style>
                .tc-test-box {
                    background: #ddd;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    cursor: pointer;
                }
            </style>
            """, unsafe_allow_html=True)
        





