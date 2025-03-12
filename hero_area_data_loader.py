import streamlit as st
import os
import json
from dotenv import load_dotenv
from exceptional_ui import (
    html_for_tooltip_from_large_list,
    install_tooltip_styling,
    install_tooltip_triggering_logic
)

# Load environment variables
load_dotenv()

# Retrieve the mock prefix from the environment, defaulting to "[MOCK TOOLTIP]" if not set
MOCK_INFO_PREFIX = os.getenv("MOCK_INFO", "[MOCK INFO]")

def load_quote():
    return [
        "<b>Modern data analysis</b> requires engaging with and developing <b>substantial software</b>, "  
        "such as <b>data gathering, processing, and visualization applications</b>. "  
        "Moreover, <b>software automation</b> is key for <b>distributing inferences</b> from <b>statistical analysis</b>, "  
        "whether derived from <b>econometric models</b> or <b>machine learning predictions</b>. "  
        "Bottom line: I recognize the deep connection between <b>data analysis</b> and <b>software development</b>, "  
        "hence my effort to <b>serve them within a unified framework</b>." ,
            
        "I am Juan Guillermo, a professional economist. "  
        "I have built my career developing data analysis and software application scripts "  
        "for research and operational environments. "  
        "My business is discovering the more <b>powerful abstractions</b> to <b>effectively work with data</b>, "  
        "implementing them with <b>software engineering standards</b> to <b>build up data-driven intelligence</b> "  
        "for key corporate and social systems. "  
        "My broader professional vision interconnects all the technologies essential for modern data analysis—"  
        "spanning <b>data mining</b>, <b>artificial intelligence models</b>, <b>algorithms</b>, <b>software engineering workflows</b>, "  
        "and <b>information tools</b>—into a cohesive and holistic framework."  

    ]

def load_avatar_caption():
    return "God told me I could either be good-looking or an excellent worker."

def load_code_samples():
    return [
        {"title": "🚀 Genetic Algorithms for forecasting app sales", "url": "https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz"},
        {"title": "🧩 Ensemble Learning for automated hiring in Human Resources", "url": "https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvAO"}
    ]

import html
import hashlib
import datetime

def html_for_tooltip_from_large_list(items, label, element_id, color="#007BFF", emoji=None):
    """
    Generates an HTML snippet displaying a summarized preview of a list with a hidden tooltip.

    Parameters:
        - items (list of str): The list of items to display.
        - label (str): Describes the type of items being enumerated.
        - element_id (str): The base ID of the element.
        - color (str): Color for the summary text (default: #007BFF).
        - emoji (str, optional): Emoji prepended to each listed item.

    Returns:
        - str: HTML snippet containing the summarized text and a tooltip for full details.
    """
    if not items:
        return f'<div style="color:gray;">No {label.lower()} listed</div>'

    # Generate a unique ID by hashing element_id with the current date
    unique_hash = hashlib.md5(f"{element_id}_{datetime.datetime.now().isoformat()}".encode()).hexdigest()[:10]
    unique_id = f"{element_id}_{unique_hash}"

    first_item = html.escape(items[0])
    summary = f"(and {len(items) - 1} more {label.lower()})" if len(items) > 1 else ""
    visible_text = f'<span style="color:{color}; border-bottom: 1px dashed {color};">{first_item} {summary}</span>'

    tooltip_content = "".join(
        f'<div style="color:{color}; margin-bottom: 4px;">{(emoji + " " if emoji else "")}{html.escape(item)}</div>'
        for item in items
    )

    return f"""
        <div style="position: relative; display: inline-block; max-width: 100%;">
            {visible_text}
            <div id="{unique_id}" style="
                visibility: hidden;
                opacity: 0;
                background: rgba(20, 20, 20, 0.9);
                color: #ffffff;
                padding: 12px;
                border-radius: 8px;
                box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.5);
                position: absolute;
                left: 50%;
                top: 120%;
                width: 300px;
                text-align: left;
                z-index: 10;
                border: 1px solid rgba(255, 255, 255, 0.2);
                transform: translateX(-50%);
            ">
                <strong>All {label} listed:</strong>
                {tooltip_content}
            </div>
        </div>
    """


