import streamlit as st

class HeroArea:
    def __init__(self, headline: str, subheading: str, cta_text: str, cta_link: str,
                 background_image: str = None, avatar_image: str = None, layout: str = "center"):
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

    def render(self):
        """
        Renders the Hero area in Streamlit, including text, CTA, and visual elements.
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
            st.image(self.avatar_image, width=120, use_container_width=True)  # Updated to use_container_width

        # Call to action (CTA) as a clickable link
        if self.cta_text and self.cta_link:
            st.markdown(f"[{self.cta_text}]({self.cta_link})", unsafe_allow_html=True)

        # Add some spacing and style adjustments
        st.markdown("<br>", unsafe_allow_html=True)

        # Optional: You can add additional components like social media links here

# Example hero area
hero = HeroArea(
    headline="Empowering Businesses with Data-Driven Insights",
    subheading="Turning complex data into actionable strategies and building applications for real-world challenges.",
    cta_text="View My Projects",
    cta_link="https://yourportfolio.com/projects",
    background_image="https://example.com/hero-bg.jpg",  # Optional background image URL
    avatar_image="https://example.com/your-avatar.jpg",  # Optional profile image URL
    layout="center"  # You can change layout to "left", "right", or "full"
)

# Render the Hero Area
hero.render()
