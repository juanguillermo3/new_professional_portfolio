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
        st.subheader("Curriculum Vitae")
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.section_description}</p>', unsafe_allow_html=True)

        # Main Professional Statement
        st.header("Professional Statement")
        st.markdown(f"<p style='text-align: justify;'>{self.statement}</p>", unsafe_allow_html=True)

        # Work Experience Section
        st.header("Work Experience")

        for i, experience in enumerate(sorted(self.work_experience, key=lambda x: x['date_range'], reverse=True)):
            color = "black" if i % 2 == 0 else "gray"
            st.markdown(f"<div style='color: {color}; margin-bottom: 1rem;'>", unsafe_allow_html=True)
            st.markdown(f"**{experience['title']}**, {experience['company']} ({experience['date_range']})", unsafe_allow_html=True)
            description = experience['description']
            if len(description) > 300:
                truncated_description = description[:300].rsplit(' ', 1)[0] + "..."
                st.markdown(f"{truncated_description} <a href='#' style='color: blue;'>Read more</a>", unsafe_allow_html=True)
            else:
                st.markdown(description, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Education Section
        st.header("Education")

        for edu in self.education:
            st.markdown(f"**{edu['degree']}**, {edu['institution']} ({edu['date_range']})", unsafe_allow_html=True)

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


