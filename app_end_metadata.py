# app_end_metadata.py
def load_repos_metadata():
    return [
        {
            "title": "monkey_research",
            "ongoing": True,
            "tags": ["ethology research", "inferential statistics", "R Studio", "Visualization"]
        },
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
    }
    ]
