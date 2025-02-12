import streamlit as st
import streamlit.components.v1 as components
import os

def render_item_visual_content(title, description, media_path, width="700px", height="400px"):
    """
    Render the visual content based on the provided metadata with minimal spacing.
    Supports images, videos, and HTML.
    """
    
    # Determine file type
    file_ext = os.path.splitext(media_path)[-1].lower()

    # Define base styles
    st.markdown(
        f"""
        <style>
            .media-container {{
                width: {width};
                height: {height};
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                background: rgba(0, 0, 0, 0.05);
                border-radius: 10px;
                margin-bottom: 5px;
            }}
            .text-container {{
                background: rgba(0, 0, 0, 0.3);
                padding: 6px;
                border-radius: 8px;
                color: white;
                width: 100%;
                text-align: center;
                margin-top: 5px;
            }}
            .title-text {{
                font-size: 18px;
                font-weight: 600;
                color: #fff;
                display: block;
            }}
            .description-text {{
                font-size: 14px;
                font-weight: 400;
                color: #ddd;
                display: block;
                margin-top: 3px;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Render media based on type
    if not os.path.exists(media_path):
        st.error(f"File not found: {media_path}")
        return

    with st.container():
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            st.image(media_path, use_column_width=True)

        elif file_ext in ['.mp4', '.avi', '.mov', '.webm']:
            st.video(media_path)

        elif file_ext == '.html':
            try:
                with open(media_path, 'r') as file:
                    html_content = file.read()
                components.html(html_content, width=int(width.replace("px", "")), height=int(height.replace("px", "")))
            except Exception as e:
                st.error(f"Error loading HTML content: {str(e)}")

        else:
            st.error(f"Unsupported media type: {file_ext}")

    # Render the text section
    st.markdown(
        f"""
        <div class="text-container">
            <span class="title-text">{title}</span>
            <span class="description-text">{description}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
