
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
    load_detailed_offerings,
    notebook_examples
)
from front_end_utils import tags_in_twitter_style
from dotenv import load_dotenv
from exceptional_ui import apply_custom_tooltip, _custom_tooltip_with_frost_glass_html,  setup_tooltip_behavior
from exceptional_ui import (
    html_for_tooltip_from_large_list,
    setup_tooltip_behavior
)
from bureaucratic_form import render_bureaucratic_form
from front_end_for_recommended_content import html_for_milestones_from_project_metadata
import html 
from expandable_text import  expandable_text_html

# Load environment variables
load_dotenv()
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "573053658650")
DEFAULT_EMAILS = [
    ("juanosio838@gmail.com"),
    ("jg.osio151@uniandes.edu.co")
]
DETAILS = {
    # Identification
    "🪪 Full Name": "Juan Guillermo Osio J",

    # Contact Information
    "📧 Emails": f"{DEFAULT_EMAILS[0]}, {DEFAULT_EMAILS[1]}",
    "📱 WhatsApp": WHATSAPP_NUMBER,

    # Professional Profile
    "💼 Profile": " Bachelor’s in Economics, Data Mining Specialist, 5+ Years in Data Mining",
    "🎯 Target Roles": "Data Minning Developer, Machine Learning Engineer",

    # Technical Skills
    "🚀 Excellence Tier": "Python, R Studio, Stata, GPT",
    "🔧 Proficiency Tier": "Airflow, SQL, Spark, Linux, GitHub",

    # Location
    "📍 Location": "Bogotá, Colombia",

    # Compensation
    "💲Compensation": "$1500 - $2000 per month, $20 per consultancy hour"
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
        self.detailed_offering= detailed_offering

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
        
        self.render_detailed_offering()
        #self.render_code_samples(notebook_examples)
         
    
    def render_code_samples(self, notebook_examples):
        st.markdown(
            """
            <style>
                .non-fixed-navbar {
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(4px);
                    border: 2px solid rgba(255, 255, 255, 0.9);
                    box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.1);
                    padding: 10px 20px;
                    border-radius: 15px;
                    display: flex;
                    gap: 20px;
                    align-items: center;
                    justify-content: center;
                    width: fit-content;
                }
                .colab-link {
                    display: inline-block;
                    text-decoration: none;
                    transition: transform 0.2s ease-in-out;
                    position: relative;
                    text-align: center;
                }
                .colab-link img {
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                }
                .colab-link:hover {
                    transform: scale(1.1);
                }
                .colab-link::after {
                    content: attr(data-tooltip);
                    position: absolute;
                    bottom: 70px;
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
                .colab-link:hover::after {
                    opacity: 1;
                    visibility: visible;
                }
                .section-label {
                    text-align: center;
                    font-size: 18px;
                    font-weight: 300;
                    color: #444;
                    margin-bottom: 10px;
                    font-style: italic;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    
        default_icon = "https://upload.wikimedia.org/wikipedia/commons/d/d0/Google_Colaboratory_SVG_Logo.svg"
    
        links_html = "".join([
            f"""
            <a href="{item['href']}" class="colab-link" data-tooltip="{item['tooltip']}">
                <img src="{item['thumbnail'] if 'thumbnail' in item else default_icon}" alt="">
            </a>
            """ for item in notebook_examples
        ])
    
        st.markdown(
            f"""
            <div>
                <p class="section-label">
                    I highlighted some exceptional code samples from my ML consultancies:
                </p>
                <div class="non-fixed-navbar">
                    {links_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    
    def render_detailed_offering(self, id_pattern="offering-{}", colors=["#f0f0f0", "#ffffff"]):
    
        import html  # Ensure html escaping is available
    
        # (0) Visual style for figure & tooltip
        figure_style = {
            "label": "Technical Skills", 
            "color": "#F9A825",        # Warm amber
            "pastel": "#FFF9C4",       # Light yellow hover
            "icon": "https://img.icons8.com/?size=100&id=YKRQA7CZkqVz&format=png&color=000000", 
            "emoji": "✨",
            "default_text": "{n} technical skills listed"
        }  
        label, color, pastel_color, icon_url, emoji, default_text = (
            figure_style["label"], figure_style["color"], figure_style["pastel"], figure_style["icon"], figure_style["emoji"], figure_style["default_text"]
        )
    
        # (1) Load offerings
        offerings = load_detailed_offerings()
        offering_html = '<h3>Key Professional Offerings</h3>'
        offering_html += '<ul style="list-style-type: none;">'
        style_block = "<style>"
    
        # (2) Iterate and render
        for i, offer in enumerate(offerings):
    
            element_id = id_pattern.format(i + 1)
            bg_color = colors[i % len(colors)]
    
            # Expandable text block
            expanded_html, expanded_style = expandable_text_html(offer["description"], wrap_style=False)
            style_block += expanded_style
    
            offering_html += (
                f'<li id="{element_id}" class="offering-container" style="background-color: {bg_color}; padding: 8px 16px; border-radius: 4px; margin-bottom: 10px;">'
                f'<p style="text-align: justify; margin: 0;">'
                f'<strong>{offer["title"]}</strong>: {expanded_html}'
            )
    
            # Tooltip block
            if "skills" in offer:
    
                skills = offer["skills"]
                skills_count = len(skills)
                summary = default_text.format(n=skills_count)
    
                visible_milestone = f'<div style="color:{color}; text-align: center;">' \
                                    f'<img src="{icon_url}" alt="{label}" style="width: 30px; height: 30px;"/><br>' \
                                    f'<label>{summary}</label></div>'
    
                tooltip_content = "".join(
                    f'<div style="color:{color};">{emoji} {html.escape(m)}</div>' for m in skills
                )
    
                tooltip_html = f"""
                <div class="tooltip-container" style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; cursor: pointer;">
                  <div class="skills-container" style="position: relative; display: inline-block;">
                    <div id="{element_id}" style="border-bottom: 1px dashed gray;" class="hover-trigger">
                      {visible_milestone}
                    </div>
                    <div class="tooltip" style="margin-top: 8px;">
                      <strong>{label}:</strong>
                      <span>{tooltip_content}</span>
                    </div>
                  </div>
                </div>
                """
                offering_html += tooltip_html
    
            offering_html += "<br>"
    
            if "subitems" in offer:
                offering_html += '<ul style="list-style-type: none; padding-left: 0;">'
                for subitem in offer["subitems"]:
                    offering_html += f'<li>{subitem}</li>'
                offering_html += '</ul>'
    
            offering_html += '</li>'
    
        offering_html += '</ul>'
        st.markdown(offering_html, unsafe_allow_html=True)
    
        style_block += "</style>"
        st.markdown(style_block, unsafe_allow_html=True)
    
        st.markdown(f"""
          <style>
              .skills-container:hover {{
                  background-color: {pastel_color};
                  transition: background-color 0.3s ease-in-out;
                  border-radius: 5px;
              }}
    
              .tooltip {{
                  visibility: hidden;
                  opacity: 0;
                  transform: translateY(5px) scale(0.95);
                  transition: 
                      opacity 0.3s ease-in-out, 
                      visibility 0.3s ease-in-out, 
                      transform 0.3s ease-in-out;
                  background-color: rgba(255, 249, 196, 0.8);  /* pastel amber */
                  backdrop-filter: blur(1px);
                  color: black;
                  text-align: left;
                  padding: 10px;
                  border-radius: 5px;
                  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
                  position: absolute;
                  left: 50%;
                  top: 100%;
                  transform: translateX(-50%) translateY(5px);
                  min-width: 300px;
                  max-width: 400px;
                  z-index: 1;
                  border: 1px solid rgba(200, 200, 200, 0.5);
                  transform-origin: top center;
              }}
    
              .hover-trigger:hover ~ .tooltip {{
                  visibility: visible;
                  opacity: 1;
                  transform: translateX(-50%) translateY(0px) scale(1.1);
              }}
          </style>
          """,
          unsafe_allow_html=True)




# Instantiate and render HeroArea with data loaded from the loader functions
hero = HeroArea(
    quote=load_quote(),
    avatar_image="jg_pick.jpg",
    avatar_caption="",
    avatar_tags=["Economist", "Data Analyst", "ML Engineer", "Data Engineer", "Application Developer"],
    detailed_offering="",
)
