
def load_quote():
    return [
        "Modern data analysis requires engaging with, sometime developing substantial software, such as data gathering and information processing applications. "
        "Moreover, software automation is key to distributing inferences from statistical analysis, such as insights from econometric analysis "
        "or predictions from machine learning models. Bottom line, I recognize the tight dependencies between data analysis and software development, "
        "hence my effort to serve both within a unified framework.",
        
        "I am Juan Guillermo. I am a professional economist. I have made a living developing data analysis and application "
        "development scripts. My larger professional project aims for a holistic vision, interconnecting all the technology for modern data analysis, "
        "comprising data mining and artificial intelligence models, algorithms, workflows, and information tools."
    ]

def load_avatar_caption():
    return "God told me I could either be good-looking or an excellent worker."

# hero_area_data_loader.py

def load_detailed_offering():
    offering = """
    <h3>(5+1) Key Differentials of My Professional Offering</h3>
    <ul style="list-style-type: none; padding: 0;">
        <li style="background-color: #f0f0f0; padding: 8px; border-radius: 4px;">
            <strong>High-Performance Predictive Analytics</strong>: I research and implement techniques for regression, classification, and forecasting use cases, 
            with applications ranging from macroeconomic and financial forecasting to microdata predictions in various systems.
        </li>
        <li style="background-color: #ffffff; padding: 8px; border-radius: 4px;">
            <strong>Software for Inference Distribution</strong>: I develop applications (batch scripts, APIs, dashboards, web applications) to distribute insights 
            and predictions across corporate environments.
        </li>
        <li style="background-color: #f0f0f0; padding: 8px; border-radius: 4px;">
            <strong>Data Transformation Expertise</strong>: As my former boss Susana Martinez Restrepo said, "I can perform data miracles." This refers to my 
            ability to clean and organize datasets from complex, multi-source environments for research and model development.
        </li>
        <li style="background-color: #ffffff; padding: 8px; border-radius: 4px;">
            <strong>Holistic Understanding of Modern Tooling</strong>: I integrate tools and technologies for modern data analysis, committing to research the 
            unique purposes of each tool and efficiently write workflows around them using GPT.
        </li>
        <li style="background-color: #f0f0f0; padding: 8px; border-radius: 4px;">
            <strong>AI & LLM Disruption in Software Development</strong>: I prepare myself by means of self-learning for the disruption of Artificial Intelligence in software development and the rise of LLM-powered applications.
        </li>
        <li style="background-color: #ffffff; padding: 8px; border-radius: 4px;">
            <strong>Bonus: Rigorous Economic Mindset</strong>: As an economist, I approach data analysis with a focus on causal reasoning, marginal effects, and 
            counterfactual analysis.
        </li>
    </ul>
    """
    
    return offering


    
    # Split the offering into individual list items
    list_items = offering.split("\n")

    # Alternate colors for the list items
    styled_items = []
    for idx, item in enumerate(list_items):
        if item.strip():  # Skip empty lines
            color = "#f0f0f0" if idx % 2 == 0 else "#ffffff"  # Alternating colors (light gray and white)
            styled_items.append(f'<li style="background-color: {color}; padding: 8px; border-radius: 4px;">{item}</li>')
    
    # Return the HTML for the list with alternating colors
    return f"<ul style='list-style-type: none; padding: 0;'>{''.join(styled_items)}</ul>"

def load_code_samples():
    return [
        {"title": "Genetic Algorithms for forecasting app sales", "url": "https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz"},
        {"title": "Ensemble models to automate hirings from Human Resources", "url": "https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvAO"}
    ]
