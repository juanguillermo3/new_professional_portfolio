import streamlit as st

class HeroArea:
    def __init__(self, headline: str, subheading: str, cta_text: str, cta_link: str,
                 background_image: str = None, avatar_image: str = None, layout: str = "center",
                 colab_portfolio: list = None):
        """
        Initialize the HeroArea class with relevant parameters for rendering.
        """
        self.headline = headline
        self.subheading = subheading
        self.cta_text = cta_text
        self.cta_link = cta_link
        self.background_image = background_image  # URL or path to image
        self.avatar_image = avatar_image  # URL or path to avatar image
        self.layout = layout  # "center", "left", "right", or "full"
        self.colab_portfolio = colab_portfolio or []  # List of dictionaries with Colab projects

    def render(self):
        """
        Renders the Hero area in Streamlit, including text, CTA, visual elements, and Colab portfolio grid.
        """
        # Set the background if provided using st.markdown for custom HTML and CSS
        if self.background_image:
            st.markdown(f"""
            <style>
            .hero-background {{
                background-image: url({self.background_image});
                background-size: cover;
                background-position: center center;
                height: 60vh;
                display: flex;
                align-items: center;
                justify-content: {self.layout};
                color: white;
                padding: 20px;
            }}
            </style>
            """, unsafe_allow_html=True)
        
        # Render the headline and subheading using st.markdown
        st.markdown(f"## {self.headline}")
        st.markdown(f"### {self.subheading}")
        
        # Optionally, render an avatar or image if provided using st.image
        if self.avatar_image:
            st.image(self.avatar_image, width=120, use_container_width=True)

        # Call to action (CTA) as a clickable link
        if self.cta_text and self.cta_link:
            st.markdown(f"[{self.cta_text}]({self.cta_link})", unsafe_allow_html=True)

        # Render Colab portfolio grid
        if self.colab_portfolio:
            st.markdown(
                """
                <style>
                .colab-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                }
                .colab-button {
                    background-color: #F4B400;
                    color: white;
                    padding: 10px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    text-align: center;
                    display: block;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('<div class="colab-grid">', unsafe_allow_html=True)
            for project in self.colab_portfolio:
                title = project.get("title", "View Project")
                url = project.get("url", "#")
                st.markdown(
                    f"""
                    <a href="{url}" target="_blank" class="colab-button">{title}</a>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        # Add some spacing and style adjustments
        st.markdown("<br>", unsafe_allow_html=True)
