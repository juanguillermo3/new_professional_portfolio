import streamlit as st

class HeroArea:
    def __init__(self, quote, avatar_image: str = None, avatar_caption: str = "", code_samples: list = None, code_samples_intro: str = "Explore the code samples below:"):
        """
        Initialize the HeroArea class with a focus on a quote-styled main statement.
        :param quote: Main statement or quote to display as a single string or list of strings (paragraphs).
        :param avatar_image: File name of the avatar image to display.
        :param avatar_caption: Caption for the avatar image.
        :param code_samples: List of dictionaries with 'title' and 'url' for code sample links.
        :param code_samples_intro: Introductory text to display above the code samples.
        """
        self.quote = quote if isinstance(quote, list) else [quote]
        self.avatar_image = avatar_image
        self.avatar_caption = avatar_caption
        self.code_samples = code_samples if code_samples is not None else [
            {"title": "Sample 1", "url": "https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz"},
            {"title": "Sample 2", "url": "https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvAO"}
        ]
        self.code_samples_intro = code_samples_intro

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

            .hero-avatar-container {
                display: flex;
                justify-content: center; /* Center horizontally */
                align-items: center; /* Center vertically */
                height: 100%;  /* Ensure the container takes the full height of the column */
            }

            .code-samples-intro {
                font-size: 1em;
                color: #555555;
                text-align: center;
                margin-bottom: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

            # Render each paragraph separately in the quote
            for paragraph in self.quote:
                st.markdown(f'<p class="hero-quote">{paragraph}</p>', unsafe_allow_html=True)

        # Render the avatar with caption
        if self.avatar_image:
            with col2:
                st.markdown('<div class="hero-avatar-container">', unsafe_allow_html=True)
                st.image(f"assets/{self.avatar_image}", caption=self.avatar_caption, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # Render the code samples (buttons) with intro
        self.render_code_samples()

    def render_code_samples(self):
        """
        Render code sample buttons as GitHub-styled buttons with an introductory text.
        """
        # Display the introductory text
        st.markdown(f'<p class="code-samples-intro">{self.code_samples_intro}</p>', unsafe_allow_html=True)
        
        # Create a grid layout for the buttons
        st.markdown("<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px;'>", unsafe_allow_html=True)
        
        for sample in self.code_samples:
            # Create GitHub-styled button for each code sample
            st.markdown(f"""
            <a href="{sample['url']}" target="_blank">
                <button style="
                    background-color: #24292f; 
                    color: white; 
                    border: 1px solid white; 
                    padding: 10px 20px; 
                    font-size: 14px; 
                    border-radius: 5px;
                    text-align: center;
                    width: 100%;
                ">{sample['title']}</button>
            </a>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)



# Example data for HeroArea with multiple paragraphs in the quote and code sample links
quote = [
    "Modern data analysis requires engaging with substantial software, such as data gathering and information processing applications. "
    "Moreover, software automation is key to distributing inferences from statistical analysis, such as insights from econometric analysis "
    "or predictions from machine learning models. Bottom line, I recognize the tight dependencies between data analysis and software development, "
    "hence my effort to serve both within a unified framework."
    "",
    "I am Juan Guillermo. I am a professional economist. I have made a living developing data analysis and application "
    "development scripts. My larger professional project aims for a holistic vision, interconnecting all the tooling for modern data analysis, "
    "comprising data mining and artificial intelligence models, algorithms, workflows, and information tools."
]


hero_caption = "God told me I could either be good-looking or an excellent worker."

# Instantiate and render HeroArea with code samples
hero = HeroArea(quote=quote, avatar_image="jg_pick.jpg", avatar_caption=hero_caption,  code_samples_intro="As an easy entry-point to my work, you can check these selected code samples from my ML consultancies:")
#hero.render()





