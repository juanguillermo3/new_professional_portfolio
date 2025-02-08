import streamlit as st
from cv_data_loader import (
    load_experience_items,
    load_education_items,
    professional_statement,
    parse_as_datetime,
    format_date_for_frontend,
    CURRENT_JOB_KEYWORD,
)

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
        st.subheader("Curriculum Vitae \ud83d\udc1c")
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.statement}</p>', unsafe_allow_html=True)
    
        # Work Experience Section
        st.markdown("#### Work Experience \ud83d\udee0\ufe0f")
    
        # Predefined Colors
        circle_color = "#1c7bba"  # Default circle color (blue)
        shadow_circle_color = "rgba(28, 123, 186, 0.2)"  # Default shadow (soft blue)
        
        current_circle_color = "#ff6f00"  # Orange for current job
        shadow_current_circle_color = "rgba(255, 111, 0, 0.2)"  # Soft orange shadow
    
        for experience in self.work_experience:
            start_date, end_date = experience['date_range']
    
            # Determine if this is the current job
            is_current_job = CURRENT_JOB_KEYWORD.strip().lower() == end_date.strip().lower()
    
            # Assign colors based on whether it is the current job
            display_circle_color = current_circle_color if is_current_job else circle_color
            display_shadow_color = shadow_current_circle_color if is_current_job else shadow_circle_color
            
            date_range_str = f"{format_date_for_frontend(start_date)} - {format_date_for_frontend(end_date)}"
    
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 20px; height: 20px; 
                    border: 5px solid {display_circle_color}; 
                    border-radius: 50%; 
                    box-shadow: 0 0 0 5px {display_shadow_color}; 
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
        st.markdown("#### Education \ud83c\udf93")
    
        for edu in self.education:
            start_date, end_date = edu['date_range']
            
            date_range_str = f"{format_date_for_frontend(start_date)} - {format_date_for_frontend(end_date)}"
            
            st.markdown(f"""<div style='margin-bottom: 0.5rem; display: flex; align-items: flex-start;'>
                <div style='
                    width: 20px; height: 20px; 
                    border: 5px solid {circle_color}; 
                    border-radius: 50%; 
                    box-shadow: 0 0 0 5px {shadow_circle_color}; 
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
    section_description="This is a description of the Curriculum Vitae section."
)


