import streamlit as st

class ProfessionalBio:
    def __init__(self, bio_pic, bio, skills):
        """
        :param bio_pic: The file name of the picture to be referenced from the assets folder (e.g., 'profile.png').
        :param bio: A dictionary where keys are headers and values are markdown formatted strings.
        :param skills: A list of key differentiators and technical skills (not displayed currently).
        """
        self.picture_url = f'assets/{bio_pic}'  # Reference image from the assets folder
        self.bio = bio
        self.skills = skills  # Skills are kept in the signature but not used in layout for now

    def render_layout(self):
        # Bio sections using markdown
        bio_sections = []
        for header, content in self.bio.items():
            bio_sections.append(f"**{header}**")
            bio_sections.append(content)

        # Layout with warning message, picture, and bio content
        st.markdown(
            "⚠️ This is a mock professional bio. The data shown here is for development purposes only.",
            unsafe_allow_html=True
        )

        # Layout with two columns: one for the picture, the other for the bio content
        col1, col2 = st.columns([1, 2])

        with col1:
            # Apply custom CSS to center the image vertically and horizontally with rounded borders
            st.markdown(
                """
                <style>
                .centered-image {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100%;
                }
                .rounded-image img {
                    border-radius: 50%;
                    width: 200px;  /* Adjust image size */
                    height: 200px; /* Ensure the image remains a circle */
                    object-fit: cover; /* Ensures the image is properly cropped */
                }
                .bio-content {
                    max-height: 500px;  /* Set the max height for the bio section */
                    overflow-y: auto;  /* Enable vertical scroll if content exceeds max-height */
                }
                </style>
                """, unsafe_allow_html=True
            )
            st.markdown('<div class="centered-image rounded-image">', unsafe_allow_html=True)
            st.image(self.picture_url, caption="Profile Picture", use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Bio content section with scrolling if overflow occurs
            st.markdown('<div class="bio-content">', unsafe_allow_html=True)
            # Render the bio content
            for section in bio_sections:
                st.markdown(section)
            st.markdown('</div>', unsafe_allow_html=True)

            # Display skills (if any)
            if self.skills:
                st.subheader("Skills")
                st.markdown("\n".join([f"- {skill}" for skill in self.skills]))

# Example usage
bio = {
    "Professional Overview": """
        I am a Colombian Economist with a professional background as a research assistant, 
        remote data analyst, and also as a freelance consultant in the development of Machine Learning technologies. 
        The focus of my current professional offering is on Machine Learning Engineering.
    """,
    "Lines of Service": """
        I excel at statistical analysis and working with data and information more generally. 
        My services include explanatory, counterfactual, predictive, and prescriptive analytics. 
        I can combine applied statistical modeling with algorithm and application development within the Python development ecosystem 
        to transform statistical inference into fully operational software with corporate value - i.e. I create data analysis/machine learning applications. 
        The gist of my professional offering is implementing data analytics and software engineering in a unified framework.
    """
}

# Adding skills to the professional bio
skills = ["Python", "Machine Learning", "Data Analysis", "Software Engineering", "Statistical Modeling"]

# Initialize ProfessionalBio object
bio_component = ProfessionalBio(bio_pic="jg_pick.jpg", bio=bio, skills=skills)
