"""
title: Hero section for a professional portfolio.
description: Low key hero section for a professional porftolio. Styled as a quote from a book with a biopick.
Author: Juan Guillermo
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

from hero_area_data_loader import (
    load_quote, 
    load_avatar_caption, 
    load_code_samples, 
    load_detailed_offering
)
from front_end_utils import tags_in_twitter_style

class HeroArea:
    def __init__(self, quote, avatar_image: str = None, avatar_caption: str = "", 
                 avatar_tags: list = None, code_samples: list = None, 
                 code_samples_intro: str = "Explore the code samples below:",
                 whatsapp_number: str = None, contact_button_intro: str = "Let's work together. Connect to talk about your specific requirements.",
                 professional_offering: str = "Simply put, I can develop application code for analytics applications at any stage of the ML/Data Analysis development workflow.",
                 detailed_offering: str ="This is a more detailed offering"
                ):
        self.quote = quote if isinstance(quote, list) else [quote]
        self.avatar_image = avatar_image
        self.avatar_caption = avatar_caption
        self.avatar_tags = avatar_tags if avatar_tags else []
        self.code_samples = code_samples if code_samples is not None else load_code_samples()
        self.code_samples_intro = code_samples_intro
        self.whatsapp_number = whatsapp_number or os.getenv("WHATSAPP_NUMBER")
        self.contact_button_intro = contact_button_intro
        self.professional_offering = professional_offering
        self.detailed_offering = detailed_offering
    
    def render(self):
        col1, col2 = st.columns([2, 1])
        with col1:
            for paragraph in self.quote:
                st.markdown(f'<p class="hero-quote">{paragraph}</p>', unsafe_allow_html=True)
        if self.avatar_image:
            with col2:
                st.image(f"assets/{self.avatar_image}", caption=self.avatar_caption, use_container_width=True)
                if self.avatar_tags:
                    styled_tags = tags_in_twitter_style(self.avatar_tags)
                    st.markdown(f'<p style="text-align: center;">{styled_tags}</p>', unsafe_allow_html=True)

# Instantiate and render HeroArea with data loaded from the loader functions
hero = HeroArea(
    quote=load_quote(),
    avatar_image="jg_pick.jpg",
    avatar_caption=load_avatar_caption(),
    avatar_tags=["ML", "AI", "Python", "DataScience"],
    detailed_offering=load_detailed_offering()
)




