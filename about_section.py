import streamlit as st
from about_section_data_loader import load_general_info, load_key_interest, load_key_hypothesis, load_dev_environment
from portfolio_section import PortfolioSection

class AboutSection(PortfolioSection):

    EARLY_DEVELOPMENT_STAGE = False  
    DATA_VERIFIED = True  

    def __init__(self, linkedin_profile):
        """
        Ensure AboutSection inherits and overrides class-level defaults.
        """
        super().__init__(
            title="About this portfolio 💡",
            description=load_general_info(),
            verified=self.DATA_VERIFIED,
            early_dev=self.EARLY_DEVELOPMENT_STAGE,
            ai_content=not self.DATA_VERIFIED
        )
        self.linkedin_profile = linkedin_profile

    def render(self):
        """Render the about section following the standard pattern."""
        self._render_headers()
        st.markdown(load_key_interest(), unsafe_allow_html=True)
        st.markdown(load_key_hypothesis().format(linkedin=self.linkedin_profile), unsafe_allow_html=True)
        st.markdown(load_dev_environment(), unsafe_allow_html=True)

# Instantiation
about = AboutSection(linkedin_profile="https://www.linkedin.com/in/juan-guillermo-osio/")


# Instantiation
about = AboutSection()

