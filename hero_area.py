
"""
title: Hero Section
description: A subtle yet impactful hero section for a professional portfolio. Styled as a book quote with a bio picture, 
             it presents essential information and key call-to-action elements.
"""


import streamlit as st
import os
import re
from hero_area_data_loader import (
    load_quote, 
    load_avatar_caption, 
    load_code_samples, 
    custom_html_for_offerings
)
from front_end_utils import tags_in_twitter_style
from dotenv import load_dotenv
from exceptional_ui import apply_custom_tooltip, _custom_tooltip_with_frost_glass_html,  setup_tooltip_behavior
from exceptional_ui import (
    html_for_tooltip_from_large_list,
    setup_tooltip_behavior
)
from bureaucratic_form import render_bureaucratic_form

# Load environment variables
load_dotenv()
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "573053658650")
DEFAULT_EMAILS = [
    ("juanosio838@gmail.com"),
    ("jg.osio151@uniandes.edu.co")
]
DETAILS = {
    # Personal Identification
    "🆔 Full Name": "Juan Guillermo Osio J",

    # Location & Legal Status
    "📍 Location": "Bogotá, Colombia",
    
    # Contact Information
    "📧 Email": DEFAULT_EMAILS[0],
    "📨 Email (Alternative)": DEFAULT_EMAILS[1],
    "📱 WhatsApp": WHATSAPP_NUMBER,

    # Professional Summary
    "💼 Job Title": "Freelance Data Mining Specialist",

    # Target Roles
    "🎯 Target Roles": "Data Minning Developer, Machine Learning Engineer",
  
    "📊 Experience": "5+ Years in Data Mining",
    "🎓 Education": "Bachelor’s in Economics",
    
    # Tech Stack
    "🚀 Excellence Tier": "Python, R Studio, Stata, GPT",
    "🔧 Proficiency Tier": "Airflow, SQL, Spark, Linux, GitHub",
    

    # Compensation
    "💰 Expected Rate": "$1500 - $2000 per month"
}
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
        render_bureaucratic_form(DETAILS)
        st.markdown('<br>', unsafe_allow_html=True)       
        st.markdown('<br>', unsafe_allow_html=True)  
        
        st.markdown(self.detailed_offering, unsafe_allow_html=True)
        for id in self.ids:
            st.markdown(setup_tooltip_behavior(id), unsafe_allow_html=True)          
        self.render_code_samples()

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
        }
        
        @keyframes inkSeep {
            0% { opacity: 0; filter: blur(5px); transform: scale(0.95); }
            100% { opacity: 1; filter: blur(0); transform: scale(1); }
        }
    
        .ink-word {
            display: inline-block;
            opacity: 0;
            animation: inkSeep 0.3s ease-in-out forwards;
        }
        </style>
        """, unsafe_allow_html=True)
    
        for paragraph in self.quote:
            # Match words with possible <b> or <em> tags and include the following space or comma
            words = re.findall(r'(<[^>]+>[^<]+<\/[^>]+>|[^<\s,]+)([\s,]*)', paragraph)
    
            # Construct the styled text preserving spacing and punctuation
            styled_text = ' '.join(
                f'<span class="ink-word" style="animation-delay: {i * 0.1}s;">{word}{space}</span>'
                for i, (word, space) in enumerate(words)
            )
    
            st.markdown(f'<p class="hero-quote">{styled_text}</p>', unsafe_allow_html=True)

def render_code_samples(self):
    # Define Custom CSS for a Stylish, Centered Row of Code Sample Buttons
    st.markdown(
        """
        <style>
            .code-sample-container {
                display: flex;
                justify-content: center;  /* Center horizontally */
                align-items: center;
                flex-direction: row;  /* Ensure row layout */
                flex-wrap: wrap;  /* Allow wrapping if needed */
                padding: 15px 10px;
                border-radius: 15px;
                background: rgba(255, 255, 255, 0.1);  /* Frosted glass effect */
                backdrop-filter: blur(5px);
                border: 2px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.1);
                gap: 20px;  /* Space between buttons */
                width: fit-content;
                margin: 0 auto;  /* Center the div in its container */
            }
            .code-sample-link {
                display: inline-block;
                text-decoration: none;
                transition: transform 0.2s ease-in-out;
                position: relative;
            }
            .code-sample-link:hover {
                transform: scale(1.1);
            }
            .code-sample-btn {
                width: 75px;
                height: 75px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #24292f;
                border: 2px solid white;
                transition: all 0.3s ease-in-out;
            }
            .code-sample-btn img {
                width: 45px;
                height: 45px;
                border-radius: 50%;
            }
            .code-sample-btn:hover {
                background-color: #1c1f26;
            }
            /* Tooltip Styling */
            .code-sample-link::after {
                content: attr(data-tooltip);
                position: absolute;
                bottom: 85px;
                left: 50%;
                transform: translateX(-50%);
                background-color: #333;
                color: white;
                padding: 6px 12px;
                border-radius: 5px;
                font-size: 14px;
                white-space: nowrap;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.3s ease-in-out, visibility 0.3s;
            }
            .code-sample-link:hover::after {
                opacity: 1;
                visibility: visible;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Default icon if not provided
    default_icon = "https://upload.wikimedia.org/wikipedia/commons/d/d0/Google_Colaboratory_SVG_Logo.svg"

    # Create a single markdown string to keep buttons in a row
    buttons_html = '<div class="code-sample-container">'
    
    for sample in self.code_samples:
        icon_url = sample.get("icon_url", default_icon)
        tooltip_text = f"Try {sample['title']}! 🚀"

        buttons_html += f"""
            <a href="{sample['url']}" target="_blank" class="code-sample-link" data-tooltip="{tooltip_text}">
                <div class="code-sample-btn">
                    <img src="{icon_url}" alt="{sample['title']}">
                </div>
            </a>
        """

    buttons_html += '</div>'

    # Render all buttons inside a single markdown block
    st.markdown(buttons_html, unsafe_allow_html=True)


        
    
# Instantiate and render HeroArea with data loaded from the loader functions
hero = HeroArea(
    quote=load_quote(),
    avatar_image="jg_pick.jpg",
    avatar_caption="",
    avatar_tags=["Economist", "Data Analyst", "ML Engineer", "Data Engineer", "Application Developer"],
    detailed_offering=custom_html_for_offerings(),
)
