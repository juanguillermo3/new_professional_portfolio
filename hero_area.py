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


# Example data for HeroArea
quote = (
    "Modern data analysis requires engaging with, sometimes developing software, "
    "such as data gathering and processing applications. "
    "Moreover, software automation is key to distributing inferences from statistical analysis, such as insights/predictions. "
    "Bottom line, I recognize the tight dependencies between modern data analysis and application development, "
    "hence my effort to serve both of them unified framework."
)

# Example caption
hero_caption = "God told me I could either be good-looking or an excellent worker."

# Instantiate and render HeroArea
hero = HeroArea(quote=quote, avatar_image="jg_pick.jpg", avatar_caption=hero_caption)



