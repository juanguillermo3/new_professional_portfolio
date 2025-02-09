import hashlib
import streamlit as st

def html_for_item_data(rec):
    """Generate HTML for a recommended item card dynamically."""
    background_color = "#f4f4f4"
    border_style = "1px solid #ddd"
    card_height = "150px"
    overflow_style = "overflow-y: auto;"
    
    galleria_present = "galleria" in rec
    title = prettify_title(rec['title'])
    if galleria_present:
        title = f"⭐ {title}"
    
    return f"""
        <div style="background-color: {background_color}; border: {border_style}; 
                    border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                    padding: 10px; text-align: center; height: {card_height}; {overflow_style}; 
                    position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; background-color: rgba(255, 255, 255, 0.7); 
                        padding: 5px 10px; border-radius: 10px 10px 0 0; font-size: 16px; font-weight: bold; z-index: 10;">
                {title}
            </div>
            <div style="margin-top: 40px; padding: 0 10px; overflow-y: auto; height: calc(100% - 40px); text-align: justify;">
                {rec['description']}
            </div>
        </div>
    """
