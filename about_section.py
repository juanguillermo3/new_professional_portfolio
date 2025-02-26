import streamlit as st
from portfolio_section import PortfolioSection
from about_section_data_loader import load_general_info, load_key_interest, load_key_hypothesis, load_dev_environment
from about_section_data_loader import (
    load_general_info, 
    load_key_interest, 
    load_key_hypothesis, 
    load_dev_environment
)

class AboutSection(PortfolioSection):

    EARLY_DEVELOPMENT_STAGE = False  # Override class defaults for this section
    DATA_VERIFIED = True  

    def __init__(self):
        """
        Ensure AboutSection inherits and overrides class-level defaults.
        """
        super().__init__(
            title="About this portfolio 💡",
            description=load_general_info(),
            verified=self.DATA_VERIFIED,  # Use subclass defaults
            early_dev=self.EARLY_DEVELOPMENT_STAGE,
            ai_content=not self.DATA_VERIFIED  # This ensures consistency
        )

    def render(self):
        """Render the about section following the standard pattern."""
        self._render_headers()
        st.markdown(load_key_interest(), unsafe_allow_html=True)
        st.markdown(load_key_hypothesis(), unsafe_allow_html=True)
        st.markdown(load_dev_environment(), unsafe_allow_html=True)

# Instantiation
about = AboutSection()



# Instantiation
about = AboutSection()

