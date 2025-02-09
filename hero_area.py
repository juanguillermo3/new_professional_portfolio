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

class HeroArea:
    def __init__(self, quote, avatar_image: str = None, avatar_caption: str = "", 
                 code_samples: list = None, code_samples_intro: str = "Explore the code samples below:",
                 whatsapp_number: str = None, contact_button_intro: str = "Let's work together. Connect to talk about your specific requirements. I can start working for you almost instantly",
                 professional_offering: str = "Simply put, I can develop application code for analytics applications at any stage of the ML/Data Analysis development workflow. I offer several key differentiators compared to typical data analysts: expertise in developing high-performance predictive analytics (Artificial Intelligence, Machine Learning, Genetic Optimization, Ensemble Models, Forecasting models); full commitment to research modern information tools for data analytics (Python, R, Stata, Airflow, Spark, SQL, Bash scripting, Cloud computing, GPT, SQLAlchemy, APIs, development frameworks, Git, and more); strong automation capabilities in complex empirical environments with multiple sources, schemas, data types, and mixes of structured/unstructured data; robust algorithm and application development skills in Python, including libraries like Requests, Selenium, Airflow, Pandas, Scikit-Learn, TensorFlow, Plotly, Flask, and Dash, as well as logging systems and object-oriented programming; knowledge of formal software development topics (architectural and design patterns, development methodologies, distributed systems, computing resources); and a very efficient development workflow supported by technologies like GPT.",
                 detailed_offering: str ="This is a more detailed offering"
                ):
        self.quote = quote if isinstance(quote, list) else [quote]
        self.avatar_image = avatar_image
        self.avatar_caption = avatar_caption
        self.code_samples = code_samples if code_samples is not None else load_code_samples()
        self.code_samples_intro = code_samples_intro
        self.whatsapp_number = whatsapp_number or os.getenv("WHATSAPP_NUMBER")
        self.contact_button_intro = contact_button_intro
        self.professional_offering = professional_offering
        self.detailed_offering = detailed_offering

    def render_code_samples(self):
        st.markdown(f'<p class="code-samples-intro">{self.code_samples_intro}</p>', unsafe_allow_html=True)
        st.markdown("<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px;'>", unsafe_allow_html=True)
        for sample in self.code_samples:
            st.markdown(f"""
            <a href="{sample['url']}" target="_blank">
                <button style="background-color: #24292f; color: white; border: 1px solid white; padding: 10px 20px; font-size: 14px; border-radius: 5px; text-align: center; width: 100%;">
                    {sample['title']}
                </button>
            </a>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    def render_contact_button(self):
        if not self.whatsapp_number:
            st.warning("WhatsApp number is not available.")
            return
        st.markdown(f'<p class="contact-button-intro">{self.contact_button_intro}</p>', unsafe_allow_html=True)
        button_url = f"https://wa.me/{self.whatsapp_number}?text=Hi,%20I%27d%20like%20to%20get%20in%20touch!"
        st.markdown(f"""
        <a href="{button_url}" target="_blank">
            <button style="background-color: #25d366; color: white; border: 1px solid white; padding: 10px 20px; font-size: 14px; border-radius: 5px; text-align: center; width: 100%;">
                Contact Me on WhatsApp
            </button>
        </a>
        """, unsafe_allow_html=True)

    def render(self):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""<style>
            .hero-quote {
                font-style: italic;
                font-size: 1.5em;
                line-height: 1.8;
                margin: 0 auto;
                max-width: 800px;
                color: #333333;
                text-align: justify;
                padding-bottom: 20px;
            }
            .hero-avatar-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;  /* Ensure the container takes up full height */
                text-align: center;  /* Center the content horizontally as well */
                padding: 0;  /* Remove padding if needed */
            }
            </style>""", unsafe_allow_html=True)
            for paragraph in self.quote:
                st.markdown(f'<p class="hero-quote">{paragraph}</p>', unsafe_allow_html=True)
        if self.avatar_image:
            with col2:
                st.markdown('<div class="hero-avatar-container">', unsafe_allow_html=True)
                st.image(f"assets/{self.avatar_image}", caption=self.avatar_caption, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        expander_label = "Explore more (details)"
        with st.expander(expander_label, expanded=True):
            st.markdown(self.detailed_offering, unsafe_allow_html=True)
            self.render_code_samples()
        self.render_contact_button()


# Instantiate and render HeroArea with data loaded from the loader functions
hero = HeroArea(
    quote=load_quote(),
    avatar_image="jg_pick.jpg",
    avatar_caption=load_avatar_caption(),
    code_samples_intro="As an easy entry-point to my work, you can check these selected code samples from my ML consultancies:",
    whatsapp_number="573053658650",
    detailed_offering=load_detailed_offering()
)
# hero.render()



