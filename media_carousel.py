import streamlit as st
import time
import threading

class MediaCarousel:
    def __init__(self, media_content, session_key=None, update_interval=None):
        self.media_content = media_content
        self.session_key = session_key or f"media_carousel_{id(self)}"
        self.update_interval = update_interval  # Interval in seconds for auto-update
        
        # Initialize session state for carousel index
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = 0

    def next_item(self):
        """Navigate to the next item."""
        st.session_state[self.session_key] = (st.session_state[self.session_key] + 1) % len(self.media_content)

    def previous_item(self):
        """Navigate to the previous item."""
        st.session_state[self.session_key] = (st.session_state[self.session_key] - 1) % len(self.media_content)

    def start_auto_update(self):
        """Start automatic updates in a separate thread."""
        if self.update_interval:
            def update_loop():
                while True:
                    time.sleep(self.update_interval)
                    self.next_item()
                    st.experimental_rerun()

            # Start the thread in daemon mode to run in the background
            threading.Thread(target=update_loop, daemon=True).start()

    def render(self):
        """Render the carousel UI."""
        # Display the current item
        current_index = st.session_state[self.session_key]
        st.write(f"**Item {current_index + 1} of {len(self.media_content)}:**")
        st.write(self.media_content[current_index])
        
        # Navigation buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("◀️ Previous", key=f"{self.session_key}_prev"):
                self.previous_item()
        with col2:
            if st.button("Next ▶️", key=f"{self.session_key}_next"):
                self.next_item()

        # Start the auto-update loop if an interval is specified
        if self.update_interval:
            self.start_auto_update()

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
