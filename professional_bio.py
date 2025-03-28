"""
title: Professional Bio
description: A portfolio section dedicated to showcasing the owner's Curriculum Vitae and professional background. 
             It is structured around a main professional statement and two key sections: work experience and education. 
             Its design is inspired by modern job platforms, ensuring a clean and engaging presentation.
"""

import random
import streamlit as st
from cv_data_loader import (
    load_experience_items, 
    load_education_items, 
    professional_statement, 
    parse_as_datetime, 
    format_date_for_frontend, 
    CURRENT_JOB_KEYWORD
)
from front_end_utils import tags_in_twitter_style
from portfolio_section import PortfolioSection

class CurriculumVitae(PortfolioSection):
    EARLY_DEVELOPMENT_STAGE = False  # Override class defaults for this section
    DATA_VERIFIED = True  
    
    CIRCLE_COLOR = "#1c7bba"
    SHADOW_CIRCLE_COLOR = "rgba(28, 123, 186, 0.2)"
    CURRENT_CIRCLE_COLOR = "#ff6f00"
    SHADOW_CURRENT_CIRCLE_COLOR = "rgba(255, 111, 0, 0.2)"

    def __init__(self, title="Curriculum Vitae 📜", section_description=professional_statement()):
        super().__init__(
            title=title,
            description=section_description,
            verified=self.DATA_VERIFIED,
            early_dev=self.EARLY_DEVELOPMENT_STAGE,
            ai_content=not self.DATA_VERIFIED  # Ensures consistency
        )

        self.statement = professional_statement()
        self.work_experience = load_experience_items()
        self.education = load_education_items()

        # Sort the work and education items by end date (most recent first)
        self.work_experience.sort(key=lambda x: parse_as_datetime(x['date_range'][1]), reverse=True)
        self.education.sort(key=lambda x: parse_as_datetime(x['date_range'][1]), reverse=True)

    MAIN_STATEMENT = """
    My recurring interest nevertheless has always been the **modernization** of the **data analysis pipeline** through **cutting-edge techniques**, such as **flexible ML-based inference**, **software and algorithmic automation**, **assimilation of data-related technology**, using **NLP** in **latent semantic spaces**, and, more recently, solving **data analysis tasks** through **agency formation** within **LLM applications**.
    """

    def render(self):
        self._render_headers()
        st.markdown(f'{self.MAIN_STATEMENT}', unsafe_allow_html=True)
        self._render_experience()
        self._render_education()

    def _render_experience(self):
        st.markdown("#### Work Experience 🔧")
        for experience in self.work_experience:
            start_date, end_date = experience['date_range']
            is_current_job = CURRENT_JOB_KEYWORD.strip().lower() == end_date.strip().lower()
            display_circle_color = self.CURRENT_CIRCLE_COLOR if is_current_job else self.CIRCLE_COLOR
            display_shadow_color = self.SHADOW_CURRENT_CIRCLE_COLOR if is_current_job else self.SHADOW_CIRCLE_COLOR
            date_range_str = f"{format_date_for_frontend(start_date)} - {format_date_for_frontend(end_date)}"

            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 16px; height: 16px; border: 4px solid {display_circle_color}; 
                    border-radius: 50%; box-shadow: 0 0 10px {display_shadow_color}; 
                    margin-right: 12px; margin-top: 4px; transition: all 0.3s ease-in-out;'
                    onmouseover="this.style.boxShadow='0 0 20px {display_circle_color}'; this.style.transform='scale(1.1)';"
                    onmouseout="this.style.boxShadow='0 0 10px {display_shadow_color}'; this.style.transform='scale(1)';">
                </div> 
                <div style="max-width: 500px;">
                    <strong>{experience['title']}</strong><br> 
                    <em>{experience['company']}</em><br> 
                    <p>{experience['description']}</p>
                    <p style='font-style: italic;'>{date_range_str}</p>
                </div>
            </div>""", unsafe_allow_html=True)

    def _render_education(self):
        st.markdown("#### Education 🎓")
        for edu in self.education:
            start_date, end_date = edu['date_range']
            date_range_str = f"{format_date_for_frontend(start_date)} - {format_date_for_frontend(end_date)}"

            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 16px; height: 16px; border: 4px solid {self.CIRCLE_COLOR}; 
                    border-radius: 50%; box-shadow: 0 0 10px {self.SHADOW_CIRCLE_COLOR}; 
                    margin-right: 12px; margin-top: 4px; transition: all 0.3s ease-in-out;'
                    onmouseover="this.style.boxShadow='0 0 20px {self.CIRCLE_COLOR}'; this.style.transform='scale(1.1)';"
                    onmouseout="this.style.boxShadow='0 0 10px {self.SHADOW_CIRCLE_COLOR}'; this.style.transform='scale(1)';">
                </div> 
                <div style="max-width: 500px;">
                    <strong>{edu['title']}</strong><br> 
                    <em>{edu['institution']}</em><br> 
                    <p>{edu['description']}</p>
                    <p style='font-style: italic;'>{date_range_str}</p>
                </div>
            </div>""", unsafe_allow_html=True)
    
    def _render_experience(self):
        st.markdown("#### Work Experience 🔧")
        
        accumulated_styles = ""  # Collect styles here to inject once
        
        for experience in self.work_experience:
            start_date, end_date = experience['date_range']
            is_current_job = CURRENT_JOB_KEYWORD.strip().lower() == end_date.strip().lower()
            display_circle_color = self.CURRENT_CIRCLE_COLOR if is_current_job else self.CIRCLE_COLOR
            display_shadow_color = self.SHADOW_CURRENT_CIRCLE_COLOR if is_current_job else self.SHADOW_CIRCLE_COLOR
            date_range_str = f"{format_date_for_frontend(start_date)} - {format_date_for_frontend(end_date)}"
    
            exp_text, exp_style = expandable_text_html(experience['description'])
            accumulated_styles += exp_style  # Accumulate CSS styles
    
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 16px; height: 16px; border: 4px solid {display_circle_color}; 
                    border-radius: 50%; box-shadow: 0 0 10px {display_shadow_color}; 
                    margin-right: 12px; margin-top: 4px; transition: all 0.3s ease-in-out;'
                    onmouseover="this.style.boxShadow='0 0 20px {display_circle_color}'; this.style.transform='scale(1.1)';"
                    onmouseout="this.style.boxShadow='0 0 10px {display_shadow_color}'; this.style.transform='scale(1)';">
                </div> 
                <div style="max-width: 500px;">
                    <strong>{experience['title']}</strong><br> 
                    <em>{experience['company']}</em><br> 
                    {exp_text}  <!-- Insert expandable description -->
                    <p style='font-style: italic;'>{date_range_str}</p>
                </div>
            </div>""", unsafe_allow_html=True)
    
        # Inject accumulated styles once at the end
        if accumulated_styles:
            st.markdown(f"<style>{accumulated_styles}</style>", unsafe_allow_html=True)
    
    def _render_education(self):
        st.markdown("#### Education 🎓")
        
        accumulated_styles = ""  # Collect styles here
        
        for edu in self.education:
            start_date, end_date = edu['date_range']
            date_range_str = f"{format_date_for_frontend(start_date)} - {format_date_for_frontend(end_date)}"
    
            edu_text, edu_style = expandable_text_html(edu['description'])
            accumulated_styles += edu_style  # Accumulate CSS styles
    
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 16px; height: 16px; border: 4px solid {self.CIRCLE_COLOR}; 
                    border-radius: 50%; box-shadow: 0 0 10px {self.SHADOW_CIRCLE_COLOR}; 
                    margin-right: 12px; margin-top: 4px; transition: all 0.3s ease-in-out;'
                    onmouseover="this.style.boxShadow='0 0 20px {self.CIRCLE_COLOR}'; this.style.transform='scale(1.1)';"
                    onmouseout="this.style.boxShadow='0 0 10px {self.SHADOW_CIRCLE_COLOR}'; this.style.transform='scale(1)';">
                </div> 
                <div style="max-width: 500px;">
                    <strong>{edu['title']}</strong><br> 
                    <em>{edu['institution']}</em><br> 
                    {edu_text}  <!-- Insert expandable description -->
                    <p style='font-style: italic;'>{date_range_str}</p>
                </div>
            </div>""", unsafe_allow_html=True)
    
        # Inject accumulated styles once at the end
        if accumulated_styles:
            st.markdown(f"<style>{accumulated_styles}</style>", unsafe_allow_html=True)


cv=CurriculumVitae()
