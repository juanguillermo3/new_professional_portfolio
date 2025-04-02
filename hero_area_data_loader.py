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
from expandable_text import expandable_text_html

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
        "My recurring effort has been the <b>modernization of data analysis</b> "  
        "through cutting-edge techniques, such as flexible statistical inference powered by <b>Machine Learning</b>, "  
        "streamlining <em>core business</em> workflows through <b>software development</b> and <b>algorithmic automation</b>, "
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
                "Flexible information processing using text-minning, regex, Natural-Language-Processing",
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


def hover_text_component(main_text="Hover over this text", hidden_text=" and see more inline content!"):
    html = f"""
    <style>
        .hover-container {{
            display: inline;
            position: relative;
            cursor: pointer;
        }}
        .hover-text {{
            display: none;
        }}
        .hover-container:hover .hover-text {{
            display: inline;
        }}
    </style>
    <span class="hover-container">
        {main_text}
        <span class="hover-text">{hidden_text}</span>
    </span>
    """
    return html


def custom_html_for_offerings(id_pattern="offering-{}", colors=["#f0f0f0", "#ffffff"]):
    offerings = load_detailed_offerings()

    # Injected style block (to be dynamically constructed)
    style_block = "<style>\n"

    offering_html = '<h3>Key Professional Offerings</h3>'
    offering_html += '<ul style="list-style-type: none;">'  # Removes bullet points

    tooltip_ids = []  # Store unique IDs for tooltips

    for i, offer in enumerate(offerings):
        element_id = id_pattern.format(i + 1)
        bg_color = colors[i % len(colors)]

        # Split description into first sentence + rest
        description_parts = offer["description"].split(".", 1)
        short_description = description_parts[0] + "."
        full_description = description_parts[1] if len(description_parts) > 1 else ""

        offering_html += (
            f'<li id="{element_id}" class="offering-container" style="background-color: {bg_color}; padding: 8px; border-radius: 4px; margin-bottom: 10px;">'
            f'<p style="text-align: justify; margin: 0;">'
            f'<strong>{offer["title"]}</strong>: {short_description}'
        )

        # In-line expanding content (now with smooth transition)
        if full_description:
            offering_html += f' <span class="hover-{element_id}">{full_description}</span>'
            style_block += (
                f".hover-{element_id} {{"
                f" display: inline-block; opacity: 0; max-width: 0px; max-height: 0px; overflow: hidden;"
                f" transition: opacity 0.3s ease-in-out 0.2s, max-width 0.4s ease-out, max-height 0.4s ease-out; }}\n"
                f"#{element_id}:hover .hover-{element_id} {{"
                f" opacity: 1; max-width: 100%; max-height: 100px; }}\n"  # Max-height adjusted dynamically
            )

        # Tooltip rendering (if available)
        if "skills" in offer:
            tooltip_html, unique_id = html_for_tooltip_from_large_list(
                offer["skills"], label="Technical Skills", color="#555", emoji="🏅"
            )
            offering_html += tooltip_html
            tooltip_ids.append(unique_id)

        offering_html += "<br>"

        # Render subitems if available
        if "subitems" in offer:
            offering_html += '<ul style="list-style-type: none; padding-left: 0;">'
            for subitem in offer["subitems"]:
                offering_html += f'<li>{subitem}</li>'
            offering_html += '</ul>'

        offering_html += '</li>'

    offering_html += '</ul>'
    style_block += "</style>\n"

    return style_block + offering_html

import hashlib

def expandable_text_html(detailed_text: str) -> tuple[str, str]:
    """
    Generates an HTML snippet with a hover-reveal effect for long text descriptions.
    
    Returns:
        offering_html (str): The generated HTML structure.
        style_block (str): The required CSS styles.
    """
    brief, details = _chunk_texts(detailed_text)
    
    # Generate a unique element ID using a hash
    element_id = "hover-" + hashlib.md5(detailed_text.encode()).hexdigest()[:8]

    # Append the continuation emoji within a span
    brief += ' <span class="ellipsis">▶️</span>'

    text_container = (
        f'<div id="{element_id}" class="ancillary-container">'
        f'<p style="text-align: justify; margin: 0; display: inline;">{brief}'
    )

    style_block = (
        f"#{element_id} {{ cursor: pointer; }}\n"  # Cursor change
        f".ellipsis {{ color: #555; font-weight: bold; font-size: 1.1em; display: inline-block; \n"
        f" animation: bounceHint 0.67s infinite ease-in-out; }}\n"  # Faster animation
        f"@keyframes bounceHint {{\n"
        f"  0% {{ transform: translateY(0); }}\n"
        f"  40% {{ transform: translateY(-4px); }}\n"  # Slower upward movement
        f"  100% {{ transform: translateY(0); }}\n"  # Faster downward movement
        f"}}\n"
    )

    if details:
        text_container += f' <span class="{element_id}-hidden">{details}</span>'
        style_block += (
            f".{element_id}-hidden {{\n"
            f" display: none; opacity: 0; max-width: 0px; max-height: 0px; overflow: hidden;\n"
            f" transition: opacity 0.3s ease-in-out 0.2s, max-width 0.4s ease-out, max-height 0.4s ease-out; }}\n"
            f"#{element_id}:hover .{element_id}-hidden {{\n"
            f" display: inline; opacity: 1; max-width: none; max-height: 400px; }}\n"  # Vertical expansion
            f"#{element_id}:hover .ellipsis {{ opacity: 0; }}\n"  # Hide emoji when hovered
        )

    return text_container, style_block

def custom_html_for_offerings(id_pattern="offering-{}", colors=["#f0f0f0", "#ffffff"]):
    offerings = load_detailed_offerings()

    # Injected style block (to be dynamically constructed)
    style_block = "<style>\n"

    offering_html = '<h3>Key Professional Offerings</h3>'
    offering_html += '<ul style="list-style-type: none;">'  # Removes bullet points

    tooltip_ids = []  # Store unique IDs for tooltips

    for i, offer in enumerate(offerings):
        element_id = id_pattern.format(i + 1)
        bg_color = colors[i % len(colors)]

        # Generate expandable text for description
        description_html, description_style = expandable_text_html(offer["description"])
        style_block += description_style  # Append the generated styles

        offering_html += (
            f'<li id="{element_id}" class="offering-container" style="background-color: {bg_color}; padding: 8px; border-radius: 4px; margin-bottom: 10px;">'
            f'<p style="text-align: justify; margin: 0;">'
            f'<strong>{offer["title"]}</strong>: {description_html}'
        )

        # Tooltip rendering (if available)
        if "skills" in offer:
            tooltip_html, unique_id = html_for_tooltip_from_large_list(
                offer["skills"], label="Technical Skills", color="#555", emoji="🏅"
            )
            offering_html += tooltip_html
            tooltip_ids.append(unique_id)

        offering_html += "<br>"

        # Render subitems if available
        if "subitems" in offer:
            offering_html += '<ul style="list-style-type: none; padding-left: 0;">'
            for subitem in offer["subitems"]:
                offering_html += f'<li>{subitem}</li>'
            offering_html += '</ul>'

        offering_html += '</li>'

    offering_html += '</ul>'
    style_block += "</style>\n"

    return style_block + offering_html











