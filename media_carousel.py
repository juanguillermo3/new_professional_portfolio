import streamlit as st

class MediaCarousel:
    def __init__(self, media_content, session_key="media_carousel"):
        """
        A class to manage a media carousel with button-based navigation.
        
        Args:
            media_content (list): List of media items (image URLs, video URLs, or embed codes).
            session_key (str): Unique session key for managing carousel state.
        """
        self.media_content = media_content
        self.session_key = session_key

        # Initialize session state
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = 0  # Start with the first media item

    def render(self):
        """
        Renders the media carousel with navigation buttons.
        """
        # Get the current index from the session state
        current_index = st.session_state[self.session_key]

        # Display the current media content
        self._display_media(current_index)

        # Render navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("◀️ Previous", key=f"{self.session_key}_prev"):
                self._navigate(-1)
        with col3:
            if st.button("Next ▶️", key=f"{self.session_key}_next"):
                self._navigate(1)

    def _display_media(self, index):
        """
        Displays the media content at the specified index.
        
        Args:
            index (int): Index of the media content to display.
        """
        media_item = self.media_content[index]
        if media_item.endswith((".jpg", ".png", ".jpeg", ".gif")):
            st.image(media_item, use_column_width=True)
        elif media_item.endswith((".mp4", ".webm", ".ogg")):
            st.video(media_item)
        else:
            st.write(media_item)  # Fallback: Display as text or raw HTML

    def _navigate(self, step):
        """
        Updates the session state index to navigate through the carousel.
        
        Args:
            step (int): Step size for navigation (-1 for previous, +1 for next).
        """
        current_index = st.session_state[self.session_key]
        new_index = (current_index + step) % len(self.media_content)  # Circular navigation
        st.session_state[self.session_key] = new_index
