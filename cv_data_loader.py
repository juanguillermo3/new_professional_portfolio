import json
import pandas as pd
from datetime import datetime
import os

# Global constants (can be loaded from environment or defaults)
DATE_FORMAT = os.getenv('DATE_FORMAT', '%d/%m/%Y')  # Default format: dd/mm/yyyy
CURRENT_JOB_KEYWORD = os.getenv('CURRENT_JOB_KEYWORD', 'Nowadays')  # Default keyword: 'Actualmente'
 
# Helper utility to parse dates, treating the special keyword for current job
def parse_as_datetime(date_str):
    """
    Parses a string as a datetime object. If the string contains the CURRENT_JOB_KEYWORD, 
    it returns the current system date.

    :param date_str: The date string to parse.
    :return: A datetime object representing the parsed date.
    """
    if date_str.lower() == CURRENT_JOB_KEYWORD.lower():
        return datetime.now()  # Return current system date if special keyword is found
    try:
        # Attempt to parse the date string using the default date format
        return datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        # Handle the case where the date format is invalid or unrecognized
        raise ValueError(f"Invalid date format for '{date_str}', expected format is '{DATE_FORMAT}'.")

def load_experience_items():
    experience_items = [
        {
            "title": "Freelance Data Analyst & R Developer",
            "company": "Private Client",
            "description": (
                "A biology Ph.D. aspirant conducted ethology research on monkey behavior in the "
                "Australian jungle, gathering data on four species, covering behaviors, diet, "
                "vegetation, and habitat. Statistical analysis in R aimed to explore how monkeys allocate "
                "their time to behaviors and how contextual (hour, season, weather, species) and individual "
                "covariates (sex, groups) influence this. Data processing, visualization, and statistical tests "
                "(Kruskal-Wallis, Dunn test) were automated for streamlined reporting."
            ),
            "date_range": ("01/07/2022", CURRENT_JOB_KEYWORD)
        },
        {
            "title": "Freelance ML Consultant/Developer (Ensemble Learning)",
            "company": "Private Client",
            "description": (
                "The client had a set of ML classifiers to automate an HR department's hiring process and asked "
                "for guidance on combining them into a superior predictive system. I created a configurable ensemble "
                "module to merge predictions from multiple classifiers and found that many non-singleton ensembles "
                "outperformed individual models in terms of F1 score. Code sample available at: "
                "<a href='https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvA' target='_blank'>Google Colab</a>"
            ),
            "date_range": ("01/01/2024", "01/07/2024")
        },
        {
            "title": "Python Developer",
            "company": "Algotrading",
            "description": (
                "I was hired as a data analyst and developer by an international start-up focused on real-time trading "
                "using NLP signals. I maintained mission-critical code for real-time feature engineering of trade signals, "
                "performed SOLID refactoring, developed visualizations of the codebase structure, and integrated logging "
                "with AWS Watchtower. Through on-the-job training, I honed my skills as a low-code developer, assimilating "
                "a tech stack involving GPT and Copilot to enhance workflow efficiency."
            ),
            "date_range": ("01/06/2023", "31/12/2023")
        },
        {
            "title": "Freelance ML Consultant/Developer (AI and Genetic Algorithms)",
            "company": "Private Client",
            "description": (
                "This consultancy focused on developing a high-performance forecasting system for Business Intelligence, "
                "targeting 1-month-ahead hourly forecasts. In Stage 1, I delivered traditional (ARIMA, Exponential Smoothing) "
                "and Deep Learning (DNN, RNN, LSTM) algorithms. In Stage 2, I implemented a custom Genetic Optimization Algorithm "
                "to find near-optimal Neural Network architectures. Code sample available at: "
                "<a href='https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz' target='_blank'>Google Colab</a>"
            ),
            "date_range": ("01/01/2023", "01/07/2023")
        },
        {
            "title": "Data Analyst, Public Policy Research Assistant",
            "company": "Corewoman",
            "description": (
                "In this role, I enabled empirical research on the impact of gender in the Colombian labor market for public policy. "
                "I engaged with complex, multi-source environments, utilizing both structured and unstructured data. I delivered data "
                "gathering and transformation pipelines using Stata, R, and Python. Additionally, I provided inferential statistics, "
                "regression analysis, and program evaluation techniques, including propensity score matching (PSM)."
            ),
            "date_range": ("01/07/2019", "01/07/2022")
        }
    ]
    
    return experience_items

def load_education_items():
    education_items = [
        {
            "title": "Economics",
            "institution": "Universidad de los Andes",
            "description": (
                "I hold a degree in Economics from Universidad de los Andes. In a few words, college educated me on social and "
                "corporate systems being statistically patterned—hence the unreasonable effectiveness of regression analysis and "
                "applied statistical modeling. A secondary highlight of my time in college was acquiring excellent programming skills "
                "to effectively deploy statistical analysis in any empirical environment. In economics, measurement is king, and "
                "effectively handling empirical tasks was repeatedly reinforced through many courses until it became second nature to me. "
                "Beyond a mandatory training as an economist, which mostly covered neoclassical economics, I delved deep into data "
                "analysis and techniques available through non-mandatory master level college courses, comprehending artificial intelligence, "
                "advanced econometrics, data mining (machine learning), forecasting, and big data, for which I hold their respective certifications."
            ),
            "date_range": ("01/01/2012", "01/06/2019")
        }
    ]
    
    return education_items


def professional_statement():
    """
    Fetches or generates the professional statement.
    Can be extended to fetch from a file, API, or database.
    """
    return (
        "I am a Colombian economist with a professional background as a quantitative research assistant, remote data analyst, "
        "remote Python developer, and freelance consultant in the development of machine learning technologies, with over 5 years "
        "of experience delivering data analysis services (mostly acquired in start-ups and freelance contexts). The focus of my "
        "current professional offering is on Data Analysis and Machine Learning engineering—making data analysis actionable through "
        "software automation."
    )



