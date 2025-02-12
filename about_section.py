import streamlit as st

import streamlit as st
from about_section_data_loader import load_general_info

class AboutSection:
    SECTION_HEADER = "About this portfolio 💡"
    KEY_HYPOTHESIS = """
    🔬 Ongoing research explores leveraging emerging technologies like Recommendation Systems (RecSys) 
    and LLM-powered applications (LLM apps) to create practical software solutions for professionals. 
    One key area of interest is efficiently displaying content to potential clients or employers. 
    Features such as the RecSys are still under development, and related research can be found on my 
    <a href="{linkedin}" target="_blank" style="color: #1f77b4; text-decoration: none;">LinkedIn profile</a>. 
    Some content is AI-generated for developmental purposes.
    """

    def __init__(self, linkedin_profile):
        self.linkedin_profile = linkedin_profile
        self.general_info = load_general_info()

    def render(self):
        """Render the about section following the standard pattern."""
        st.subheader(self.SECTION_HEADER)
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.general_info}</p>', unsafe_allow_html=True)

        # Display research hypothesis
        st.markdown(self.KEY_HYPOTHESIS.format(linkedin=self.linkedin_profile), unsafe_allow_html=True)

# Instantiation
about = AboutSection(linkedin_profile="https://www.linkedin.com/in/juan-guillermo-osio/")

