# cv_data_loader.py

import json
import pandas as pd

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
            "date_range": "Julio 2022 - Actualmente"
        },
        {
            "title": "Freelance ML Consultant/Developer (Ensemble Learning)",
            "company": "Private Client",
            "description": (
                "The client had a set of ML classifiers to automate an HR department's hiring process and asked "
                "for guidance on combining them into a superior predictive system. I created a configurable ensemble "
                "module to merge predictions from multiple classifiers and found that many non-singleton ensembles "
                "outperformed individual models in terms of F1 score. Code sample available at: "
                "https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvA"
            ),
            "date_range": "Enero 2024 - Julio 2024"
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
            "date_range": "Junio 2023 - Diciembre 2023"
        },
        {
            "title": "Freelance ML Consultant/Developer (AI and Genetic Algorithms)",
            "company": "Private Client",
            "description": (
                "This consultancy focused on developing a high-performance forecasting system for Business Intelligence, "
                "targeting 1-month-ahead hourly forecasts. In Stage 1, I delivered traditional (ARIMA, Exponential Smoothing) "
                "and Deep Learning (DNN, RNN, LSTM) algorithms. In Stage 2, I implemented a custom Genetic Optimization Algorithm "
                "to find near-optimal Neural Network architectures. Code sample available at: "
                "https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz"
            ),
            "date_range": "Enero 2023 - Julio 2023"
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
            "date_range": "Julio 2019 - Julio 2022"
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
            "date_range": "Enero 2012 - Junio 2019"
        }
    ]
    
    return education_items


def professional_statement():
    """
    Fetches or generates the professional statement.
    Can be extended to fetch from a file, API, or database.
    """
    return "Experienced software developer and data scientist with a passion for solving complex problems using data-driven solutions. Adept at both collaborative and independent work in fast-paced environments."

