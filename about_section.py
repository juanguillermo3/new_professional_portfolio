import streamlit as st
from about_section_data_loader import load_general_info

class AboutSection:
    
    DATA_VERIFIED=True
    
    SECTION_HEADER = "About this portfolio 💡"
    
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
        self.linkedin_profile = linkedin_profile
        self.general_info = load_general_info()

    def render(self):
        """Render the about section following the standard pattern."""

        verified_title=self._get_title_with_badge(self.SECTION_HEADER, self.DATA_VERIFIED)  # ✅ Use badge method
        st.subheader(verified_title)
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.general_info}</p>', unsafe_allow_html=True)

        # Display research hypothesis
        st.markdown(self.KEY_HYPOTHESIS.format(linkedin=self.linkedin_profile), unsafe_allow_html=True)

        # Add break line and display development environment info
        st.markdown(self.DEV_ENVIRONMENT, unsafe_allow_html=True)


# Instantiation
about = AboutSection(linkedin_profile="https://www.linkedin.com/in/juan-guillermo-osio/")

