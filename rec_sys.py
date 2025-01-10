import streamlit as st
import re
from git_api import repos_metadata, metadata_list, REPOS_IN_PORTFOLIO
from dotenv import load_dotenv, dotenv_values
import os

class RecSys:
    def __init__(self):
        self.NUM_RECOMMENDED_ITEMS = 6
        self.NUM_COLUMNS = 3
        self.recommendations = metadata_list
        self.query = ""
        self.selected_project = "All Projects"
        
        # Load environment variables
        self._load_env()

    def _load_env(self, dotenv_path=".env"):
        """
        Reloads the .env file, ensuring all variables are updated.
        """
        # Parse current .env values without loading them into os.environ
        current_env = dotenv_values(dotenv_path)

        # Remove any keys from os.environ that exist in the .env file
        for key in current_env.keys():
            if key in os.environ:
                del os.environ[key]

        # Reload .env file into os.environ
        load_dotenv(dotenv_path, override=True)
        
    def _get_filtered_recommendations(self):
        # Filter recommendations by selected project
        if self.selected_project != "All Projects":
            self.recommendations = [rec for rec in self.recommendations if rec["project"] == self.selected_project]
        
        # Filter recommendations by search query
        if self.query:
            query_pattern = re.compile(re.escape(self.query), re.IGNORECASE)
            self.recommendations = [
                rec for rec in self.recommendations 
                if query_pattern.search(rec["title"]) or query_pattern.search(rec["description"])
            ]
        
        # Truncate recommendations to NUM_RECOMMENDED_ITEMS
        self.recommendations = self.recommendations[:self.NUM_RECOMMENDED_ITEMS]
    
    def _add_project_metadata(self, project_metadata=None):
        if project_metadata:
            project_card = {
                "title": project_metadata["title"],
                "description": project_metadata["description"],
                "url": project_metadata.get("url", None),
                "is_project": True
            }
            self.recommendations.insert(0, project_card)

    def set_query(self, query):
        self.query = query

    def set_selected_project(self, selected_project):
        self.selected_project = selected_project

    def generate_recommendations(self):
        # This function can be used to generate recommendations based on the environment
        # For now, let's just return mocked recommendations
        return [
            {"project": "Ethology Research", "image": "https://via.placeholder.com/150", "title": "Ethology Data Collection", "description": "Module on data collection techniques."},
            {"project": "Ethology Research", "image": "https://via.placeholder.com/150", "title": "Behavioral Data Analysis", "description": "Analyzing animal behavior in the wild."},
            {"project": "Forecasting Sales with Artificial Intelligence", "image": "https://via.placeholder.com/150", "title": "Sales Forecasting with ML", "description": "Using machine learning models for accurate sales predictions."},
            {"project": "Forecasting Sales with Artificial Intelligence", "image": "https://via.placeholder.com/150", "title": "AI in Retail", "description": "Application of AI techniques in retail sales forecasting."},
            {"project": "Ensemble Models for Human Resources", "image": "https://via.placeholder.com/150", "title": "HR Data Analysis", "description": "Leveraging ensemble models for employee retention."},
            {"project": "Ensemble Models for Human Resources", "image": "https://via.placeholder.com/150", "title": "Predicting Employee Turnover", "description": "Predictive modeling for employee turnover using ensemble techniques."},
            {"project": "Trends in the Colombian Labor Market", "image": "https://via.placeholder.com/150", "title": "Labor Market Trends Analysis", "description": "Analyzing the evolution of the Colombian labor market."},
            {"project": "Trends in the Colombian Labor Market", "image": "https://via.placeholder.com/150", "title": "Job Market Forecasting", "description": "Predicting future job trends in Colombia using data analytics."},
        ] + metadata_list

    def render(self):
        # **Recommendation System Section**
        st.subheader("Recommendation System 🎯")
        st.markdown("---")
        st.markdown('<p style="color: gray;">Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category.</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Query Input
        query_input = st.text_input(
            "Search for recommendations by keyword (e.g., Python, R):", 
            placeholder="Type a keyword and press Enter"
        )
        self.set_query(query_input)

        # Radial Button for Project Filter
        projects = ["All Projects"] + REPOS_IN_PORTFOLIO
        selected_project = st.selectbox("Filter recommendations by project:", projects)
        self.set_selected_project(selected_project)

        # Get recommendations
        recommendations = self.generate_recommendations()
        self._get_filtered_recommendations()

        # Add project metadata as the first recommendation (if available)
        project_metadata = None
        if selected_project != "All Projects":
            for repo in repos_metadata:
                if repo["title"].lower() == selected_project.lower():
                    project_metadata = repo
                    break
        self._add_project_metadata(project_metadata)

        # Render recommendations in a grid
        for i in range(0, len(recommendations), self.NUM_COLUMNS):
            cols = st.columns(self.NUM_COLUMNS)
            for col, rec in zip(cols, recommendations[i:i + self.NUM_COLUMNS]):
                with col:
                    # Style the project card distinctly
                    background_color = "#fff5e6" if rec.get("is_project") else "white"
                    border_style = "2px solid gold" if rec.get("is_project") else "1px solid #ddd"
                    
                    # Render the card
                    st.markdown(
                        f"""
                        <div style="background-color: {background_color}; border: {border_style}; 
                                    border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                                    padding: 10px; text-align: center;">
                            <img src="https://via.placeholder.com/150" alt="{rec['title']}" 
                                 style="border-radius: 10px; width: 100%; height: auto;">
                            <h5>{rec['title']}</h5>
                            <p>{rec['description']}</p>
                        </div>
                        """, unsafe_allow_html=True
                    )

                    # Add "See in GitHub" button if URL is present
                    if "url" in rec and rec["url"]:
                        st.markdown(
                            f"""
                            <div style="display: flex; justify-content: center; margin-top: 10px;">
                                <a href="{rec['url']}" target="_blank" 
                                   style="text-decoration: none;">
                                    <button style="background-color: #333; color: white; 
                                                   border: none; padding: 10px 20px; 
                                                   text-align: center; text-decoration: none; 
                                                   font-size: 14px; cursor: pointer; 
                                                   border-radius: 5px;">
                                        See in GitHub
                                    </button>
                                </a>
                            </div>
                            """, unsafe_allow_html=True
                        )

# Initialize RecSys
recsys = RecSys()

# Call the render method to display the recommendations
#recsys.render()
