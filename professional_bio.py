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
                .bio-container {
                    border-radius: 20px; /* Rounded corners for the container */
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Shadow effect */
                    padding: 20px;
                    background-color: #ffffff;
                }
                </style>
                """, unsafe_allow_html=True
            )
            # Apply container with shadow and rounded borders
            st.markdown('<div class="bio-container">', unsafe_allow_html=True)
            st.markdown('<div class="centered-image rounded-image">', unsafe_allow_html=True)
            st.image(self.picture_url, caption="Profile Picture", use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Render the bio content inside the container
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
bio_component.render_layout()



