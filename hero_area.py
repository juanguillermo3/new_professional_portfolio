import streamlit as st


class HeroArea:
    def __init__(self, quote: str, avatar_image: str = None, avatar_caption: str = ""):
        """
        Initialize the HeroArea class with a focus on a quote-styled main statement.
        :param quote: Main statement or quote to display as a single paragraph.
        :param avatar_image: File name of the avatar image to display.
        :param avatar_caption: Caption for the avatar image.
        """
        self.quote = quote
        self.avatar_image = avatar_image
        self.avatar_caption = avatar_caption

    def render(self):
        """
        Render the Hero area in Streamlit.
        """
        # Two-column layout for quote and avatar
        col1, col2 = st.columns([2, 1])

        # Render the quote
        with col1:
            st.markdown("""
            <style>
            .hero-quote {
                font-size: 1.2em;
                line-height: 1.8;
                margin: 0 auto;
                text-align: justify;
                color: #333333;
            }
            </style>
            """, unsafe_allow_html=True)

            # Render the quote as a single justified paragraph
            st.markdown(f'<p class="hero-quote">{self.quote}</p>', unsafe_allow_html=True)

        # Render the avatar with caption
        if self.avatar_image:
            with col2:
                st.image(f"assets/{self.avatar_image}", caption=self.avatar_caption, use_container_width=True)


class ProfessionalBio:
    def __init__(self, bio_pic, bio, skills, avatar_caption: str = ""):
        """
        Initialize the ProfessionalBio class.
        :param bio_pic: The file name of the picture to be referenced from the assets folder (e.g., 'profile.png').
        :param bio: A dictionary where keys are headers and values are markdown formatted strings.
        :param skills: A list of key differentiators and technical skills.
        :param avatar_caption: Caption for the bio picture.
        """
        self.picture_url = f'assets/{bio_pic}'  # Reference image from the assets folder
        self.bio = bio
        self.skills = skills
        self.avatar_caption = avatar_caption

    def render_layout(self):
        """
        Render the professional bio layout with a picture and bio sections.
        """
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(
                """
                <style>
                .rounded-image img {
                    border-radius: 50%;
                    width: 200px;
                    height: 200px;
                    object-fit: cover;
                }
                </style>
                """, unsafe_allow_html=True
            )
            st.image(self.picture_url, caption=self.avatar_caption, use_container_width=False)

        with col2:
            for header, content in self.bio.items():
                st.subheader(header)
                st.markdown(content, unsafe_allow_html=True)

            if self.skills:
                st.subheader("Skills")
                st.markdown("\n".join([f"- {skill}" for skill in self.skills]))


# Example data for HeroArea and ProfessionalBio
quote = (
    "Modern data analysis requires engaging with, sometimes developing software applications, "
    "such as data gathering and processing services. "
    "Moreover, software automation is key to distributing inferences from statistical analysis. "
    "Bottom line, I recognize the tight dependencies between data analysis and application development, "
    "hence my effort to offer data analysis and software analysis within a unified framework."
)


# Example captions
hero_caption = "God told me I could either be good-looking or an excellent worker. Guess which one I chose?"

# Instantiate components
hero = HeroArea(quote=quote, avatar_image="jg_pick.jpg", avatar_caption=hero_caption)


