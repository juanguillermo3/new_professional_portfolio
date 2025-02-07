"""
title: Curriculum Vitae
description: CV area for a modern proffesional portfolio. The gist of it is serving an elegant front end representation of a couple of unordered lists: work items, experience items. Its design is inspired by modern job intermediation sites.
"""

def render_expandable_text(text, limit=300):
    """Renders an expandable text component with 'Read more' functionality."""
    unique_id = hash(text)  # Unique ID for each block to avoid conflicts

    if len(text) <= limit:
        return text  # No need for expansion

    short_text = text[:limit] + "..."
    full_text = text

    html_code = f"""
    <span id="short_{unique_id}">{short_text}</span>
    <span id="full_{unique_id}" style="display: none;">{full_text}</span>
    <a href="javascript:void(0);" id="btn_{unique_id}" onclick="toggleText('{unique_id}')"> Read more</a>

    <script>
    function toggleText(id) {{
        var shortText = document.getElementById("short_" + id);
        var fullText = document.getElementById("full_" + id);
        var btnText = document.getElementById("btn_" + id);

        if (fullText.style.display === "none") {{
            fullText.style.display = "inline";
            shortText.style.display = "none";
            btnText.innerHTML = " Read less";
        }} else {{
            fullText.style.display = "none";
            shortText.style.display = "inline";
            btnText.innerHTML = " Read more";
        }}
    }}
    </script>
    """
    return html_code  # Return as string to inject into Markdown
    

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
            end_date_str = CURRENT_JOB_KEYWORD if is_current_job else parse_as_datetime(end_date).strftime('%m/%Y')
    
            start_date_str = parse_as_datetime(start_date).strftime('%m/%Y')
            date_range_str = f"{start_date_str} - {end_date_str}"
    
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
        st.markdown("#### Education 🎓")
    
        for edu in self.education:
            start_date, end_date = edu['date_range']
            # Format date ranges to mm/yyyy
            start_date_str = parse_as_datetime(start_date).strftime('%m/%Y')
            end_date_str = parse_as_datetime(end_date).strftime('%m/%Y') if end_date != CURRENT_JOB_KEYWORD else "Present"
            
            date_range_str = f"{start_date_str} - {end_date_str}"
            
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

    def render(self):
        # Curriculum Vitae Header
        st.subheader("Curriculum Vitae 📜")
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.statement}</p>', unsafe_allow_html=True)
    
        # Work Experience Section
        st.markdown("#### Work Experience 🔧")
    
        # Predefined Colors
        circle_color = "#1c7bba"  # Default circle color (blue)
        shadow_circle_color = "rgba(28, 123, 186, 0.2)"  # Default shadow (soft blue)
        
        current_circle_color = "#ff6f00"  # Orange for current job
        shadow_current_circle_color = "rgba(255, 111, 0, 0.2)"  # Soft orange shadow
    
        for experience in self.work_experience:
            start_date, end_date = experience['date_range']
    
            # Determine if this is the current job
            is_current_job = end_date.strip().lower() == "present"
    
            # Assign colors based on whether it is the current job
            display_circle_color = current_circle_color if is_current_job else circle_color
            display_shadow_color = shadow_current_circle_color if is_current_job else shadow_circle_color
            end_date_str = "Present" if is_current_job else end_date
    
            date_range_str = f"{start_date} - {end_date_str}"

            # Convert long descriptions into expandable versions
            expandable_description = render_expandable_text(experience['description'], 250)

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
                    <p>{expandable_description}</p>
                    <p style='font-style: italic;'>{date_range_str}</p>
                </div>
            </div>""", unsafe_allow_html=True)
    
        # Education Section
        st.markdown("#### Education 🎓")
    
        for edu in self.education:
            start_date, end_date = edu['date_range']
            end_date_str = "Present" if end_date.strip().lower() == "present" else end_date
            date_range_str = f"{start_date} - {end_date_str}"

            # Convert long descriptions into expandable versions
            expandable_description = render_expandable_text(edu['description'], 250)
            
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
                    <p>{expandable_description}</p>
                    <p style='font-style: italic;'>{date_range_str}</p>
                </div>
            </div>""", unsafe_allow_html=True)

            
cv = CurriculumVitae(
    section_description="This is a description of the Curriculum Vitae section.",
)

#cv.render()

