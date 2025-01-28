import streamlit as st
import time
import threading

import streamlit as st
import time

import streamlit as st
import time

class MediaCarousel:
    def __init__(self, media_content, session_key=None, update_interval=None):
        self.media_content = media_content
        self.session_key = session_key or f"media_carousel_{id(self)}"
        self.update_interval = update_interval  # Interval in seconds for auto-update
        # Initialize the index in the session state if not already initialized
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = 0
        
        # The index will be tracked by the instance variable
        self.index = st.session_state[self.session_key]

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

    def render(self):
        """Render the carousel UI."""
        # Automatically update if the interval is set
        self.start_auto_update()

        # Display the current item
        st.write(f"**Item {self.index + 1} of {len(self.media_content)}:**")
        st.write(self.media_content[self.index])
        
        # Navigation buttons
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
carousel = MediaCarousel(media_items, session_key="example_carousel", update_interval=5)

#carousel.render()
