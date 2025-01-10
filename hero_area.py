import streamlit as st


import streamlit as st


class HeroArea:
    def __init__(self, quote, avatar_image: str = None, avatar_caption: str = ""):
        """
        Initialize the HeroArea class with a focus on a quote-styled main statement.
        :param quote: Main statement or quote to display as a single string or list of strings (paragraphs).
        :param avatar_image: File name of the avatar image to display.
        :param avatar_caption: Caption for the avatar image.
        """
        # Ensure the quote is a list of paragraphs
        self.quote = quote if isinstance(quote, list) else [quote]  # Convert to list if a single string
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
                font-style: italic;
                font-size: 1.5em;
                line-height: 1.8;
                margin: 0 auto;
                max-width: 800px;
                color: #333333;
                text-align: justify;
                padding-bottom: 20px;  /* Add space between paragraphs */
            }
            </style>
            """, unsafe_allow_html=True)

            # Render each paragraph separately in the quote
            for paragraph in self.quote:
                st.markdown(f'<p class="hero-quote">{paragraph}</p>', unsafe_allow_html=True)

        # Render the avatar with caption
        if self.avatar_image:
            with col2:
                st.image(f"assets/{self.avatar_image}", caption=self.avatar_caption, use_container_width=True)


# Example data for HeroArea with multiple paragraphs in the quote
quote = [
    "Modern data analysis requires engaging with, sometimes developing software applications, "
    "such as data gathering and processing services. "
    "Moreover, software automation is key to distributing inferences from statistical analysis. "
    "Bottom line, I recognize the tight dependencies between data analysis and application development, "
    "hence my effort to offer data analysis and software analysis within a unified framework.",
    
    "I am, and always wanted to be, a professional economist. I had made a living of developing data analysis, "
    "machine learning and application development scripts. My larger professional project aims from a holistic vision "
    "interconnecting all the modern tooling for data analysis, including statistical models, algorithms, workflows, "
    "and information tools."
]

# Example caption for the avatar
hero_caption = "God told me I could either be good-looking or an excellent worker."

# Instantiate and render HeroArea
hero = HeroArea(quote=quote, avatar_image="jg_pick.jpg", avatar_caption=hero_caption)




