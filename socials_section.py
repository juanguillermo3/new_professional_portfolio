import streamlit as st

class SocialMediaButtons:
    def __init__(self, links: dict):
        self.links = links
        self.platform_colors = {
            "WhatsApp": "#25D366",
            "LinkedIn": "#0077B5",
            "GitHub": "#333333",
            "Facebook": "#3b5998",
        }

    def create_button(self, platform, url):
        color = self.platform_colors.get(platform, "#000000")  # Default to black if not found
        return f"""
            <a href="{url}" target="_blank">
                <button style="background-color:{color}; color:white; border-radius:10px; 
                               padding:10px 20px; font-size:16px; border:none; margin: 5px;">
                    {platform}
                </button>
            </a>
        """

    def render(self):
        # Header and Description
        st.subheader("Connect with Me 🤝")
        st.markdown("---")
        st.markdown('<p style="color: gray;">Feel free to connect with me via social media or WhatsApp.</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Buttons Area
        buttons_area = st.container()
        with buttons_area:
            st.markdown('<div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 10px;">', unsafe_allow_html=True)
            for platform, url in self.links.items():
                button_html = self.create_button(platform, url)
                st.markdown(button_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# Instantiation
socials = SocialMediaButtons(
    links={
        "LinkedIn": "https://www.linkedin.com/in/juan-guillermo-osio/",
        "GitHub": "https://github.com/juanguillermo3/",
        "WhatsApp": "https://wa.me/573053658650",
        "Facebook": "https://www.facebook.com/juan.jaramillo.96",
    }
)

