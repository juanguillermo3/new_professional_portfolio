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

    def __init__(self, title: str, description: str):
        """
        Initialize the portfolio section with a title and description.

        :param title: The section title.
        :param description: The section description.
        """
        self.title = title
        self.description = description

    def _render_headers(self):
        """Render the standard headers: title, horizontal rule, and description."""
        st.subheader(self.title)
        st.markdown("---")
        st.markdown(f'<p style="{self.DESCRIPTION_STYLE}">{self.description}</p>', unsafe_allow_html=True)

    def _render_messages(self):
        """Render housekeeping messages, such as warnings for unfinished sections."""
        if self.EARLY_DEVELOPMENT_STAGE:
            st.warning("🚧 We are working on this section. Content may be incomplete.")

    def render(self):
        """Render the section, including standard headers and optional messages."""
        self._render_headers()  # Render title, rule, and description
        self._render_messages()  # Render any section-specific messages
