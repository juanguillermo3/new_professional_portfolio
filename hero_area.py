import streamlit as st

class HeroArea:
    def __init__(self, quote: str, author: str = ""):
        """
        Initialize the HeroArea class with a focus on a subtle, quote-styled main statement.
        """
        self.quote = quote
        self.author = author

    def render(self):
        """
        Render the subtle Hero area as a quote.
        """
        st.markdown("""
        <style>
        .hero-quote {
            font-style: italic;
            font-size: 1.5em;
            line-height: 1.8;
            margin: 0 auto;
            max-width: 800px;
            text-align: center;
            color: #333333;
        }
        .hero-author {
            font-size: 1em;
            margin-top: 10px;
            text-align: center;
            color: gray;
        }
        </style>
        """, unsafe_allow_html=True)

        # Render the quote
        st.markdown(f'<p class="hero-quote">"{self.quote}"</p>', unsafe_allow_html=True)

        # Render the author if provided
        if self.author:
            st.markdown(f'<p class="hero-author">— {self.author}</p>', unsafe_allow_html=True)

# Example usage of HeroArea

hero = HeroArea(
    quote=(
        "Modern data analysis requires engaging with, sometimes developing software applications, "
        "such as data gathering and processing services. Moreover, software automation is key to "
        "distributing inferences from statistical analysis. Bottom line, I recognize the tight "
        "dependencies between data analysis and application development, hence my effort to offer "
        "data analysis and software analysis within a unified framework."
    ),
    author=""
)



