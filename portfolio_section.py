import streamlit as st

class PortfolioSection:
    """
    A base class for portfolio sections, providing common rendering behavior.
    
    This class allows different sections of the portfolio to inherit a standard structure, 
    including a title, a horizontal separator, and a description with a consistent grayish style. 
    
    Subclasses can extend this functionality by adding specific content while keeping the 
    default layout intact.
    """

    DESCRIPTION_STYLE = "color: gray;"
    EARLY_DEVELOPMENT_STAGE = True  # Override this in subclasses if the section is complete
    MOCKED_DATA_NOTICE = True  # Override this in subclasses if data is real

    def __init__(self, title: str, description: str):
        """
        Initialize the portfolio section with a title and description.

        :param title: The section title.
        :param description: The section description.
        """
        self.title = title
        self.description = description

    @staticmethod
    def _get_title_with_badge(title: str, verified: bool) -> str:
        """
        Returns the title with an optional verified badge if the section is marked as verified.
        
        This is a static method to facilitate integration with older sections.
        
        :param title: The section title.
        :param verified: Whether the data is verified.
        :return: The formatted title with or without a badge.
        """
        if verified:
            badge_html = (
                '<span style="font-size: 0.8em; background: #28a745; color: white; padding: 3px 8px; '
                'border-radius: 12px; cursor: help;" title="This section has been checked and mostly contains accurate data.">'
                '✅ Verified</span>'
            )
            return f"{title} {badge_html}"
        return title

    def _render_headers(self):
        """Render the standard headers: title, horizontal rule, and description."""
        st.subheader(self._get_title_with_badge(self.title, self.DATA_VERIFIED))
        st.markdown("---")
        st.markdown(f'<p style="{self.DESCRIPTION_STYLE}">{self.description}</p>', unsafe_allow_html=True)

    def _render_messages(self):
        """Render housekeeping messages, such as warnings for unfinished sections."""
        if self.EARLY_DEVELOPMENT_STAGE:
            st.warning("🚧 This is a new section we are working on. Content may be incomplete.")

        if not self.DATA_VERIFIED:
            st.info("🤖 This section is still being reviewed and may contain AI-generated or placeholder data.")

    def render(self):
        """Render the section, including standard headers and optional messages."""
        self._render_headers()  # Render title, rule, and description
        self._render_messages()  # Render any section-specific messages

