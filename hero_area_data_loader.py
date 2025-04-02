import streamlit as st
import os
import json
from dotenv import load_dotenv
from exceptional_ui import (
    html_for_tooltip_from_large_list,
    setup_tooltip_behavior
)
from front_end_utils import render_section_separator
import hashlib
import datetime
from expandable_text import _chunk_texts, expandable_text_html
import markdown

# Load environment variables
load_dotenv()

# Retrieve the mock prefix from the environment, defaulting to "[MOCK TOOLTIP]" if not set
MOCK_INFO_PREFIX = os.getenv("MOCK_INFO", "[MOCK INFO]")

#
# (0)
#
def load_avatar_caption():
    return "God told me I could either be good-looking or an excellent worker."
#
# (1)
#
def load_quote():
    return [
        "My permanent professional effort is the <b>modernization of data analysis</b> "  
        "through <b>research and development</b> of cutting-edge techniques, such as flexible statistical inference of predictive patterns powered by <b>Machine Learning</b>, "  
        "streamlining <em>core business workflows</em> through <b>software development</b> and <b>algorithmic automation</b>, "
        "handling <em>enterprise-grade datasets</em> with <b>modern data technology</b>, "  
        "grouping data by <em>meaning</em> with <b>Natural Language Processing</b>, "  
        "and enabling dynamically <em>decision-making</em> through the <b>agency of Large Language Models.</b> "
    ]
#
# (2)
#
def load_code_samples():
    return [
        {"title": "🚀 Genetic Algorithms for forecasting app sales", "url": "https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz"},
        {"title": "🧩 Ensemble Learning for automated hiring in Human Resources", "url": "https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvAO"}
    ]
#
# (3)
#
def load_detailed_offerings():
    offerings = [
        {
            "title": "⚡ 1. High-Performance Prediction of Key Business Outcomes",
            "description": "I implement <em>statistically driven inference</em> of predictive patterns powered by <em>Machine Learning</em> "
                           "and <em>Deep Learning</em> algorithms. Applications range from forecasting "
                           "the macroeconomic/financial environment to <em>fine-grained predictions</em> from business micro-data (sales forecasting, churn modeling, engagement models).",
            "skills": [
                "Familiarity with predictive algorithms for regression, classification, and forecasting problems.", 
                "Strong grasp of Linear Regression.", 
                "Deep understanding of Machine Learning algorithms for detecting predictive patterns.", 
                "Mastery of the statistical learning workflow for implementing and calibrating predictive models.", 
                "Expert in the development of search and optimization techniques to discover better predictive models."
            ]
        },
        {
            "title": "🔌 2. Sharing Actionable Insights Through Software and Application Development",
            "description": "I develop software applications (batch scripts, APIs, dashboards, web applications) to distribute insights "
                           "and predictions across corporate environments.",
            "skills": [
                "Strong grasp of software engineering best practices.", 
                "Familiarity with software engineering methodologies, architectural models, and design patterns.", 
                "Expertise in developing code using Object-Oriented, Functional, and Asynchronous programming styles.", 
                "Efficient at learning and utilizing new libraries for application development."
            ]
        },
        {
            "title": "🧩 3. Forging Key Datasets from Primary Sources",
            "description": 'As my former boss '
                           '<a href="https://www.linkedin.com/in/susana-mart%C3%ADnez-restrepo-ph-d-1314b137/" target="_blank" style="color: #0073b1; text-decoration: none;">'
                           'Susana Martinez Restrepo</a> said, <em>I can perform data miracles.</em> '
                           'This refers to my ability to clean and organize datasets from complex, multi-source environments '
                           'for research and model development.',
            "skills": [
                "Activate implicit datasets by ETL effort from enterprise systems",
                "Flexible information processing using text-minning, ReGex and Natural-Language-Processing",
                "Familiarity with algorithms for alternative/unstructured data sources (NLP, GIS, Network Data)",
                "Expertise developing complex merges from multiple data sources"
            ]
        },
        {
            "title": "🛠️ 4. Fast Learning of Modern Data Stacks",
            "description": "I integrate tools and technologies for modern data analysis, committing to research the "
                           "unique purposes of each tool and efficiently write workflows around them using GPT.",
            "subitems": [
                "<strong>Excellence Tier (I know the code line by heart):</strong> Python, R Studio, Stata, GPT",
                "<strong>Proficiency Tier:</strong> Airflow, SQL, Spark, Bash scripting",
                "<strong>Currently Learning:</strong> Docker, Kubernetes, GitHub, Big Data Cloud tools, SQLAlchemy, Django"
            ],
            "skills2": [
                "Data integration expertise: Can connect enterprise applications with internal and external datasources: APIs, web scraping applications, databases, unstructured datasources",
                "Activate implicit datasets by ETL effort from enterprise systems",
                "Flexible information processing using text-minning, regex, Natural-Language-Processing",
                "Familiarity with algorithms for alternative/unstructured data sources (NLP, GIS, Network Data)",
                "Expertise developing complex merges from multiple data sources"
            ]
        },
        {
            "title": "🛸 5. Unpacking Artificial Intelligence for Data Analysis",
            "description": "I prepare myself by means of self-learning for the disruption of Artificial Intelligence in software development and the rise of LLM-powered applications."
        },
        {
            "title": "⚖️ (Bonus) Rigorous Economic Mindset",
            "description": "As a professional economist, I over-simplify complex social phenomena by casually referencing supply and demand (kidding!). "
                           "But really, I approach data analysis with a focus on causal reasoning, marginal effects, and counterfactual analysis."
        }
    ]
    return offerings










