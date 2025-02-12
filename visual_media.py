import streamlit as st
import streamlit.components.v1 as components
import os
import glob

# Create a persistent placeholder outside the function
if "media_placeholder" not in st.session_state:
    st.session_state.media_placeholder = st.empty()  # Stores the placeholder reference

def render_item_visual_content(title, description, media_path, width="700px", height="400px"):
    """
    Render visual content based on metadata with minimal spacing.
    Supports images, videos, and HTML with navigation.
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

    # Use the persistent placeholder
    with st.session_state.media_placeholder.container():
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

    # Render navigation buttons
    if total_files > 1:
        nav_buttons = st.columns(total_files)
        for idx, col in enumerate(nav_buttons):
            with col:
                if st.button(f"{idx + 1}", key=f"nav_button_{idx}", use_container_width=True):
                    st.session_state.media_index = idx
                    st.experimental_rerun()

    # Render text section
    st.markdown(
        f"""
        <div style="background: rgba(0,0,0,0.3); padding: 6px; border-radius: 8px; color: white; text-align: center; margin-top: 5px;">
            <span style="font-size: 18px; font-weight: 600;">{title}</span><br>
            <span style="font-size: 14px; font-weight: 400; color: #ddd;">{description}</span>
        </div>
        """,
        unsafe_allow_html=True
    )




