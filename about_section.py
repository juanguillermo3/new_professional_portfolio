import streamlit as st

class AboutSection:
    def __init__(self, linkedin_profile):
        self.linkedin_profile = linkedin_profile

    def render(self):
        st.subheader("About this portfolio 💡")
        st.markdown("---")
        st.markdown(
            f"""
            <p style="color: gray;">
            This portfolio showcases code samples I developed over more than five years as a Data Analyst and Data Mining Engineer across several projects. 
            It is quite eclectic as I am not focused on a single vertical but I hope it's representative of some core workflows I enjoy working in. Moreover, ongoing research aims at leveraging emerging technologies like 
            Recommendation Systems (RecSys) and LLM-powered applications (LLM apps) to create practical software solutions to practical problem of workers at the laboral marketing, such as efficiently displaying content to an audience 
            of potential clients or employers. Features like the RecSys are still under development, and related research can be found on my 
            <a href="{self.linkedin_profile}" target="_blank" style="color: #1f77b4; text-decoration: none;">LinkedIn profile</a>. 
            Some content is AI-generated for developmental purposes.
            </p>
            """,
            unsafe_allow_html=True,
        )

# Instantiation
about_section = AboutSection(linkedin_profile="https://www.linkedin.com/in/juan-guillermo-osio/")
