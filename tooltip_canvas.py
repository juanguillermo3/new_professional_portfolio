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
from media_carrousel import html_for_media_carousel, dummy_media_list 
         
# Default tooltip content styling
DEFAULT_TOOLTIP_STYLES = {
    "width": "300px",
    "background": "rgba(23, 33, 43, 0.5)",
    "color": "#ffffff",
    #"padding": "5px 10px",  # Minimal padding: 5px top/bottom, 10px left/right
    "border-radius": "8px",
    "box-shadow": "0px 4px 20px rgba(255, 255, 255, 0.1)",
    "transition": "opacity 0.3s ease-in-out, visibility 0.3s ease-in-out, transform 0.3s ease-in-out",
    "backdrop-filter": "blur(6px)",
    "z-index": "9999",
    "border": "2px solid rgba(255, 255, 255, 0.9)",
    
    # Additional spacing control:
    "margin": "8px",  # Adds space between tooltips (vertical & horizontal spacing)

    # Enforce non-bold text
    "font-weight": "normal",

    # Ensure justified text alignment
    #"text-align": "justify"
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

    def _define_tooltip(self, content: Union[str, List[Union[str, List[str]]]], element_id: str, visible_text: str = "Hover me") -> str:
        """Generates the tooltip HTML, supporting multiple lists rendered in a flexible grid layout."""
        
        # Ensure content is always a list of lists
        if isinstance(content, str):
            content = [[content]]  # Wrap in a nested list
        elif isinstance(content, list) and all(isinstance(item, str) for item in content):
            content = [content]  # Wrap in a single column
    
        # Generate HTML for the tooltip grid
        grid_items = "".join(
            f"<div class='tc-tooltip-item'>{item}</div>"
            for sublist in content
            for item in sublist
        )
    
        return f'''
        <div class="tc-tooltip-container">
            {self._generate_tooltip_trigger(element_id, visible_text)}
            <div class="tc-tooltip-content tc-tooltip-{element_id}">
                <div class="tc-tooltip-grid">
                    {grid_items}
                </div>
            </div>
        </div>
        '''

             
    def _define_tooltip(self, content: Union[str, List[Union[str, List[str]]]], element_id: str, visible_text: str = "Hover me") -> str:
       """Generates the tooltip HTML, supporting multiple lists rendered in a flexible grid layout."""
       
       # Ensure content is always a list of lists
       if isinstance(content, str):
           content = [[content]]  # Wrap in a nested list
       elif isinstance(content, list) and all(isinstance(item, str) for item in content):
           content = [content]  # Wrap in a single column
    
       # Generate HTML for the tooltip grid
       grid_columns = "".join(
           f'<div class="tc-tooltip-column">{" ".join(f"<div class=\'tc-tooltip-item\'>{item}</div>" for item in sublist)}</div>'
           for sublist in content
       )
       
       return f'''
       <div class="tc-tooltip-container">
           {self._generate_tooltip_trigger(element_id, visible_text)}
           <div class="tc-tooltip-content tc-tooltip-{element_id}">
               <div class="tc-tooltip-grid">
                   {grid_columns}
               </div>
           </div>
       </div>
       '''
                     
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
                display: inline-block; /* Ensures proper spacing */
                position: relative;
            }}
    
            .tc-tooltip-content.tc-tooltip-{element_id} {{
                position: absolute;
                left: 50%;
                top: 100%;
                transform: translateX(-50%);
                width: auto;
                max-width: 1000px;
                padding: 10px;
                background: rgba(0, 0, 0, 0.8);
                border-radius: 5px;
                color: white;
                visibility: hidden;
                opacity: 0;
                transition: opacity 0.2s ease-in-out, transform 0.2s ease-in-out;
                z-index: 9999;
            }}
    
            .tc-tooltip-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, 300px); /* ✅ Forces proper column layout */
                gap: 10px;
                justify-content: center;
                padding: 10px;
            }}
    
            .tc-tooltip-container:hover .tc-tooltip-content.tc-tooltip-{element_id} {{
                visibility: visible;
                opacity: 1;
                transform: translateX(-50%) translateY(5px);
            }}
    
            .tc-tooltip-item {{
                width: 300px; /* ✅ Ensures all items align properly */
                text-align: center;
                padding: 8px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 3px;
                {tooltip_styles};
                animation: {animation_styles};
            }}
    
            .tc-tooltip-trigger {{
                color: rgb(0, 115, 177);
                border-bottom: 1px dashed rgb(0, 115, 177);
                cursor: pointer;
                font-weight: normal;
            }}
    
        </style>
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
                display: inline-block; /* Inline-block to ensure proper spacing */
                position: relative;
            }}
    
            .tc-tooltip-content.tc-tooltip-{element_id} {{
                position: absolute;
                left: 50%;
                top: 100%;
                transform: translateX(-50%); /* Center tooltip */
                width: auto; /* Let grid dictate width */
                max-width: 1000px; /* Adjust if needed */
                padding: 10px;
                background: rgba(0, 0, 0, 0.8);
                border-radius: 5px;
                color: white;
                visibility: hidden;
                opacity: 0;
                transition: opacity 0.2s ease-in-out, transform 0.2s ease-in-out;
                z-index: 9999;
            }}
    
            .tc-tooltip-grid {{
                display: grid; /* ✅ Enable grid */
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* ✅ Dynamic 300px-wide columns */
                justify-content: center; /* ✅ Center columns */
                gap: 10px; /* ✅ Ensure proper spacing */
                padding: 10px;
            }}
    
            .tc-tooltip-container:hover .tc-tooltip-content.tc-tooltip-{element_id} {{
                visibility: visible;
                opacity: 1;
                transform: translateX(-50%) translateY(5px); /* ✅ Smooth reveal effect */
            }}
            
            .tc-tooltip-item {{
                width: 300px; /* ✅ Ensure fixed width per item */
                text-align: center;
                padding: 8px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 3px;
                {tooltip_styles}; /* ✅ Apply custom styles */
                animation: {animation_styles}; /* ✅ Apply animations */
            }}
    
            .tc-tooltip-trigger {{
                color: rgb(0, 115, 177);
                border-bottom: 1px dashed rgb(0, 115, 177);
                cursor: pointer;
                font-weight: normal;
            }}
    
        </style>
        """

    def _generate_tooltip_trigger(self, element_id: str, visible_text: str = "Hover me") -> str:
        """Generates the HTML for the visible tooltip trigger element."""
        return f'<span id="{element_id}" class="tc-tooltip-trigger">{visible_text}</span>'


    def html_to_apply_tooltip(self, element_id: str, content: str, visible_text: str = "Hover me"):
        """Returns the HTML and CSS required to apply a tooltip to an element."""
        tooltip_html = self._define_tooltip(content, element_id, visible_text)
        tooltip_css = self._generate_tooltip_css(element_id)
        return tooltip_html, tooltip_css

    def apply_tooltip(self, element_id: str, content: str, visible_text: str = "Hover me"):
        """Applies a tooltip to an existing element by injecting the required HTML & CSS."""
        tooltip_html = self._define_tooltip(content, element_id, visible_text)
        tooltip_css = self._generate_tooltip_css(element_id)

        st.markdown(tooltip_css, unsafe_allow_html=True)
        st.markdown(tooltip_html, unsafe_allow_html=True)

    def render_test_case(self):
        """Renders a test case for visual verification of tooltips with grid layout."""
        test_id = "test-tooltip"
    
        # Define test data (arbitrary HTML content)
        test_content = [
            ["<strong>First Column - Row 1</strong>", "<em>First Column - Row 2</em>"],
            [
                "<span style='color: blue;'>Second Column - Row 1</span>",
                "<u>Second Column - Row 2</u>",
                html_for_media_carousel(dummy_media_list+[{'src': 'assets//wages.png', 'alt': 'Media 1'}]+[{'src': 'assets//stores_summary.html', 'alt': 'Media 2'}]    )
            ],
            ["<button onclick='alert(\"Clicked!\")'>Click Me</button>"]
        ]
    
    
        # Apply tooltip with grid structure
        self.apply_tooltip(test_id, test_content, visible_text="Hoover me for more info")

