"""
title: Curriculum Vitae
description: CV area for a modern proffesional portfolio. The gist of it is serving an elegant front end representation of a couple of unordered lists: work items, experience items. Its design is inspired by modern job intermediation sites.
"""

import streamlit as st

        
class CurriculumVitae:
    def __init__(self, section_description, statement, work_experience, education):
        """
        :param section_description: A string representing the description for the Curriculum Vitae section.
        :param statement: A string representing the main professional statement.
        :param work_experience: A list of dictionaries with keys: title, company, description, and date_range.
        :param education: A list of dictionaries with keys: title, institution, description, and date_range.
        """
        self.section_description = section_description
        self.statement = statement
        self.work_experience = work_experience
        self.education = education

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
    statement="An experienced professional with a background in software development, data science, and project management.",
    work_experience=[
        {
            'title': 'Software Developer',
            'company': 'Tech Solutions Inc.',
            'description': 'Developed and maintained software solutions for various clients, focusing on full-stack development and optimization.',
            'date_range': 'January 2020 - Present'
        },
        {
            'title': 'Data Scientist',
            'company': 'Data Insights Ltd.',
            'description': 'Applied machine learning techniques to predict consumer behavior, significantly increasing forecast accuracy.',
            'date_range': 'June 2018 - December 2019'
        }
    ],
    education=[
        {
            'title': 'B.Sc. Computer Science',
            'institution': 'University of Techville',
            'description': 'Graduated with honors in Computer Science, with a focus on artificial intelligence and software engineering.',
            'date_range': 'September 2014 - June 2018'
        },
        {
            'title': 'M.Sc. Data Science',
            'institution': 'Tech University',
            'description': 'Specialized in machine learning and big data analytics.',
            'date_range': 'September 2018 - June 2020'
        }
    ]
)

#cv.render()

