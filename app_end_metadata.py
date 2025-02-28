"""
title: APP End Metadata
description: A lightweight storage for additional metadata related to portfolio repositories. It helps front-end 
             engineers include extra information about different projects, such as tags, milestones, and completion 
             status. More specialized in displaying engaging information that complements essential project data.
"""

def load_repos_metadata():
    return [
        {
            "title": "new_professional_portfolio",
            "ongoing": True,
            "tags": ["online portfolio", "application development", "streamlit", "Recommendation Systems", "LLM apps"]
        },
        {
            "title": "predictive_analytics",
            "tags": ["Neural Networks", "Genetic Algorithms", "Ensemble Learning"]
        },
        {
        "title": "sales_forecasting_with_genetic_neural_networks",
        "tags": ["Sales Forecasting", "Food Delivery", "Deep Neural Networks", "Genetic Optimization", "Feed Forward Neural Networks", "Recurrent Neural Networks"],
        "achieved_milestones": [
            "Built an ETL pipeline to aggregate sales counts into hourly and 15-minute intervals.",
            "Developed services for feature extraction and ML sample delivery for forecasting.",
            "Implemented traditional forecasting models (ARIMA, Exponential Smoothing).",
            "Developed AI-based forecasting models (Deep Neural Networks, Recurrent Neural Networks).",
            "Conducted research and custom-built a Genetic Optimization algorithm to fine-tune neural networks using core Python with GPT assistance."
        ],
        "next_milestones": []
        },
        {
            "title": "monkey_research",
            "ongoing": "True",
            "tags": [
                "Scientific Research",
                "Ethology",
                "Behavioral Analysis",
                "Inferential Statistics",
                "Multivariate Analysis",
                "Visualization",
                "Unsupervised Learning",
                "R Studio"
            ],
            "achieved_milestones": [
                "Standardized scientific taxonomies across project tables.",
                "Implemented an analytical database using SQLite.",
                "Developed exploratory queries to analyze project data.",
                "Implemented transformation pipelines for feature extraction.",
                "Developed publication-grade visualizations for key behavioral patterns.",
                "Implemented a statistical engine using Dunn's test and bootstrapping to analyze differences in behavior and diet patterns.",
                "Developed a model for group behavior using multinomial logistic regression.",
                "Estimated habitat areas using the Minimum Convex Polygon method.",
                "Performed spatial correlation analysis of vegetation parameters using site clustering and spatial smoothing.",
                "Visualized nutritional profiles of diets through geometric modeling."
            ],
            "next_milestones": [
                "Editing for publication and dissemination."
            ]
        },
        {
            "title": "lab_market_trends",
            "ongoing": "True",
            "tags": ["labor market", "wage analysis", "data engineering", "PySpark", "Selenium", "NLP", "Deep Learning"],
            "achieved_milestones": [
                "Developed a recurrent web scraping service (Selenium/Airflow) to periodically collect job postings from the SPE website.",
                "Built a distributed application (PySpark) to filter and deduplicate job postings.",
                "Created visualizations for overall wage distribution and segment-specific trends.",
                "Implemented a distributed application (PySpark) for phrase discovery using lift metrics.",
                "Developed distributed applications (PySpark) for text standardization, feature extraction, and transformation.",
                "Trained a deep learning model (NumPy/TensorFlow) to predict wages based on job posting vocabulary.",
                "Built services to analyze wage drivers from the underlying model (NumPy/TensorFlow).",
                "Designed a persistence model (SQLAlchemy) to store model inferences."
            ],
            "next_milestones": [
                "Refine the overall architecture of the neural network model (word vectors, transformers).",
                "Develop a calibration service for optimal hyperparameter selection.",
                "Conduct analysis on key labor market segments of interest."
            ]
        }
    ]
