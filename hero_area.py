import streamlit as st

class HeroArea:
    def __init__(self, quote, author: str = "", background_image: str = None):
        """
        Initialize the HeroArea class with a focus on a subtle, quote-styled main statement.
        :param quote: Single string or list of strings (each interpreted as a paragraph).
        :param author: Optional author name for the quote.
        :param background_image: Optional background image for styling.
        """
        self.quote = quote if isinstance(quote, list) else [quote]  # Ensure it's a list, even if passed as a single string
        self.author = author
        self.background_image = background_image  # Optional background image for styling

    def render(self):
        """
        Render the subtle Hero area as a quote with optional background.
        """
        # Apply background styling if a background image is provided
        if self.background_image:
            st.markdown(f"""
            <style>
            .hero-background {{
                background-image: url({self.background_image});
                background-size: cover;
                background-position: center;
                height: 50vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                text-align: center;
                padding: 20px;
            }}
            .hero-quote {{
                font-style: italic;
                font-size: 1.5em;
                line-height: 1.8;
                margin: 0 auto;
                max-width: 800px;
            }}
            .hero-author {{
                font-size: 1em;
                margin-top: 10px;
                color: rgba(255, 255, 255, 0.8);
            }}
            </style>
            """, unsafe_allow_html=True)
            st.markdown('<div class="hero-background">', unsafe_allow_html=True)
        else:
            st.markdown("""
            <style>
            .hero-quote {{
                font-style: italic;
                font-size: 1.5em;
                line-height: 1.8;
                margin: 0 auto;
                max-width: 800px;
                text-align: center;
            }}
            .hero-author {{
                font-size: 1em;
                margin-top: 10px;
                text-align: center;
                color: gray;
            }}
            </style>
            """, unsafe_allow_html=True)
            st.markdown('<div>', unsafe_allow_html=True)

        # Render the quote (each paragraph will be a separate <p> tag)
        for paragraph in self.quote:
            st.markdown(f'<p class="hero-quote">"{paragraph}"</p>', unsafe_allow_html=True)

        # Render the author if provided
        if self.author:
            st.markdown(f'<p class="hero-author">— {self.author}</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# Example usage of HeroArea
hero = HeroArea(
    quote=(
        "Modern data analysis requires engaging with, sometimes developing software applications, "
        "such as data gathering and processing services. Moreover, software automation is key to "
        "distributing inferences from statistical analysis. Bottom line, I recognize the tight "
        "dependencies between data analysis and application development, hence my effort to offer "
        "data analysis and software analysis within a unified framework."
    ),
    author="",
    background_image="jg_pick.jpg"  # Optional background image
)



