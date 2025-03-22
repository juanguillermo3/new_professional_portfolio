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

# Load environment variables
load_dotenv()

# Retrieve the mock prefix from the environment, defaulting to "[MOCK TOOLTIP]" if not set
MOCK_INFO_PREFIX = os.getenv("MOCK_INFO", "[MOCK INFO]")

def load_quote():
    return [
        "<b>Modern data analysis</b> requires engaging with and developing <b>substantial software</b>, "  
        "such as <b>data gathering, processing, and visualization applications</b>. "  
        "Moreover, <b>software automation</b> is key for <b>distributing inferences</b> from <b>statistical analysis</b>, "  
        "whether derived from <b>econometric models</b> or <b>machine learning predictions</b>. "  
        "Bottom line: I recognize the deep connection between <b>data analysis</b> and <b>software development</b>, "  
        "hence my effort to <b>serve them within a unified framework</b>." ,
            
        "I am Juan Guillermo, a professional economist. "  
        "I have built my career developing <b>data analysis</b> and <b>software application</b> scripts "  
        "for <b>research</b> and <b>operational environments</b>. "  
        "My business is discovering the best <b>abstractions</b> to <b>effectively work with data</b>, "  
        "implementing them with <b>software engineering standards</b> to build up <b>data-driven intelligence</b> "  
        "for key corporate and social systems. "
        "I can solve data engineering, statistical modelling, and software application tasks",
        
        "My broader professional vision interconnects all the key technologies essential for modern data analysis—"  
        "spanning <b>data mining</b>, <b>artificial intelligence models</b>, <b>algorithms</b>, <b>software engineering workflows</b>, "  
        "and <b>information tools</b>—into a cohesive and holistic framework."  

    ]


def load_quote():
    return [
        "My recurring interest has been the <b> modernization of data analysis</b> through cutting-edge techniques, "  
        "such as  flexible statistical inference powered by <b>Machine Learning</b>, "
        "streamlining core <em>business workflows</em> by <b>software development</b> and <b>algorithmic automation</b>, "
        "tackling datasets with <b>modern data tech stacks</b>, "
        "groupping data by <em>meaning</em> in with <b>Natural Language Processing</b>, "
        "and dynamicall <em>decision making</em>  through the  <b>agency of LLM applications </b>.",

        "I am Juan Guillermo, a professional economist. "  
        "I have built my career developing <b>data analysis</b> and <b>software application</b> scripts "  
        "for <b>research</b> and <b>operational environments</b>. "  
        "My business is discovering the best <b>abstractions</b> to <b>effectively work with data</b>, "  
        "implementing them with <b>software engineering standards</b> to build up <b>data-driven intelligence</b> "  
        "for key corporate and social systems. ", 
        
        "My broader professional vision interconnects all the key technologies for modern data analysis—"  
        "spanning <b>data mining</b>, <b>artificial intelligence models</b>, <b>algorithms</b>, <b>software engineering workflows</b>, "  
        "and <b>information tools</b>—into a cohesive and holistic framework."  
    ]

            
    
def load_avatar_caption():
    return "God told me I could either be good-looking or an excellent worker."

def load_code_samples():
    return [
        {"title": "🚀 Genetic Algorithms for forecasting app sales", "url": "https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz"},
        {"title": "🧩 Ensemble Learning for automated hiring in Human Resources", "url": "https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvAO"}
    ]



def load_detailed_offering(id_pattern="offering-{}", colors=["#f0f0f0", "#ffffff"]):
    # Generate a hash from the system date
    system_date = datetime.datetime.now().strftime("%Y-%m-%d")
    style_prefix = hashlib.md5(system_date.encode()).hexdigest()[:8]  # Shorten hash for readability

    offerings = [
        {
            "title": "⚡ 1. High-Performance Prediction of Key Business Outcomes",
            
            "description": "I implement <em>statistically driven inference</em> of predictive patterns powered by state-of-the-art <em>Machine Learning</em> "
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
                "Skilled at developing custom data processing algorithms with bespoke logic. ",
                "Capable of using text-minning and Natural Language Processing tricks to engineer flexible information proessing heuristics. ",
                "Facility to engage with structured and unstructured sources.",
                "Foundations in NLP, GIS, and network analysis.",
                "High expertise in designing advanced merges and data sources.",
                "Expertise in using text-mining and NLP for information processing."
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
            "skills": [
                "Expert use of Python, R Studio and Stata for applied statistical analysis. ",
                "Profficient implementation of Object Oriented programming in Python (Core Features, OOP), Functional Programming in R (dplyr, ggplot, shiny, regex). ",
                "Profficient implementation of analytical queries using SQL. ",
                "Profficient implementation of distributed computing (PySpark) and workflow orchestration (Airflow). ",
                "Expertise developing and mantaining code in AI accelerated environments (GPT and Copilot). ",
                "Fast pace of research/assimilation of new tools. "
            ]
        },
        {
            "title": "🛸 5. Unpacking Artificial Intelligence for Data Analysis",
            "description": "I prepare myself by means of self-learning for the disruption of Artificial Intelligence in software development and the rise of LLM-powered applications.",
        },
        {
            "title": "⚖️ (Bonus) Rigorous Economic Mindset",
            "description": "As a professional economist, I over-simplify complex social phenomena by casually referencing supply and demand (kidding!). "
                           "But really, I approach data analysis with a focus on causal reasoning, marginal effects, and counterfactual analysis.",
        }
    ]
    

    # Initialize HTML output
    offering_html = '<h3>(5+1) Key Differentials of My Professional Offering</h3>'
    offering_html += '<ul style="padding-left: 20px; list-style-type: none;">'  # Removes bullet points

    tooltip_ids = []  # Store unique IDs for tooltips

    # Generate offering list without any enumeration
    for i, offer in enumerate(offerings):
        element_id = id_pattern.format(i+1)
        bg_color = colors[i % len(colors)]
        offering_html += f'<li id="{element_id}" style="background-color: {bg_color}; padding: 8px; border-radius: 4px; margin-bottom: 10px;">'
        offering_html += f'<strong>{offer["title"]}</strong>: {offer["description"]}'

        # Insert the tooltip for the list of technical skills
        if "skills" in offer:
            tooltip_html, unique_id = html_for_tooltip_from_large_list(
                offer["skills"], label="Technical Skills", color="#555", emoji="🏅"
            )
            offering_html += tooltip_html
            tooltip_ids.append(unique_id)
        offering_html +="<br>"

        if "subitems" in offer:
            offering_html += '<ul style="list-style-type: none; padding-left: 0;">'
            for subitem in offer["subitems"]:
                offering_html += f'<li>{subitem}</li>'
            offering_html += '</ul>'

        offering_html += '</li>'
    
    offering_html += '</ul>'

    return offering_html, tooltip_ids



