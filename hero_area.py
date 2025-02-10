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
# Load environment variables from the .env file
load_dotenv()

WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "573658650")
EMAILS = ["juanosio838@gmail.com", "jg.osio151@uniandes.edu.co"]

class HeroArea:
    def __init__(self, quote, avatar_image: str = None, avatar_caption: str = "", avatar_tags: list = None,
                 code_samples: list = None, code_samples_intro: str = "Explore the code samples below:",
                 whatsapp_number: str = WHATSAPP_NUMBER, contact_button_intro: str = "Let's work together. Connect to talk about your specific requirements. I can start working for you almost instantly",
                 professional_offering: str = "Simply put, I can develop application code for analytics applications at any stage of the ML/Data Analysis development workflow.",
                 detailed_offering: str ="This is a more detailed offering"
                ):
        self.quote = quote if isinstance(quote, list) else [quote]
        self.avatar_image = avatar_image
        self.avatar_caption = avatar_caption
        self.avatar_tags = avatar_tags if avatar_tags else []
        self.code_samples = code_samples if code_samples is not None else load_code_samples()
        self.code_samples_intro = code_samples_intro
        self.whatsapp_number = whatsapp_number
        self.contact_button_intro = contact_button_intro
        self.professional_offering = professional_offering
        self.detailed_offering = detailed_offering

    def prepare_contact_details(self):
        contact_html = f"""
        <div style='text-align: center; margin-top: 5px;'>
            <p style='margin: 2px 0;'><b>📞 WhatsApp:</b> {self.whatsapp_number}</p>
            <p style='margin: 2px 0;'><b>📝 Emails:</b> {', '.join(EMAILS)}</p>
        </div>
        """
        return contact_html

    def render(self):
        col1, col2 = st.columns([2, 1])
        with col1:
            for paragraph in self.quote:
                st.markdown(f'<p class="hero-quote">{paragraph}</p>', unsafe_allow_html=True)

        if self.avatar_image:
            with col2:
                st.image(f"assets/{self.avatar_image}", use_container_width=True)
                tags_html = tags_in_twitter_style(self.avatar_tags)
                st.markdown(
                    f"""
                    <div style="text-align: center; font-size: 1.1em; color: #444;">
                        <p>{self.avatar_caption} {tags_html}</p>
                        {self.prepare_contact_details()}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        expander_label = "Explore more (details)"
        with st.expander(expander_label, expanded=True):
            st.markdown(self.detailed_offering, unsafe_allow_html=True)
        
# Instantiate and render HeroArea with data loaded from the loader functions
hero = HeroArea(
    quote=load_quote(),
    avatar_image="jg_pick.jpg",
    avatar_caption="",
    avatar_tags=["Economist", "Data Analyst", "Data Minning", "Data Engineer", "Application Developer"],
    detailed_offering=load_detailed_offering()
)




