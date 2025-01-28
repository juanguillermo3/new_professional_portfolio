import os
import glob
import streamlit as st
import time
import streamlit.components.v1 as components

import os
import glob
import time
import streamlit as st
import json
from streamlit import components

class MediaCarousel:
    def __init__(self, media_content, session_key=None, update_interval=None):
        """
        Initializes the carousel.
        
        :param media_content: Either a list of media content (strings or URLs) or a path to a folder of media files.
        :param session_key: The key for session state to store the current index (optional).
        :param update_interval: Time interval (in seconds) for automatic updates (optional).
        """
        self.session_key = session_key or f"media_carousel_{id(self)}"
        self.update_interval = update_interval  # Interval in seconds for auto-update
        
        # Handle media content based on type (list or folder path)
        if isinstance(media_content, list):
            self.media_content = media_content  # Use directly if it's a list
        elif os.path.isdir(media_content):
            # Load files from the folder if media_content is a folder path
            self.media_content = self.load_media_from_folder(media_content)
        else:
            raise ValueError("media_content should be a list of media items or a valid folder path.")
        
        # Load metadata if available
        self.metadata = {}
        metadata_file = os.path.join(media_content, 'media_metadata.json') if isinstance(media_content, str) else None
        if metadata_file and os.path.exists(metadata_file):
            with open(metadata_file, 'r') as file:
                self.metadata = json.load(file)
        
        # Initialize the index in the session state if not already initialized
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = 0
        
        # The index will be tracked by the instance variable
        self.index = st.session_state[self.session_key]

    def load_media_from_folder(self, folder_path):
        """
        Loads media files from a folder.
        
        :param folder_path: The path to the folder containing media files (e.g., images, videos).
        :return: A list of media file paths.
        """
        # Define the types of files to be considered media (you can expand this list)
        media_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.mp4', '*.avi', '*.html']
        media_files = []
        
        for ext in media_extensions:
            media_files.extend(glob.glob(os.path.join(folder_path, ext)))
        
        # Sort the files for consistent order
        media_files.sort()
        
        return media_files

    def next_item(self):
        """Navigate to the next item."""
        self.index = (self.index + 1) % len(self.media_content)
        st.session_state[self.session_key] = self.index

    def previous_item(self):
        """Navigate to the previous item."""
        self.index = (self.index - 1) % len(self.media_content)
        st.session_state[self.session_key] = self.index

    def start_auto_update(self):
        """Handle periodic updates in the app loop."""
        if self.update_interval:
            # Time tracking for auto-update
            last_update_time = st.session_state.get(f"{self.session_key}_last_update", time.time())
            current_time = time.time()

            if current_time - last_update_time >= self.update_interval:
                self.next_item()
                # Update the last update time
                st.session_state[f"{self.session_key}_last_update"] = current_time
                st.experimental_rerun()

    def get_caption(self, media_path):
        """
        Retrieves the caption for the current media item from the metadata.
        
        :param media_path: The path of the media file.
        :return: A string caption if found, otherwise an empty string.
        """
        filename = os.path.basename(media_path)
        return self.metadata.get(filename, {}).get("caption", "")

    def parse_media(self, media_path):
        """
        Parses media based on file extension and returns appropriate HTML or Streamlit format.
        
        :param media_path: The path of the media file.
        :return: Streamlit-compatible media rendering command.
        """
        _, ext = os.path.splitext(media_path)
        ext = ext.lower()
        
        # Get caption from metadata
        caption = self.get_caption(media_path)

        # Render image or video
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            # Render image with aspect ratio preserved
            img = st.image(media_path, use_container_width=True)
            if caption:
                st.markdown(f"<p style='font-size: 12px; color: #888;'>{caption}</p>", unsafe_allow_html=True)
        elif ext in ['.mp4', '.avi']:
            # Render video with autoplay, muted, and looping
            video = st.video(media_path, loop=True, autoplay=True, muted=True)
            if caption:
                st.markdown(f"<p style='font-size: 12px; color: #888;'>{caption}</p>", unsafe_allow_html=True)
        elif ext == '.html':
            # Render HTML content with embedded JavaScript or dynamic elements
            with open(media_path, 'r') as file:
                html_content = file.read()
            components.html(html_content, height=600)
        else:
            # Fallback: Display the file path if unsupported format
            return st.write(media_path)

    def render(self):
        """Render the carousel UI."""
        # Automatically update if the interval is set
        self.start_auto_update()

        # Display the current item
        st.write(f"**Item {self.index + 1} of {len(self.media_content)}:**")
        
        # Call the parse_media function to render based on file type
        self.parse_media(self.media_content[self.index])
        
        # Custom CSS to style the buttons and center them vertically
        st.markdown("""
            <style>
            .stButton>button {
                background-color: #e0e0e0;
                color: #333;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                width: 100%;
                box-sizing: border-box;
            }
            .stButton>button:hover {
                background-color: #d6d6d6;
            }
            .stColumn {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Navigation buttons with centered alignment
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("◀️ Previous", key=f"{self.session_key}_prev"):
                self.previous_item()
        with col2:
            if st.button("Next ▶️", key=f"{self.session_key}_next"):
                self.next_item()


# Example media content
media_items = [
    "https://via.placeholder.com/800x400.png?text=Image+1",
    "https://via.placeholder.com/800x400.png?text=Image+2",
    "https://www.w3schools.com/html/mov_bbb.mp4",
    "This is a raw HTML or text fallback."
]

# Initialize the carousel with a 5-second auto-update interval
#carousel = MediaCarousel(media_items, session_key="example_carousel", update_interval=5)

#carousel.render()
