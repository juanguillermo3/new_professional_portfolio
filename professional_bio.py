"""
title: Curriculum Vitae
description: CV area for a modern proffesional portfolio. The gist of it is serving an elegant front end representation of a couple of unordered lists: work items, experience items. Its design is inspired by modern job intermediation sites.
"""

import streamlit as st
from cv_data_loader import load_experience_items, load_education_items, professional_statement, parse_as_datetime, CURRENT_JOB_KEYWORD

class CurriculumVitae:
    def __init__(self, section_description):
        """
        :param section_description: A string representing the description for the Curriculum Vitae section.
        """
        self.section_description = section_description
        self.statement = professional_statement()  # Fetch professional statement
        self.work_experience = load_experience_items()  # Fetch work experience data
        self.education = load_education_items()  # Fetch education data

        # Sort the work and education items by the second date in the date range (end date), in reverse order (most recent first)
        self.work_experience.sort(key=lambda x: parse_as_datetime(x['date_range'][1]), reverse=True)
        self.education.sort(key=lambda x: parse_as_datetime(x['date_range'][1]), reverse=True)

    def render(self):
        # Curriculum Vitae Header
        st.subheader("Curriculum Vitae 📜")
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.statement}</p>', unsafe_allow_html=True)

        # Work Experience Section
        st.markdown("#### Work Experience 🔧")

        st.text(CURRENT_JOB_KEYWORD)
        
        default_circle_color = "#1c7bba"  # Default circle color (blue)
        current_job_circle_color = "#ff6f00"  # Orange circle color for current jobs
        shadow_color = "rgba(28, 123, 186, 0.2)"  # Fixed shadow color

        for experience in self.work_experience:
            start_date, end_date = experience['date_range']
            
            # Special handling for current job experience
            if CURRENT_JOB_KEYWORD.strip().lower() == end_date.strip().lower():
                end_date_str = CURRENT_JOB_KEYWORD  # Keep the keyword as is for current job
                circle_color = current_job_circle_color  # Use orange for current job
            else:
                end_date_str = parse_as_datetime(end_date).strftime('%m/%Y') if end_date !=CURRENT_JOB_KEYWORD else "Present"
                circle_color = default_circle_color  # Default to blue for past jobs
            
            start_date_str = parse_as_datetime(start_date).strftime('%m/%Y')
            date_range_str = f"{start_date_str} - {end_date_str}"

            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 20px; height: 20px; 
                    border: 5px solid {circle_color}; 
                    border-radius: 50%; 
                    box-shadow: 0 0 0 5px {shadow_color}; 
                    position: relative; 
                    margin-right: 10px; 
                    margin-top: 2px;  
                '></div> 
                <div style="max-width: 500px;">
                    <strong>{experience['title']}</strong><br> 
                    <em>{experience['company']}</em><br> 
                    <p>{experience['description']}</p>
                    <p style='font-style: italic;'>{date_range_str}</p>
                </div>
            </div>""", unsafe_allow_html=True)

        # Education Section
        st.markdown("#### Education 🎓")
        
        for edu in self.education:
            start_date, end_date = edu['date_range']
            # Format date ranges to mm/yyyy
            start_date_str = parse_as_datetime(start_date).strftime('%m/%Y')
            end_date_str = parse_as_datetime(end_date).strftime('%m/%Y') if end_date != "Actualmente" else "Present"
            
            date_range_str = f"{start_date_str} - {end_date_str}"
            
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 20px; height: 20px; 
                    border: 5px solid {default_circle_color}; 
                    border-radius: 50%; 
                    box-shadow: 0 0 0 5px {shadow_color}; 
                    position: relative; 
                    margin-right: 10px; 
                    margin-top: 2px; 
                '></div> 
                <div style="max-width: 500px;">
                    <strong>{edu['title']}</strong><br> 
                    <em>{edu['institution']}</em><br> 
                    <p>{edu['description']}</p>
                    <p style='font-style: italic;'>{date_range_str}</p>
                </div>
            </div>""", unsafe_allow_html=True)



            
cv = CurriculumVitae(
    section_description="This is a description of the Curriculum Vitae section.",
)

#cv.render()

