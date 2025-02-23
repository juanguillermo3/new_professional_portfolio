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
    DATA_VERIFIED = False  # Controls both the mocked data message and the verified badge
    
    def __init__(self, title: str, description: str):
        """
        Initialize the portfolio section with a title and description.

        :param title: The section title.
        :param description: The section description.
        """
        self.title = title
        self.description = description

    @staticmethod
    def _render_title_with_badge(title: str, verified: bool):
        """
        Renders the given title with a subtle verified badge beside it.

        :param title: The section title to be displayed.
        :param verified: Whether the section data has been verified.
        """
        if verified:
            badge_html = (
                '<span style="font-size: 0.92em; background: #28a745; color: white; padding: 4px 9px; '
                'border-radius: 10px; margin-left: 10px; cursor: pointer;" '
                'title="✅ This section has been reviewed for accuracy and does not contain AI-generated content.">'
                '✔ Verified</span>'
            )
            st.markdown(f"### {title} {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"### {title}", unsafe_allow_html=True)

    @staticmethod
    def _render_title_with_badge(title: str, verified: bool):
        """
        Renders the given title with a subtle verified badge below it.

        :param title: The section title to be displayed.
        :param verified: Whether the section data has been verified.
        """
        # Render the title
        st.markdown(f"### {title}", unsafe_allow_html=True)

        # Render a small badge below the title, only if verified
        if verified:
            st.markdown(
                '<p style="font-size: 0.75em; background: #28a745; color: white; display: inline-block; '
                'padding: 2px 6px; border-radius: 6px; margin-top: -8px; cursor: help;" '
                'title="The information in this section is verified and does not contain AI-generated content.">'
                '✅ Verified Section</p>',
                unsafe_allow_html=True
            )
            
    def _render_headers(self):
        """Render the section, including the title with a badge, description, and optional messages."""
        self._render_title_with_badge(self.title, self.DATA_VERIFIED)  # Uses class attribute automatically
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

