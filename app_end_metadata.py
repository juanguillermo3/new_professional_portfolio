# app_end_metadata.py
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
            "title": "lab_market_trends",
            "ongoing": True,
            "tags": ["labor market", "wages analysis", "data engineering", "PySpark", "Selenium"],
            "achieved_milestones": [
                "Data pipeline established",
                "First wage trend analysis published"
            ],
            "next_milestones": [
                "Integrate real-time labor demand trends"
            ]
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
            ]
        }
    ]
