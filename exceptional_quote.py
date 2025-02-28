"""
title: Exceptional Quote
description: A custom front-end component to highlight notable quotes.
"""

import streamlit as st

def exceptional_but_subtle_quote(markdown_text: str):
    """
    Render a subtle notable quote with:
    - 5% left indentation.
    - Soft shadow effect on bottom and right.
    - No special font styling (blends naturally).
    - Properly parsed markdown inside the styled container.
    - Minimal spacing at the bottom for clarity.
    - Vertically centered text.
    """
    subtle_style = f"""
        <div style="
            padding: 10px;
            margin-left: 5%;
            border-radius: 6px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.05);
            display: flex;
            align-items: center;
            min-height: 60px;
        ">
            {markdown_text}

    """
    
    st.markdown(subtle_style, unsafe_allow_html=True)
