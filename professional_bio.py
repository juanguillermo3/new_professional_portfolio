import streamlit as st
from textwrap import shorten

class CurriculumVitae:
    def __init__(self, professional_statement, work_experience, education):
        """
        :param professional_statement: A single string representing the main professional statement.
        :param work_experience: A list of dictionaries, each containing "title", "company", "description", and "date_range".
        :param education: A list of dictionaries, each containing "degree", "institution", and "date_range".
        """
        self.professional_statement = professional_statement
        self.work_experience = work_experience
        self.education = education

    def render(self):
        st.subheader("Curriculum Vitae")
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.professional_statement}</p>', unsafe_allow_html=True)

        # Work Experience Section
        st.markdown("### Work Experience")
        for index, experience in enumerate(reversed(self.work_experience)):
            color = "black" if index % 2 == 0 else "gray"
            st.markdown(
                f'<ul style="list-style-position: inside; margin-left: 20px;">
                    <li style="margin-bottom: 20px;">
                        <p style="color: {color}; font-weight: bold;">{experience["title"]}</p>
                        <p style="color: {color};">{experience["company"]}</p>
                        <p style="color: {color};">
                            {shorten(experience["description"], width=150, placeholder="... ")}
                            <a href="#" style="color: {color}; text-decoration: underline;">See more</a>
                        </p>
                        <p style="color: {color}; font-style: italic;">{experience["date_range"]}</p>
                    </li>
                </ul>', unsafe_allow_html=True
            )

        # Education Section
        st.markdown("### Education")
        for index, edu in enumerate(reversed(self.education)):
            color = "black" if index % 2 == 0 else "gray"
            st.markdown(
                f'<ul style="list-style-position: inside; margin-left: 20px;">
                    <li style="margin-bottom: 20px;">
                        <p style="color: {color}; font-weight: bold;">{edu["degree"]}</p>
                        <p style="color: {color};">{edu["institution"]}</p>
                        <p style="color: {color}; font-style: italic;">{edu["date_range"]}</p>
                    </li>
                </ul>', unsafe_allow_html=True
            )


# Example usage
section_description = "This section provides a comprehensive overview of my professional background, including my main statement, work experience, and education."
statement = (
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

cv = CurriculumVitae(section_description, statement, work_experience, education)
#cv.render()




