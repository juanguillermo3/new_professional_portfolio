"""
title: Curriculum Vitae
description: CV area for a modern proffesional portfolio. The gist of it is serving an elegant front end representation of a couple of unordered lists: work items, experience items. Its design is inspired by modern job intermediation sites.
"""

import streamlit as st
from cv_data_loader import load_experience_items, load_education_items, professional_statement

class CurriculumVitae:
    def __init__(self, section_description):
        """
        :param section_description: A string representing the description for the Curriculum Vitae section.
        """
        self.section_description = section_description
        self.statement = professional_statement()  # Fetch professional statement
        self.work_experience = load_experience_items()  # Fetch work experience data
        self.education = load_education_items()  # Fetch education data

    def render(self):
        # Curriculum Vitae Header
        st.subheader("Curriculum Vitae 📜")
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.statement}</p>', unsafe_allow_html=True)

        # Work Experience Section
        st.markdown("#### Work Experience")
        
        circle_color = "#1c7bba"  # Fixed circle color
        shadow_color = "rgba(28, 123, 186, 0.2)"  # Fixed shadow color

        for experience in self.work_experience:
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 20px; height: 20px; 
                    border: 5px solid {circle_color}; 
                    border-radius: 50%; 
                    box-shadow: 0 0 0 5px {shadow_color}; 
                    position: relative; 
                    margin-right: 10px; 
                    margin-top: 2px;  /* Align the circle with the top of the title */
                '></div> 
                <div style="max-width: 500px;">  <!-- Fixed width for descriptions -->
                    <strong>{experience['title']}</strong><br> 
                    <em>{experience['company']}</em><br> 
                    <p>{experience['description']}</p>
                    <p style='font-style: italic;'>{experience['date_range']}</p>
                </div>
            </div>""", unsafe_allow_html=True)

        # Education Section
        st.markdown("#### Education")
        
        for edu in self.education:
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 20px; height: 20px; 
                    border: 5px solid {circle_color}; 
                    border-radius: 50%; 
                    box-shadow: 0 0 0 5px {shadow_color}; 
                    position: relative; 
                    margin-right: 10px; 
                    margin-top: 2px;  /* Align the circle with the top of the title */
                '></div> 
                <div style="max-width: 500px;">  <!-- Fixed width for descriptions -->
                    <strong>{edu['title']}</strong><br> 
                    <em>{edu['institution']}</em><br> 
                    <p>{edu['description']}</p>  <!-- Add description -->
                    <p style='font-style: italic;'>{edu['date_range']}</p>
                </div>
            </div>""", unsafe_allow_html=True)


    def render(self):
        # Curriculum Vitae Header
        st.subheader("Curriculum Vitae 📜")
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.statement}</p>', unsafe_allow_html=True)

        # Work Experience Section
        st.markdown("#### Work Experience")
        
        circle_color = "#1c7bba"  # Fixed circle color
        shadow_color = "rgba(28, 123, 186, 0.2)"  # Fixed shadow color

        for experience in self.work_experience:
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 20px; height: 20px; 
                    border: 5px solid {circle_color}; 
                    border-radius: 50%; 
                    box-shadow: 0 0 0 5px {shadow_color}; 
                    position: relative; 
                    margin-right: 10px; 
                    margin-top: 2px;  /* Align the circle with the top of the title */
                '></div> 
                <div style="max-width: 500px;">  <!-- Fixed width for descriptions -->
                    <strong>{experience['title']}</strong><br> 
                    <em>{experience['company']}</em><br> 
                    <p>{experience['description']}</p>
                    <p style='font-style: italic;'>{experience['date_range']}</p>
                </div>
            </div>""", unsafe_allow_html=True)

        # Education Section
        st.markdown("#### Education")
        
        for edu in self.education:
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 20px; height: 20px; 
                    border: 5px solid {circle_color}; 
                    border-radius: 50%; 
                    box-shadow: 0 0 0 5px {shadow_color}; 
                    position: relative; 
                    margin-right: 10px; 
                    margin-top: 2px;  /* Align the circle with the top of the title */
                '></div> 
                <div style="max-width: 500px;">  <!-- Fixed width for descriptions -->
                    <strong>{edu['title']}</strong><br> 
                    <em>{edu['institution']}</em><br> 
                    <p>{edu['description']}</p>  <!-- Add description -->
                    <p style='font-style: italic;'>{edu['date_range']}</p>
                </div>
            </div>""", unsafe_allow_html=True)

            
cv = CurriculumVitae(
    section_description="This is a description of the Curriculum Vitae section.",
)

#cv.render()

