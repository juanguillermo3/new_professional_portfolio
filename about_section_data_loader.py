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

def load_general_info():
    """
    Load general information for the About section.
    
    Returns:
        str: A brief description of the portfolio's purpose and scope.
    """
    return (
        f"This portfolio showcases code samples I have developed over more than {num_years} years as a Data Analyst "
        "and ML Consultant across various projects. You'll likely find my work quite eclectic, as I have explored topics "
        "as varied as the impact of gender on the Colombian labor market and scientific research on monkey behavior "
        "to high-performance sales forecasting for food delivery services. My recurring interest nevertheless has always "
        "been the modernization of the data analysis pipeline through cutting-edge techniques, such as flexible ML-based "
        "inference, software and algorithmic automation, using NLP in latent semantic spaces, and, more recently, solving "
        "data analysis tasks through agency formation within LLM applications."
    )
