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

        # Picture section (Instagram-like circular photo)
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(self.picture_url, caption="Profile Picture", use_container_width=True, width=200)
        
        with col2:
            for section in bio_sections:
                st.markdown(section)

# Example usage
bio = {
    "Name": "John Doe",
    "Profession": "Software Engineer",
    "Experience": "Over 10 years of experience in web development and data science.",
    "Hobbies": "Cycling, Reading, Traveling"
}

# Initialize ProfessionalBio object
bio_component = ProfessionalBio(bio_pic="jg_pick.jpg", bio=bio, skills=[])