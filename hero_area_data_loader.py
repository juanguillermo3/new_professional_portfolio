import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the mock prefix from the environment, defaulting to "[MOCK TOOLTIP]" if not set
MOCK_INFO_PREFIX = os.getenv("MOCK_INFO", "[MOCK INFO]")

def load_tooltips_for_detailed_offerings():
    tooltips = {
        "offering-1": f"{MOCK_INFO_PREFIX} Predictive analytics involves using statistical techniques and machine learning to forecast future outcomes based on historical data.",
        "offering-2": f"{MOCK_INFO_PREFIX} Inference distribution ensures that insights generated from models reach stakeholders via APIs, dashboards, or batch reports.",
        "offering-3": f"{MOCK_INFO_PREFIX} Data transformation converts raw, unstructured data into a structured, usable format for analysis and machine learning.",
        "offering-4": f"{MOCK_INFO_PREFIX} Modern data tooling involves integrating various technologies to create efficient, scalable workflows for data-driven decision-making.",
        "offering-5": f"{MOCK_INFO_PREFIX} AI and large language models (LLMs) are reshaping software development by automating coding, debugging, and decision-making.",
        "offering-6": f"{MOCK_INFO_PREFIX} An economic mindset applies principles like supply & demand, marginal effects, and counterfactual analysis to data interpretation.",
        "offering-999": f"{MOCK_INFO_PREFIX} This is a non-existent tooltip for testing error handling.",  # Mock non-existent ID
        "offering-X": f"{MOCK_INFO_PREFIX} Another non-existent tooltip to ensure system robustness."  # Mock non-existent ID
    }
    
    return tooltips

def load_quote():
    return [
        "<b>Modern data analysis</b> requires engaging with and developing <b>substantial software</b>, "  
        "such as <b>data gathering, processing, and visualization applications</b>. "  
        "Moreover, <b>software automation</b> is key for <b>distributing inferences</b> from <b>statistical analysis</b>, "  
        "whether derived from <b>econometric models</b> or <b>machine learning predictions</b>. "  
        "Bottom line: I recognize the deep connection between <b>data analysis</b> and <b>software development</b>, "  
        "hence my effort to <b>serve them within a unified framework</b>." ,
            
        "I am Juan Guillermo, a professional economist. "  
        "I have built my career developing data analysis and software application scripts "  
        "for research and operational environments. "  
        "My business is discovering the more <b>powerful abstractions</b> to <b>effectively work with data</b>, "  
        "implementing them with <b>software engineering standards</b> to <b>build up data-driven intelligence</b> "  
        "for key corporate and social systems. "  
        "My broader professional vision interconnects all the technologies essential for modern data analysis—"  
        "spanning <b>data mining</b>, <b>artificial intelligence models</b>, <b>algorithms</b>, <b>software engineering workflows</b>, "  
        "and <b>information tools</b>—into a cohesive and holistic framework."  

    ]

def load_avatar_caption():
    return "God told me I could either be good-looking or an excellent worker."

def load_detailed_offering():
    offering = """
    <h3>(5+1) Key Differentials of My Professional Offering</h3>
    <ol style="padding-left: 20px;">
        <li id="offering-1" style="background-color: #f0f0f0; padding: 8px; border-radius: 4px;">
            <strong>1. Inferential Statistics & High-Performance Predictive Analytics</strong>: I research and implement techniques for regression, classification, and forecasting use cases, 
            with applications ranging from macroeconomic and financial forecasting to microdata predictions in various systems.
        </li>
        <li id="offering-2" style="background-color: #ffffff; padding: 8px; border-radius: 4px;">
            <strong>2. Software & Application Development for Inference Distribution</strong>: I develop applications (batch scripts, APIs, dashboards, web applications) to distribute insights 
            and predictions across corporate environments.
        </li>
        <li id="offering-3" style="background-color: #f0f0f0; padding: 8px; border-radius: 4px;">
            <strong>3. Data Engineering </strong>: As my former boss Susana Martinez Restrepo said, "I can perform data miracles." This refers to my 
            ability to clean and organize datasets from complex, multi-source environments for research and model development.
        </li>
        <li id="offering-4" style="background-color: #ffffff; padding: 8px; border-radius: 4px;">
            <strong>4. Holistic Understanding of Modern Tooling</strong>: I integrate tools and technologies for modern data analysis, committing to research the 
            unique purposes of each tool and efficiently write workflows around them using GPT.
            <ul style="list-style-type: none; padding-left: 0;">
                <li><strong>Excellence Tier (I know the code line by heart):</strong> Python, R Studio, Stata, GPT</li>
                <li><strong>Proficiency Tier:</strong> Airflow, SQL, Spark, Bash scripting</li>
                <li><strong>Currently Learning:</strong> Docker, Kubernetes, GitHub, Big Data Cloud tools, SQLAlchemy, Django</li>
            </ul>
        </li>
        <li id="offering-5" style="background-color: #f0f0f0; padding: 8px; border-radius: 4px;">
            <strong>5. Research effort on AI & LLM powered applications </strong>: I prepare myself by means of self-learning for the disruption of Artificial Intelligence in software development and the rise of LLM-powered applications.
        </li>
        <li id="offering-6" style="background-color: #ffffff; padding: 8px; border-radius: 4px;">
            <strong>Bonus: Rigorous Economic Mindset</strong>: As a professional economist, I over-simplify complex social phenomena by casually referencing supply and demand (kidding!).  
            But really, I approach data analysis with a focus on causal reasoning, marginal effects, and counterfactual analysis.
        </li>
    </ol>
    """
    
    return offering

def load_tooltips_for_detailed_offerings():
    tooltips = {
        "offering-1": "[MOCK TOOLTIP] Predictive analytics involves using statistical techniques and machine learning to forecast future outcomes based on historical data.",
        "offering-2": "[MOCK TOOLTIP] Inference distribution ensures that insights generated from models reach stakeholders via APIs, dashboards, or batch reports.",
        "offering-3": "[MOCK TOOLTIP] Data transformation converts raw, unstructured data into a structured, usable format for analysis and machine learning.",
        "offering-4": "[MOCK TOOLTIP] Modern data tooling involves integrating various technologies to create efficient, scalable workflows for data-driven decision-making.",
        "offering-5": "[MOCK TOOLTIP] AI and large language models (LLMs) are reshaping software development by automating coding, debugging, and decision-making.",
        "offering-6": "[MOCK TOOLTIP] An economic mindset applies principles like supply & demand, marginal effects, and counterfactual analysis to data interpretation.",
        "offering-999": "[MOCK TOOLTIP] This is a non-existent tooltip for testing error handling.",  # Mock non-existent ID
        "offering-X": "[MOCK TOOLTIP] Another non-existent tooltip to ensure system robustness."  # Mock non-existent ID
    }
    
    return tooltips


def load_code_samples():
    return [
        {"title": "🚀 Genetic Algorithms for forecasting app sales", "url": "https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz"},
        {"title": "🧩 Ensemble Learning for automated hiring in Human Resources", "url": "https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvAO"}
    ]
