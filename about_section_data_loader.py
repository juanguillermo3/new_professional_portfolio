import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read the career start date from .env or default to June 2019
CAREER_START_DATE = os.getenv("CAREER_START_DATE", "2019-06-01")
career_start_year = datetime.strptime(CAREER_START_DATE, "%Y-%m-%d").year
current_year = datetime.now().year
num_years = current_year - career_start_year

# Hardcoded LinkedIn profile URL
LINKEDIN_PROFILE = "https://www.linkedin.com/in/juan-guillermo-osio/"

def load_general_info():
    """
    Load general information for the About section.
    
    Returns:
        str: A brief description of the portfolio's purpose and scope.
    """
    return (
        f"This portfolio showcases code samples I have developed over more than {num_years} years as a Data Analyst "
        "and ML Consultant across various projects. You'll likely find my work quite eclectic, as I have worked on a range "
        "of subjects as varied as the role of gender in the Colombian labor market, ethology research on monkey behavior, "
        "sales forecasting for delivery services, recommendation of optimal store placement, setup of key dashboards/reporting "
        "for financial departments, and more."
    )

def load_key_interest():
    """
    Load the key interest statement.

    Returns:
        str: The key interest text.
    """
    return """
    🔑 My recurring interest nevertheless has always been the **modernization of the data analysis pipeline** 
    through cutting-edge techniques, such as **flexible** ML-based inference, **software** and **algorithmic automation**, 
    assimilation of **data-related technology**, using **NLP** in latent semantic spaces, and, more recently, solving data analysis tasks 
    through **agency formation** within **LLM applications**.
    """

def load_key_hypothesis():
    """
    Load the key hypothesis statement.

    Returns:
        str: The key hypothesis text.
    """
    return f"""
    🔬 This portfolio was created with two key goals in mind. First, it brings to life a **Recommendation System (RecSys)** 
    as a core feature to showcase my work to interested parties. More broadly, as a **heterodox economist** concerned with 
    the smooth functioning of the labor market, this project allows me to assess the value of emerging technologies—such as 
    **RecSys**, **LLM-powered applications (LLM apps)**, and **software-based automation**—in addressing common struggles 
    faced by workers. My key empirical hypothesis is that **RecSys can serve dynamic, context-dependent representations of a 
    professional portfolio**, mitigating trade-offs between specialization and market penetration. Features such as the **RecSys** 
    are still under development, and related research can be found on my 
    <a href="{LINKEDIN_PROFILE}" target="_blank" style="color: #1f77b4; text-decoration: none;">**LinkedIn profile**</a>.
    """


def load_dev_environment():
    """
    Load the development environment description.

    Returns:
        str: The development environment description.
    """
    return """
    🛠️ This portfolio is a **Python/Streamlit web application** with a **modular design** inspired by **microservice 
    architecture**, adapted for a professional site. It follows **OOP principles** and **SOLID design patterns**, 
    with modules organized by responsibility. The **full codebase** is available on 
    <a href="https://github.com/juanguillermo3/new_professional_portfolio/tree/main" 
    target="_blank" style="color: #1f77b4; text-decoration: none;">**GitHub**</a>. 
    """

