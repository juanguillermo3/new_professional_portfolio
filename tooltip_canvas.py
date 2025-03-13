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
