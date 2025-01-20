# cv_data_loader.py
import json

# cv_data_loader.py

def experience_items():
    """
    Fetches or generates a list of real work experience items.
    """
    return [
        {
            'title': 'Freelance Data Analyst & R Developer',
            'company': 'Private client',
            'description': 'A biology Ph.D. aspirant conducted ethology research on monkey behavior in the Australian jungle, gathering data on four species, covering behaviors...',
            'date_range': 'Julio 2022 - Actualmente'
        },
        {
            'title': 'Freelance ML consultant/Developer (Ensemble Learning)',
            'company': 'Private client',
            'description': 'The client had a set of ML classifiers to automate an HR department\'s hiring process and asked for guidance on combining them into a superior predictive system. I created a configurable ensemble module to merge predictions from multiple classifiers and found that many non-singleton ensembles outperformed individual models in terms of F1 score.',
            'date_range': 'Enero 2024 - Julio 2024'
        },
        {
            'title': 'Python Developer',
            'company': 'Algotrading',
            'description': 'I was hired as a data analyst and developer by an international start-up focused on real-time trading using NLP signals. I maintained mission-critical code for real-time feature engineering of trade signals, performed SOLID refactoring, developed visualizations of the codebase structure, and integrated logging with AWS Watchtower.',
            'date_range': 'Junio 2023 - Diciembre 2023'
        },
        {
            'title': 'Freelance ML consultant/Developer (AI and Genetic Algorithms)',
            'company': 'Private client',
            'description': 'This consultancy focused on developing a high-performance forecasting system for Business Intelligence, targeting 1-month-ahead hourly forecasts. I delivered traditional (ARIMA, Exponential Smoothing) and Deep Learning (DNN, RNN, LSTM) algorithms. In Stage 2, I implemented a custom Genetic Optimization Algorithm to find near-optimal Neural Network architectures.',
            'date_range': 'Enero 2023 - Julio 2023'
        },
        {
            'title': 'Data Analyst, Public policy research assistant',
            'company': 'Corewoman',
            'description': 'In this role, I enabled empirical research on the impact of gender in the Colombian labor market for public policy. I engaged with complex, multi-source environments, utilizing both structured and unstructured data. I delivered data gathering and transformation pipelines using Stata, R, and Python.',
            'date_range': 'Julio 2019 - Julio 2022'
        }
    ]

def education_items():
    """
    Fetches or generates a list of real education items.
    """
    return [
        {
            'title': 'Economics Degree',
            'institution': 'Universidad de los Andes',
            'description': 'College educated me on social and corporate systems being statistically patterned—hence the unreasonable effectiveness of regression analysis and applied statistical modeling. I acquired excellent programming skills to effectively deploy statistical analysis in any empirical environment.',
            'date_range': 'Enero 2012 - Junio 2019'
        }
    ]

def professional_statement():
    """
    Fetches or generates the professional statement.
    """
    return "Mis experiencias profesionales"


def professional_statement():
    """
    Fetches or generates the professional statement.
    Can be extended to fetch from a file, API, or database.
    """
    return "Experienced software developer and data scientist with a passion for solving complex problems using data-driven solutions. Adept at both collaborative and independent work in fast-paced environments."

