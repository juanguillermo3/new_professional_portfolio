import streamlit as st
from about_section_data_loader import load_general_info
from portfolio_section import PortfolioSection

class AboutSection(PortfolioSection):

    EARLY_DEVELOPMENT_STAGE = False  # Override this in subclasses if the section is complete
    DATA_VERIFIED = True  # Controls both the mocked data message and the verified badge
    
    KEY_HYPOTHESIS = """
    🔬 Ongoing research explores leveraging emerging technologies like Recommendation Systems (RecSys) 
    and LLM-powered applications (LLM apps) to create practical software solutions for professionals. 
    One key area of interest is efficiently displaying content to potential clients or employers. 
    Features such as the RecSys are still under development, and related research can be found on my 
    <a href="{linkedin}" target="_blank" style="color: #1f77b4; text-decoration: none;">LinkedIn profile</a>. 
    """

    DEV_ENVIRONMENT = """
    🛠️ This portfolio is a Python/Streamlit web application with a modular design inspired by microservice 
    architecture, adapted for a professional site. It follows OOP principles and SOLID design patterns, 
    with modules organized by responsibility. The full codebase is available on 
    <a href="https://github.com/juanguillermo3/new_professional_portfolio/tree/main" 
    target="_blank" style="color: #1f77b4; text-decoration: none;">GitHub</a>. 
    """

    def __init__(self, linkedin_profile):
        self.image_path="assets/about_section_theme.jpg"
        self.title="About this portfolio 💡"
        self.description = load_general_info()
        self.linkedin_profile = linkedin_profile

    def render(self):
        """Render the about section following the standard pattern."""
        
        self._render_headers()

        # Display research hypothesis
        st.markdown(self.KEY_HYPOTHESIS.format(linkedin=self.linkedin_profile), unsafe_allow_html=True)

        # Add break line and display development environment info
        st.markdown(self.DEV_ENVIRONMENT, unsafe_allow_html=True)


# Instantiation
about = AboutSection(linkedin_profile="https://www.linkedin.com/in/juan-guillermo-osio/")

