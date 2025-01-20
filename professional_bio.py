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
        :param education: A list of dictionaries with keys: institution, degree, and date_range.
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

        for i, experience in enumerate(sorted(self.work_experience, key=lambda x: x['date_range'], reverse=True)):
            color = "black" if i % 2 == 0 else "gray"
            st.markdown(f"<div style='color: {color}; margin-bottom: 0.5rem;'>", unsafe_allow_html=True)

            st.markdown(f"{experience['title']}", unsafe_allow_html=True)
            st.markdown(f"{experience['company']}", unsafe_allow_html=True)
            
            description = experience['description']
            truncated_description = description[:150].rsplit(' ', 1)[0] + "... "
            expanded_key = f"expanded_{i}"

            if expanded_key not in st.session_state:
                st.session_state[expanded_key] = False

            if st.session_state[expanded_key]:
                st.markdown(
                    f"{description} <a style='color: blue; text-decoration: underline; cursor: pointer;' "
                    f"onclick=\"window.sessionStorage.setItem('{expanded_key}', 'false');\">See less</a>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"{truncated_description}<a style='color: blue; text-decoration: underline; cursor: pointer;' "
                    f"onclick=\"window.sessionStorage.setItem('{expanded_key}', 'true');\">See more</a>",
                    unsafe_allow_html=True
                )

            st.markdown(f"<p style='font-style: italic;'>{experience['date_range']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Education Section
        st.markdown("#### Education")

        for edu in self.education:
            color = "black" if self.education.index(edu) % 2 == 0 else "gray"
            st.markdown(f"<div style='color: {color}; margin-bottom: 0.5rem;'>", unsafe_allow_html=True)
            
            st.markdown(f"{edu['degree']}", unsafe_allow_html=True)
            st.markdown(f"{edu['institution']}", unsafe_allow_html=True)
            st.markdown(f"<p style='font-style: italic;'>{edu['date_range']}</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    def render(self):
        # Curriculum Vitae Header
        st.subheader("Curriculum Vitae 📜")
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.statement}</p>', unsafe_allow_html=True)
    
        # Work Experience Section
        st.markdown("#### Work Experience")
    
        for i, experience in enumerate(sorted(self.work_experience, key=lambda x: x['date_range'], reverse=True)):
            # Determine the color for the circle (alternating colors for visual effect)
            circle_color = "#1c7bba" if i % 2 == 0 else "#5c9cc2"  # You can customize the colors
            shadow_color = "rgba(28, 123, 186, 0.2)" if i % 2 == 0 else "rgba(92, 156, 194, 0.2)"
            
            # Create the work experience container with a circle effect
            st.markdown(f"""
            <div style='color: {"black" if i % 2 == 0 else "gray"}; margin-bottom: 0.5rem; display: flex; align-items: center;'>
                <div style='
                    width: 20px; height: 20px; 
                    border: 5px solid {circle_color}; 
                    border-radius: 50%; 
                    box-shadow: 0 0 0 5px {shadow_color}; 
                    position: relative; 
                    margin-right: 10px;
                '></div>
                <div>
                    <strong>{experience['title']}</strong><br>
                    <em>{experience['company']}</em><br>
            """, unsafe_allow_html=True)
    
            description = experience['description']
            truncated_description = description[:150].rsplit(' ', 1)[0] + "... "
            expanded_key = f"expanded_{i}"
    
            if expanded_key not in st.session_state:
                st.session_state[expanded_key] = False
    
            if st.session_state[expanded_key]:
                st.markdown(
                    f"{description} <a style='color: blue; text-decoration: underline; cursor: pointer;' "
                    f"onclick=\"window.sessionStorage.setItem('{expanded_key}', 'false');\">See less</a>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"{truncated_description}<a style='color: blue; text-decoration: underline; cursor: pointer;' "
                    f"onclick=\"window.sessionStorage.setItem('{expanded_key}', 'true');\">See more</a>",
                    unsafe_allow_html=True
                )
    
            st.markdown(f"<p style='font-style: italic;'>{experience['date_range']}</p>", unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)  # Closing the work experience container
    
        # Education Section (now with circular design as well)
        st.markdown("#### Education")
        for i, edu in enumerate(self.education):
            # Determine the color for the circle (alternating colors for visual effect)
            circle_color = "#1c7bba" if i % 2 == 0 else "#5c9cc2"  # You can customize the colors
            shadow_color = "rgba(28, 123, 186, 0.2)" if i % 2 == 0 else "rgba(92, 156, 194, 0.2)"
            
            # Create the education item container with a circle effect
            st.markdown(f"""
            <div style='color: {"black" if i % 2 == 0 else "gray"}; margin-bottom: 0.5rem; display: flex; align-items: center;'>
                <div style='
                    width: 20px; height: 20px; 
                    border: 5px solid {circle_color}; 
                    border-radius: 50%; 
                    box-shadow: 0 0 0 5px {shadow_color}; 
                    position: relative; 
                    margin-right: 10px;
                '></div>
                <div>
                    <strong>{edu['degree']}</strong><br>
                    <em>{edu['institution']}</em><br>
                    <p style='font-style: italic;'>{edu['date_range']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)


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

    def _render_item(self, title, entity, description, date_range, index, color_odd, color_even):
        """Render a single item (work or education) with alternating colors and a circular design."""
        circle_color = color_even if index % 2 == 0 else color_odd
        shadow_color = "rgba(28, 123, 186, 0.2)" if index % 2 == 0 else "rgba(92, 156, 194, 0.2)"
        truncated_description = description[:150].rsplit(' ', 1)[0] + "... "
        expanded_key = f"expanded_{index}"

        if expanded_key not in st.session_state:
            st.session_state[expanded_key] = False

        st.markdown(f"""
        <div style='color: {"black" if index % 2 == 0 else "gray"}; margin-bottom: 1rem; display: flex; align-items: center;'>
            <div style='
                width: 20px; height: 20px;
                border: 5px solid {circle_color};
                border-radius: 50%;
                box-shadow: 0 0 0 5px {shadow_color};
                position: relative;
                margin-right: 10px;
            '></div>
            <div>
                <strong>{title}</strong><br>
                <em>{entity}</em><br>
        """, unsafe_allow_html=True)

        if st.session_state[expanded_key]:
            st.markdown(
                f"{description} <a style='color: blue; text-decoration: underline; cursor: pointer;' "
                f"onclick=\"window.sessionStorage.setItem('{expanded_key}', 'false');\">See less</a>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"{truncated_description}<a style='color: blue; text-decoration: underline; cursor: pointer;' "
                f"onclick=\"window.sessionStorage.setItem('{expanded_key}', 'true');\">See more</a>",
                unsafe_allow_html=True
            )

        st.markdown(f"<p style='font-style: italic;'>{date_range}</p>", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    def render(self):
        # Curriculum Vitae Header
        st.subheader("Curriculum Vitae 📜")
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.statement}</p>', unsafe_allow_html=True)

        # Work Experience Section
        st.markdown("#### Work Experience")
        for i, experience in enumerate(sorted(self.work_experience, key=lambda x: x['date_range'], reverse=True)):
            self._render_item(
                experience['title'],
                experience['company'],
                experience['description'],
                experience['date_range'],
                i,
                "#1c7bba",
                "#5c9cc2"
            )

        # Education Section
        st.markdown("#### Education")
        for i, edu in enumerate(sorted(self.education, key=lambda x: x['date_range'], reverse=True)):
            self._render_item(
                edu['title'],
                edu['institution'],
                edu['description'],
                edu['date_range'],
                i,
                "#1c7bba",
                "#5c9cc2"
            )


# Example usage
section_description = (
    "I am a Colombian Economist with a professional background as a research assistant, "
    "remote data analyst, and also as a freelance consultant in the development of Machine Learning technologies. "
    "The focus of my current professional offering is on Machine Learning Engineering."
)

work_experience = [
    {
        "title": "Machine Learning Engineer",
        "company": "TechCorp",
        "description": "Developed and deployed machine learning models for predictive analytics in a cloud environment. Collaborated with cross-functional teams to improve data pipelines and model performance.",
        "date_range": "2020 - Present"
    },
    {
        "title": "Data Analyst",
        "company": "DataWorks",
        "description": "Analyzed complex datasets to provide actionable insights for clients. Created interactive dashboards and reports to visualize key performance indicators.",
        "date_range": "2018 - 2020"
    }
]

education = [
    {
        "institution": "University of Colombia",
        "degree": "Bachelor's in Economics",
        "date_range": "2014 - 2018"
    }
]

cv = CurriculumVitae(section_description, section_description, work_experience, education)


