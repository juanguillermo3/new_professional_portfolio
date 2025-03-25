
"""
title: Hero Section
description: A subtle yet impactful hero section for a professional portfolio. Styled as a book quote with a bio picture, 
             it presents essential information and key call-to-action elements.
"""


import streamlit as st
import os
from hero_area_data_loader import (
    load_quote, 
    load_avatar_caption, 
    load_code_samples, 
    load_detailed_offering
)
from front_end_utils import tags_in_twitter_style
from dotenv import load_dotenv
from exceptional_ui import apply_custom_tooltip, _custom_tooltip_with_frost_glass_html,  setup_tooltip_behavior
from exceptional_ui import (
    html_for_tooltip_from_large_list,
    setup_tooltip_behavior
)


# Load environment variables
load_dotenv()
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "573053658650")
DEFAULT_EMAILS = [
    ("juanosio838@gmail.com"),
    ("jg.osio151@uniandes.edu.co")
]

class HeroArea:
    def __init__(self, 
                 quote, 
                 avatar_image: str = None, 
                 avatar_caption: str = "", 
                 avatar_tags: list = None,
                 code_samples: list = None, 
                 code_samples_intro: str = "I’ve highlighted the following code samples from my ML consulting projects as examples of my work.",
                 whatsapp_number: str = WHATSAPP_NUMBER, 
                 contact_button_intro: str = "Interested in collaborating? Let's discuss how I can bring value to your project. I'm ready to help when you are.",
                 professional_offering: str = "Professional offering description.",
                 detailed_offering: str = "Detailed offering description.",
                 tooltip_content: dict = None):  # Added tooltip content loader
        
        self.quote = quote if isinstance(quote, list) else [quote]
        self.avatar_image = avatar_image
        self.avatar_caption = avatar_caption
        self.avatar_tags = avatar_tags if avatar_tags else []
        self.code_samples = code_samples if code_samples is not None else load_code_samples()
        self.code_samples_intro = code_samples_intro
        self.whatsapp_number = whatsapp_number
        self.contact_button_intro = contact_button_intro
        self.professional_offering = professional_offering
        self.detailed_offering, self.ids = detailed_offering

    def render_code_samples(self):
        st.markdown(f'<p class="code-samples-intro">{self.code_samples_intro}</p>', unsafe_allow_html=True)
        
        st.markdown("<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px;'>", unsafe_allow_html=True)
        
        for i, sample in enumerate(self.code_samples):
            element_id = f"code-sample-{i}"  # Unique ID for each button
            tooltip_text = "Check out this example! ✨"  # Enthusiastic, positive vibe
    
            # Render the button with an ID
            st.markdown(f"""
            <a href="{sample['url']}" target="_blank">
                <button id="{element_id}" style="background-color: #24292f; color: white; border: 1px solid white; padding: 10px 20px; font-size: 14px; border-radius: 5px; text-align: center; width: 100%;">
                    {sample['title']}
                </button>
            </a>
            """, unsafe_allow_html=True)
    
            # Apply the tooltip
            apply_custom_tooltip(element_id, tooltip_text)
        
        st.markdown("</div>", unsafe_allow_html=True)

    def render_contact_details(self):
          contact_html = f"""
          <div style="text-align: left; font-size: 0.9em; color: #444; line-height: 1.2;">
              <p style="padding-left: 20px;">📱 {self.whatsapp_number}</p>
              <p style="padding-left: 20px;">📧 {' | '.join(DEFAULT_EMAILS)}</p>
          </div>
          """
          st.markdown(contact_html, unsafe_allow_html=True)

    def render_contact_button(self):
        if not self.whatsapp_number:
            st.warning("WhatsApp number is not available.")
            return
        
        st.markdown(f'<p class="contact-button-intro">{self.contact_button_intro}</p>', unsafe_allow_html=True)
        
        button_url = f"https://wa.me/{self.whatsapp_number}?text=Hi,%20I%27d%20like%20to%20connect!"
    
        button_label = "Start a Conversation 💬"
    
        st.markdown(f"""
        <a href="{button_url}" target="_blank">
            <button style="background-color: #25d366; color: white; border: 1px solid white; padding: 10px 20px; font-size: 14px; border-radius: 5px; text-align: center; width: 100%;">
                {button_label}
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    def _render_biopic_section(self):
        """Renders the avatar, caption, hashtags, and contact details with a fun tooltip."""
        avatar_id = "biopic-avatar"
    
        st.markdown('<div class="hero-avatar-container" style="position: relative;">', unsafe_allow_html=True)
    
        # Actual image (keeps working properly)
        st.image(f"assets/{self.avatar_image}", use_container_width=True)
    
        # Invisible div positioned over the image
        st.markdown(f"""
        <div id="{avatar_id}" style="
            position: absolute; 
            top: 0; left: 0; width: 100%; height: 100%;
            background: transparent;">
        </div>
        """, unsafe_allow_html=True)
    
        apply_custom_tooltip(avatar_id, "I am 15% less good-looking but 25% greater worker than I appear. 🎭💪")
    
        # Caption and Hashtags
        tags_html = tags_in_twitter_style(self.avatar_tags)
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 1.1em; color: #444;">
                <p>{self.avatar_caption}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
        # Contact Details
        #self.render_contact_details()
    
        st.markdown('</div>', unsafe_allow_html=True)

    
    def _render_quote(self):
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
            padding: 0 5%;
            padding-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
    
        for paragraph in self.quote:
            st.markdown(f'<p class="hero-quote">{paragraph}</p>', unsafe_allow_html=True)
    
    def _render_bureaucratic_form(self, details: dict):
        """
        Renders a bureaucratic-style form layout to display critical personal/professional information.
        :param details: Dictionary containing field names as keys and corresponding values.
        """
        # Define the layout structure (irregular grid pattern)
        cols = st.columns([2, 3, 2, 3])  # Adjust width proportions as needed
    
        # Iterate through the dictionary and place values in the grid
        fields = list(details.items())
    
        for i in range(0, len(fields), 2):  # Two fields per row
            with cols[i % 4]:
                field_name, field_value = fields[i]
                st.text_input(f"**{field_name}**", value=field_value, disabled=True, label_visibility="collapsed")
    
            if i + 1 < len(fields):  # Ensure we don't go out of bounds
                with cols[(i + 1) % 4]:
                    field_name, field_value = fields[i + 1]
                    st.text_input(f"**{field_name}**", value=field_value, disabled=True, label_visibility="collapsed")

    

    def render(self):
        col1, col2 = st.columns([2, 1])
    
        # Render Quote Section
        with col1:
            self._render_quote()
    
        # Render Biopic Section
        if self.avatar_image:
            with col2:
                self._render_biopic_section()


         
        # Bureaucratic Form Section (before detailed professional offering)
        self._render_bureaucratic_form(
        {
          "Name": "Juan Guillermo"
        })
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Expandable Detailed Offering Section
        expander_label = "Explore more (details)"
        with st.expander(expander_label, expanded=True):
            st.markdown(self.detailed_offering, unsafe_allow_html=True)
            for id in self.ids:
                st.markdown(setup_tooltip_behavior(id), unsafe_allow_html=True)
            
            self.render_code_samples()
                
# Instantiate and render HeroArea with data loaded from the loader functions
hero = HeroArea(
    quote=load_quote(),
    avatar_image="jg_pick.jpg",
    avatar_caption="",
    avatar_tags=["Economist", "Data Analyst", "ML Engineer", "Data Engineer", "Application Developer"],
    detailed_offering=load_detailed_offering(),
)
