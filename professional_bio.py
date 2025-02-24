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
    
    def __init__(self, section_description):
        """
        :param section_description: A string representing the description for the Curriculum Vitae section.
        :param tags: A list of string tags to be displayed in a Twitter-style format.
        """
        
        super().__init__(
            title=title,
            description=section_description,
            verified=self.DATA_VERIFIED,  # Use subclass defaults
            early_dev=self.EARLY_DEVELOPMENT_STAGE,
            ai_content=not self.DATA_VERIFIED  # This ensures consistency
        )

        self.statement = professional_statement()
        self.work_experience = load_experience_items()
        self.education = load_education_items()

        # Sort the work and education items by end date (most recent first)
        self.work_experience.sort(key=lambda x: parse_as_datetime(x['date_range'][1]), reverse=True)
        self.education.sort(key=lambda x: parse_as_datetime(x['date_range'][1]), reverse=True)

    def render(self):
        
        self._render_headers()
    
        st.markdown("#### Work Experience 🔧")
    
        circle_color = "#1c7bba"
        shadow_circle_color = "rgba(28, 123, 186, 0.2)"
        current_circle_color = "#ff6f00"
        shadow_current_circle_color = "rgba(255, 111, 0, 0.2)"
    
        for experience in self.work_experience:
            start_date, end_date = experience['date_range']
            is_current_job = CURRENT_JOB_KEYWORD.strip().lower() == end_date.strip().lower()
            display_circle_color = current_circle_color if is_current_job else circle_color
            display_shadow_color = shadow_current_circle_color if is_current_job else shadow_circle_color
            date_range_str = f"{format_date_for_frontend(start_date)} - {format_date_for_frontend(end_date)}"
    
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='width: 20px; height: 20px; border: 5px solid {display_circle_color}; border-radius: 50%; 
                    box-shadow: 0 0 0 5px {display_shadow_color}; position: relative; margin-right: 10px; margin-top: 2px;'>
                </div> 
                <div style="max-width: 500px;">
                    <strong>{experience['title']}</strong><br> 
                    <em>{experience['company']}</em><br> 
                    <p>{experience['description']}</p>
                    <p style='font-style: italic;'>{date_range_str}</p>
                </div>
            </div>""", unsafe_allow_html=True)
    
        st.markdown("#### Education 🎓")
    
        for edu in self.education:
            start_date, end_date = edu['date_range']
            date_range_str = f"{format_date_for_frontend(start_date)} - {format_date_for_frontend(end_date)}"
    
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='width: 20px; height: 20px; border: 5px solid {circle_color}; border-radius: 50%; 
                    box-shadow: 0 0 0 5px {shadow_circle_color}; position: relative; margin-right: 10px; margin-top: 2px;'>
                </div> 
                <div style="max-width: 500px;">
                    <strong>{edu['title']}</strong><br> 
                    <em>{edu['institution']}</em><br> 
                    <p>{edu['description']}</p>
                    <p style='font-style: italic;'>{date_range_str}</p>
                </div>
            </div>""", unsafe_allow_html=True)
        

cv = CurriculumVitae(
    section_description="This is a description of the Curriculum Vitae section."
)

