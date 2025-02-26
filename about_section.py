import streamlit as st
from about_section_data_loader import load_general_info
from portfolio_section import PortfolioSection


class AboutSection(PortfolioSection):

    EARLY_DEVELOPMENT_STAGE = False  # Override class defaults for this section
    DATA_VERIFIED = True  

    KEY_INTEREST = """
    🔑 My recurring interest nevertheless has always been the modernization of the data analysis pipeline
    through cutting-edge techniques, such as flexible ML-based inference, software and algorithmic automation,
    using NLP in latent semantic spaces, and, more recently, solving data analysis tasks through agency formation
    within LLM applications.
    """
    
    KEY_HYPOTHESIS = """
    🔬 Ongoing research explores leveraging emerging technologies like Recommendation Systems (RecSys) 
    and LLM-powered applications (LLM apps) to create practical software solutions for professionals. 
    One key area of interest is efficiently displaying content to potential clients or employers. 
    Features such as the RecSys are still under development, and related research can be found on my 
    <a href="https://www.linkedin.com/in/juan-guillermo-osio/" target="_blank" 
    style="color: #1f77b4; text-decoration: none;">LinkedIn profile</a>. 
    """

    DEV_ENVIRONMENT = """
    🛠️ This portfolio is a Python/Streamlit web application with a modular design inspired by microservice 
    architecture, adapted for a professional site. It follows OOP principles and SOLID design patterns, 
    with modules organized by responsibility. The full codebase is available on 
    <a href="https://github.com/juanguillermo3/new_professional_portfolio/tree/main" 
    target="_blank" style="color: #1f77b4; text-decoration: none;">GitHub</a>. 
    """

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
        st.markdown(self.KEY_INTEREST, unsafe_allow_html=True)
        st.markdown(self.KEY_HYPOTHESIS, unsafe_allow_html=True)
        st.markdown(self.DEV_ENVIRONMENT, unsafe_allow_html=True)

# Instantiation
about = AboutSection()

