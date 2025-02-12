

import streamlit as st
import streamlit.components.v1 as components
import os
import glob

def parse_media_content(media_path, width="700px", height="400px"):
    """
    Render media content based on the file type (image, video, HTML).
    This function is responsible for parsing and rendering the appropriate media.
    """
    file_ext = os.path.splitext(media_path)[-1].lower()

    # Render media
    with st.container():
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            st.image(media_path, use_container_width=True)  # ✅ Fixed: Replaced deprecated `use_column_width`

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


def render_item_visual_content(title, description, media_path, width="700px", height="400px"):
    """
    Render visual content based on metadata with minimal spacing. Supports images, videos, and HTML.
    Allows navigation between multiple media files matched by a glob pattern using numbered buttons.
    
    This function:
    1. Resolves a file path pattern (supports glob patterns) to a list of media files.
    2. Displays a single media item at a time, such as an image, video, or HTML.
    3. Provides numbered buttons for navigation to jump directly to any media file.
    4. Uses Streamlit session state to track the current media index and enable navigation.
    5. Renders text metadata (title and description) with a styled minimal layout.
    """
    
    # Resolve file paths (first time media_path gets registered in session_state)
    if "file_list" not in st.session_state:
        file_list = glob.glob(media_path) if '*' in media_path or '?' in media_path else [media_path]
        file_list = sorted(file_list)  # Sort for consistent order
        st.session_state.file_list = file_list

    file_list = st.session_state.file_list
    
    if not file_list:
        st.error(f"No files found for pattern: {media_path}")
        return

    # Session state for navigation
    if "media_index" not in st.session_state:
        st.session_state.media_index = 0

    total_files = len(file_list)
    current_file = file_list[st.session_state.media_index]

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
                margin-top: 10px;
                gap: 5px;
            }}
            .nav-button {{
                background-color: navy;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 5px;
                cursor: pointer;
            }}
            .nav-button:hover {{
                background-color: darkblue;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Render the current media item
    parse_media_content(current_file, width, height)

    # Render navigation buttons as a grid of numbered buttons
    if total_files > 1:
        nav_buttons = st.columns(total_files)
        for idx, col in enumerate(nav_buttons):
            with col:
                if st.button(f"{idx + 1}", key=f"nav_button_{idx}"):
                    st.session_state.media_index = idx
                    parse_media_content(file_list[st.session_state.media_index], width, height)
                    break  # No need for rerun; the content gets updated directly

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


