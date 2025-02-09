import hashlib
import streamlit as st
from front_end_utils import prettify_title
import re

def html_for_item_data(rec):
    """
    Generate an HTML snippet for a recommended item card dynamically.
    
    Parameters:
    - rec (dict): A dictionary containing item metadata with the following fields:
        - "title" (str): The title of the recommended item.
        - "description" (str): A short descriptive text for the item.
        - "galleria" (bool, optional, legacy): Marks outstanding content (deprecated).
        - "highlighted_content" (bool, optional, preferred): Marks outstanding content.

    Returns:
    - str: A formatted HTML string representing the item card.
    """
    
    # Define styling attributes
    background_color = "#f4f4f4"  # Light gray background
    border_style = "1px solid #ddd"  # Thin, soft border
    card_height = "150px"  # Fixed height for uniformity
    overflow_style = "overflow-y: auto;"  # Enables vertical scrolling if content overflows

    # Use regex to detect any outstanding content key
    outstanding_content_regex = re.compile(r"^(galleria|highlighted_content)$", re.IGNORECASE)
    is_outstanding = any(outstanding_content_regex.match(key) and rec.get(key) for key in rec)

    # Apply title transformation
    title = prettify_title(rec['title'])
    if is_outstanding:
        title = f"⭐ {title}"  # Highlight special items
    
    # Return the HTML structure
    return f"""
        <div style="background-color: {background_color}; border: {border_style}; 
                    border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                    padding: 10px; text-align: center; height: {card_height}; {overflow_style}; 
                    position: relative; overflow: hidden;">
            
            <!-- Title Banner -->
            <div style="position: absolute; top: 0; left: 0; right: 0; 
                        background-color: rgba(255, 255, 255, 0.7); 
                        padding: 5px 10px; border-radius: 10px 10px 0 0; 
                        font-size: 16px; font-weight: bold; z-index: 10;">
                {title}
            </div>
            
            <!-- Description Content -->
            <div style="margin-top: 40px; padding: 0 10px; overflow-y: auto; 
                        height: calc(100% - 40px); text-align: justify;">
                {rec['description']}
            </div>
        </div>
    """

