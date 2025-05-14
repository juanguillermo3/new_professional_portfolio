"""
title: APP End Metadata
description: A lightweight storage for additional metadata related to portfolio repositories. It helps front-end 
             engineers include extra information about different projects, such as tags, milestones, and completion 
             status. More specialized in displaying engaging information that complements essential project data.
"""

def load_repos_metadata():
    return [
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
        },
        {
            "title": "new_professional_portfolio",
            "ongoing": True,
            "tags": [
                "online portfolio",
                "application development",
                "streamlit",
                "Recommendation Systems",
                "LLM apps",
                "front-end development",
                "web design",
                "metadata aggregation"
            ],
            "achieved_milestones": [
                "Developed a front-end web application for a professional portfolio with multiple sections.",
                "Developed classes for a hero area, RecSys, services, and curriculum vitae sections, following web application and marketing patterns.",
                "Implemented core RecSys logic to serve recommendations on projects and code samples.",
                "Implemented key workflows to collect and harmonize project metadata from multiple sources.",
                "Worked on visually appealing representation of recommended content and other front-end components."
            ],
            "next_milestones": [
                "Explore a more flexible, NLP-based query matching system for the RecSys."
            ]
        },
        {
          "title": "Random-Forest-Modeling-of-Mexican-Gas-Output",
          "tags": [
            "Energy Forecasting",
            "Natural Gas",
            "Random Forest",
            "Socioeconomic Modeling",
            "Policy Planning",
            "Machine Learning"
          ],
          "description": "This private consultancy project developed a Random Forest-based framework to model Mexico’s national gas production (Million Standard Cubic Feet per Day) from structural economic, demographic, and industrial variables. Designed to serve forecasts at variable horizons (from a month to a year), it supports strategic foresight and proactive planning for policymakers and private sector actors. Feature selection was guided by expert input, enabling the model to capture key natural-level processes driving gas output.",
          "achieved_milestones": [
            "Integrated structural and demographic datasets from public Mexican sources.  # (mock-up)",
            "Engineered feature set with expert knowledge to reflect socio-economic drivers.  # (mock-up)",
            "Trained and validated Random Forest models for short- and long-term forecasting.  # (mock-up)",
            "Implemented diagnostic tools to evaluate long-term predictive reliability.  # (mock-up)"
          ],
          "business_impact": [
            "Can support energy policy decisions with interpretable, data-driven forecasts.",
            "Can assist private energy providers in proactive planning based on structural drivers."
          ],
          "performance": [
            "Forecasting system predicts Mexico’s gas output at **1, 3, 6, and 12-month horizons**, achieving **R² scores of 0.89, 0.86, 0.82, and 0.70**, respectively, on **holdout validation sets**."
          ],
          "models": [
            "Forecasting engine implemented using **`RandomForestRegressor`** from the **scikit-learn** library, leveraging ensemble learning for robust regression performance."
          ],
          "breakthrough": [
            "Applied multiple **feature engineering workarounds** and a **sliding retraining window** strategy to address the limitations of Random Forests when applied to **non-stationary time series forecasting**."
          ],
          "notebooks": [
            {
              "title": "Gas Forecasting Notebook",
              "url": "https://colab.research.google.com/drive/1MHMx_IS1_a1x9jhEhuy2BRLoGQ239TpU"
            }
          ],
          "dashboard": {
            "title": "How it works",
            "media": "assets/forecast_per_horizon.png",
            "bullets": [
              "**Forecasting system** predicts Mexico’s gas output at multiple horizons (1, 3, 6, and 12 months), achieving R² scores of **0.89**, **0.86**, **0.82**, and **0.70** respectively."
            ]
          },
          "call_to_action": "Did you like this project? I can use ML to forecast any relevant parameter of the economic environment for corporate planning. Reach out to discuss your requirements!"
        },
        {
        "title": "welcoming_index",
        "tags": [
          "International Policy",
          "Visa Openness",
          "Index Design",
          "Global Mobility",
          "Data Visualization"
        ],
        "description": "This exercise implements an index to measure how welcoming a given country is—in principle—to citizens from any other country in the world.",
        "achieved_milestones": [
          "# (ai placeholder: milestone 1)",
          "# (ai placeholder: milestone 2)",
          "# (ai placeholder: milestone 3)"
        ],
        "business_impact": [
          "# (ai placeholder: business impact 1)",
          "# (ai placeholder: business impact 2)"
        ],
        "performance": [
          "# (ai placeholder: performance details)"
        ],
        "models": [
          "# (ai placeholder: model description)"
        ],
        "breakthrough": [
          "# (ai placeholder: breakthrough details)"
        ],
        "notebooks": [
          {
            "title": "Visa Requirement Index",
            "url": "https://colab.research.google.com/drive/1JMsWOW2dnL_sc1_v_yuqE1097dfWWWcn#scrollTo=8O2UpQkk03VY"
          }
        ],
        "dashboard": {
          #"title": "# (ai placeholder: dashboard title)",
          "media": "welcoming_choroplet.png",
          "bullets": [
            "**Overall positive association** between open migratory policies (being *welcoming*) and low visa requirements (being *welcomed*) → basic reciprocation in action.",
            "**Large regional disparities** in migratory policies and reception: North America and Europe are much more *welcomed*, while countries in the Caribbean, Central, and South America are much more *welcoming*.",
            "**Reciprocation varies widely** between regions: Eastern Europe, East and Southeast Asia are almost as *welcomed* as South and Central America, but are far more *restrictive* in their own policies."
          ]
        },
        "call_to_action": "Do you find this project interesting? I can organize and develop data collection and information processing activities for research environments, with a focus on public policy analysis. Reach out to discuss your requirements!"
  }


]
