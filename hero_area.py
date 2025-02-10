"""
title: Hero section for a professional portfolio.
description: Low key hero section for a professional porftolio. Styled as a quote from a book with a biopick.
Author: Juan Guillermo
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

# Load environment variables
load_dotenv()
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "573658650")
DEFAULT_EMAILS = [
    ("📧", "juanosio838@gmail.com"),
    ("📧", "jg.osio151@uniandes.edu.co")
]

class HeroArea:
    def __init__(self, quote, avatar_image: str = None, avatar_caption: str = "", avatar_tags: list = None,
                 code_samples: list = None, code_samples_intro: str = "Explore the code samples below:",
                 whatsapp_number: str = WHATSAPP_NUMBER, emails: list = None,
                 contact_button_intro: str = "Let's work together. Connect to talk about your specific requirements.",
                 professional_offering: str = "", detailed_offering: str = ""):
        self.quote = quote if isinstance(quote, list) else [quote]
        self.avatar_image = avatar_image
        self.avatar_caption = avatar_caption
        self.avatar_tags = avatar_tags if avatar_tags else []
        self.code_samples = code_samples if code_samples is not None else load_code_samples()
        self.code_samples_intro = code_samples_intro
        self.whatsapp_number = whatsapp_number
        self.emails = emails if emails else DEFAULT_EMAILS
        self.contact_button_intro = contact_button_intro
        self.professional_offering = professional_offering
        self.detailed_offering = detailed_offering

    def prepare_contact_details(self):
        contact_html = ""  # Initialize empty HTML
        if self.whatsapp_number:
            contact_html += f'<p>📱 <a href="https://wa.me/{self.whatsapp_number}" target="_blank">{self.whatsapp_number}</a></p>'
        for icon, email in self.emails:
            contact_html += f'<p>{icon} <a href="mailto:{email}">{email}</a></p>'
        return contact_html

    def render_code_samples(self):
        st.markdown(f'<p class="code-samples-intro">{self.code_samples_intro}</p>', unsafe_allow_html=True)
        for sample in self.code_samples:
            st.markdown(f'<a href="{sample["url"]}" target="_blank">{sample["title"]}</a>', unsafe_allow_html=True)
    
    def render(self):
        col1, col2 = st.columns([2, 1])
        with col1:
            for paragraph in self.quote:
                st.markdown(f'<p class="hero-quote">{paragraph}</p>', unsafe_allow_html=True)

        if self.avatar_image:
            with col2:
                st.image(f"assets/{self.avatar_image}", use_container_width=True)
                tags_html = tags_in_twitter_style(self.avatar_tags)
                st.markdown(f'<p>{self.avatar_caption} {tags_html}</p>', unsafe_allow_html=True)
                st.markdown(self.prepare_contact_details(), unsafe_allow_html=True)
        
        with st.expander("Explore more (details)", expanded=True):
            st.markdown(self.detailed_offering, unsafe_allow_html=True)
            self.render_code_samples()

        
# Instantiate and render HeroArea with data loaded from the loader functions
hero = HeroArea(
    quote=load_quote(),
    avatar_image="jg_pick.jpg",
    avatar_caption="",
    avatar_tags=["Economist", "Data Analyst", "Data Minning", "Data Engineer", "Application Developer"],
    detailed_offering=load_detailed_offering()
)




