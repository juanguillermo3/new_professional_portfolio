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

class TooltipCanvas:
    def __init__(self):
        self.unique_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:10]

    def _define_tooltip(self, content: str) -> str:
        """
        Generates the tooltip HTML structure.
        """
        return f'''
        <div class="tooltip-container">
            <div id="tooltip-{self.unique_id}" class="tooltip-content">
                {html.escape(content)}
            </div>
        </div>
        '''

    def apply_tooltip(self, element_id: str, content: str):
        """
        Injects the tooltip styling and behavior into the DOM for a given element.
        """
        tooltip_html = self._define_tooltip(content)
        
        tooltip_css = f'''
        <style>
            .tooltip-container {{
                position: relative;
                display: inline-block;
            }}
            
            .tooltip-content {{
                visibility: hidden;
                opacity: 0;
                width: 300px;
                background: rgba(23, 33, 43, 0.8);
                color: white;
                text-align: center;
                padding: 10px;
                border-radius: 8px;
                position: absolute;
                left: 50%;
                top: 100%;
                transform: translateX(-50%) translateY(-5px);
                transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out, transform 0.3s ease-in-out;
                z-index: 10;
            }}
            
            @keyframes floatTooltip {{
                0%   {{ transform: translateX(-50%) translateY(-5px); }}
                50%  {{ transform: translateX(-50%) translateY(0px); }}
                100% {{ transform: translateX(-50%) translateY(-5px); }}
            }}
            
            #{element_id}:hover + .tooltip-container .tooltip-content {{
                visibility: visible;
                opacity: 1;
                animation: floatTooltip 2.5s infinite alternate ease-in-out;
            }}
        </style>
        '''
        
        st.markdown(tooltip_css, unsafe_allow_html=True)
        st.markdown(tooltip_html, unsafe_allow_html=True)

    def render_test_case(self):
        """
        Renders a test case with a styled box and an attached tooltip.
        """
        test_element_id = f"test-box-{self.unique_id}"
        
        test_box_html = f'''
        <div id="{test_element_id}" style="
            display: inline-block;
            padding: 15px 20px;
            background: gray;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;">
            I have a tooltip attached
        </div>
        '''
        
        st.markdown(test_box_html, unsafe_allow_html=True)
        self.apply_tooltip(test_element_id, "I am the tooltip")
