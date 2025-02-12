import streamlit as st
import streamlit.components.v1 as components
import os
import glob

def render_item_visual_content(title, description, media_path, width="700px", height="400px"):
    """
    Render visual content based on metadata with minimal spacing.
    Supports images, videos, and HTML. Allows navigation if multiple media files match a glob pattern.
    """

    # Resolve file paths
    file_list = glob.glob(media_path) if '*' in media_path or '?' in media_path else [media_path]
    file_list = sorted(file_list)  # Sort for consistent order
    
    if not file_list:
        st.error(f"No files found for pattern: {media_path}")
        return

    # Session state for navigation
    if "media_index" not in st.session_state:
        st.session_state.media_index = 0

    total_files = len(file_list)
    current_file = file_list[st.session_state.media_index]
    file_ext = os.path.splitext(current_file)[-1].lower()

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
            .nav-buttons {{
                display: flex;
                justify-content: center;
                margin-top: 5px;
                gap: 10px;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Render media
    with st.container():
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            st.image(current_file, use_container_width=True)

        elif file_ext in ['.mp4', '.avi', '.mov', '.webm']:
            st.video(current_file)

        elif file_ext == '.html':
            try:
                with open(current_file, 'r') as file:
                    html_content = file.read()
                components.html(html_content, width=int(width.replace("px", "")), height=int(height.replace("px", "")))
            except Exception as e:
                st.error(f"Error loading HTML content: {str(e)}")

        else:
            st.error(f"Unsupported media type: {file_ext}")

    # Navigation buttons if multiple files exist
    if total_files > 1:
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ Previous", key="prev_media"):
                st.session_state.media_index = (st.session_state.media_index - 1) % total_files
                st.experimental_rerun()
        with col2:
            if st.button("Next ➡️", key="next_media"):
                st.session_state.media_index = (st.session_state.media_index + 1) % total_files
                st.experimental_rerun()
        
        st.caption(f"Media {st.session_state.media_index + 1} of {total_files}")

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

