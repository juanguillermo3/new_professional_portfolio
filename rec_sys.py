import os
import streamlit as st
import re
from git_api_utils import load_repos_metadata, load_modules_metadata, REPOS_IN_PORTFOLIO

# Assuming these values are set in the environment variables (.env file)
NUM_RECOMMENDED_ITEMS = int(os.getenv('NUM_RECOMMENDED_ITEMS', 6))  # Default to 6 if not set
NUM_COLUMNS = int(os.getenv('NUM_COLUMNS', 3))  # Default to 3 if not set

class RecommendationSystem:
    def __init__(self, section_header="Recommendation System 🎯", section_description="Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category."):
        """
        Initialize the RecommendationSystem class.
        The configuration (number of recommended items and columns) is loaded from the environment variables.
        Default section header and description can be overridden at instantiation.
        """
        self.num_recommended_items = NUM_RECOMMENDED_ITEMS
        self.num_columns = NUM_COLUMNS
        self.section_header = section_header
        self.section_description = section_description

    def render(self, section_header=None, section_description=None):
        """
        Render the recommendation system based on the configuration.
        The section header and description can be customized via parameters.
        """
        # Use provided parameters or fallback to instance attributes
        section_header = section_header or self.section_header
        section_description = section_description or self.section_description

        st.subheader(section_header)
        st.markdown("---")
        st.markdown(
            f'<p style="color: gray;">{section_description}</p>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Query Input
        query = st.text_input(
            "Search for recommendations by keyword (e.g., Python, R):",
            placeholder="Type a keyword and press Enter",
        )

        repos_metadata = load_repos_metadata()
        metadata_list = load_modules_metadata()

        # Radial Button for Project Filter
        recommendations = metadata_list
        projects = ["All Projects"] + REPOS_IN_PORTFOLIO
        selected_project = st.selectbox("Filter recommendations by project:", projects)

        # Container for Recommendations
        recsys_area = st.container()

        with recsys_area:
            recommendations = metadata_list

            # Check if the selected project exists in repos_metadata
            project_metadata = None
            if selected_project != "All Projects":
                for repo in repos_metadata:
                    if repo["title"].lower() == selected_project.lower():
                        project_metadata = repo
                        break

            # Filter recommendations by selected project
            if selected_project != "All Projects":
                recommendations = [
                    rec
                    for rec in recommendations
                    if rec["repo_name"] == selected_project
                ]

            # Filter recommendations by search query
            if query:
                query_pattern = re.compile(re.escape(query), re.IGNORECASE)
                recommendations = [
                    rec
                    for rec in recommendations
                    if query_pattern.search(rec["title"])
                    or query_pattern.search(rec["description"])
                ]

            # Truncate recommendations to self.num_recommended_items
            recommendations = recommendations[:self.num_recommended_items]

            # Add project metadata as the first recommendation (if available)
            if project_metadata:
                project_card = {
                    "title": project_metadata["title"],
                    "description": project_metadata["description"],
                    "url": project_metadata.get("url", None),
                    "is_project": True,
                }
                recommendations.insert(0, project_card)

            # Render recommendations in a grid
            for i in range(0, len(recommendations), self.num_columns):
                cols = st.columns(self.num_columns)
                for col, rec in zip(cols, recommendations[i : i + self.num_columns]):
                    with col:
                        # Style the project card distinctly
                        background_color = (
                            "#fff5e6" if rec.get("is_project") else "white"
                        )
                        border_style = (
                            "2px solid gold" if rec.get("is_project") else "1px solid #ddd"
                        )

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
                            """,
                            unsafe_allow_html=True,
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
                                """,
                                unsafe_allow_html=True,
                            )


import os
import streamlit as st
import re
from git_api_utils import load_repos_metadata, load_modules_metadata, REPOS_IN_PORTFOLIO

# Assuming these values are set in the environment variables (.env file)
NUM_RECOMMENDED_ITEMS = int(os.getenv('NUM_RECOMMENDED_ITEMS', 6))  # Default to 6 if not set
NUM_COLUMNS = int(os.getenv('NUM_COLUMNS', 3))  # Default to 3 if not set

class RecommendationSystem:
    def __init__(self, section_header="Recommendation System 🎯", section_description="Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category."):
        """
        Initialize the RecommendationSystem class.
        The configuration (number of recommended items and columns) is loaded from the environment variables.
        Default section header and description can be overridden at instantiation.
        """
        self.num_recommended_items = NUM_RECOMMENDED_ITEMS
        self.num_columns = NUM_COLUMNS
        self.section_header = section_header
        self.section_description = section_description

    def render(self, section_header=None, section_description=None):
        """
        Render the recommendation system based on the configuration.
        The section header and description can be customized via parameters.
        """
        # Use provided parameters or fallback to instance attributes
        section_header = section_header or self.section_header
        section_description = section_description or self.section_description

        st.subheader(section_header)
        st.markdown("---")
        st.markdown(
            f'<p style="color: gray;">{section_description}</p>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Query Input
        query = st.text_input(
            "Search for recommendations by keyword (e.g., Python, R):",
            placeholder="Type a keyword and press Enter",
        )

        repos_metadata = load_repos_metadata()
        metadata_list = load_modules_metadata()

        # Radial Button for Project Filter
        recommendations = metadata_list
        projects = ["All Projects"] + REPOS_IN_PORTFOLIO
        selected_project = st.selectbox("Filter recommendations by project:", projects)

        # Container for Recommendations
        recsys_area = st.container()

        with recsys_area:
            recommendations = metadata_list

            # Check if the selected project exists in repos_metadata
            project_metadata = None
            if selected_project != "All Projects":
                for repo in repos_metadata:
                    if repo["title"].lower() == selected_project.lower():
                        project_metadata = repo
                        break

            # Filter recommendations by selected project
            if selected_project != "All Projects":
                recommendations = [
                    rec
                    for rec in recommendations
                    if rec["repo_name"] == selected_project
                ]

            # Filter recommendations by search query
            if query:
                query_pattern = re.compile(re.escape(query), re.IGNORECASE)
                recommendations = [
                    rec
                    for rec in recommendations
                    if query_pattern.search(rec["title"])
                    or query_pattern.search(rec["description"])
                ]

            # Truncate recommendations to self.num_recommended_items
            recommendations = recommendations[:self.num_recommended_items]

            # Add project metadata as the first recommendation (if available)
            if project_metadata:
                project_card = {
                    "title": project_metadata["title"],
                    "description": project_metadata["description"],
                    "url": project_metadata.get("url", None),
                    "is_project": True,
                    "video_url": project_metadata.get("video_url", None),  # Added video URL field
                }

                # Render the project view as a full-width row
                st.markdown(
                    f"""
                    <div style="background-color: #fff5e6; border-radius: 10px; padding: 20px; text-align: center;">
                        <h3>{project_card['title']}</h3>
                        <p>{project_card['description']}</p>
                        {"<video width='100%' height='auto' controls><source src='" + project_card['video_url'] + "' type='video/mp4'></video>" if project_card['video_url'] else ''}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Insert the project card as the first element in the recommendations list
                recommendations.insert(0, project_card)

            # Render recommendations in a grid
            for i in range(0, len(recommendations), self.num_columns):
                cols = st.columns(self.num_columns)
                for col, rec in zip(cols, recommendations[i : i + self.num_columns]):
                    with col:
                        # Style the project card distinctly
                        background_color = (
                            "#fff5e6" if rec.get("is_project") else "white"
                        )
                        border_style = (
                            "2px solid gold" if rec.get("is_project") else "1px solid #ddd"
                        )

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
                            """,
                            unsafe_allow_html=True,
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
                                """,
                                unsafe_allow_html=True,
                            )

    def render(self):
        st.subheader(self.section_header)
        st.markdown(f'<p style="color: gray;">{self.section_description}</p>', unsafe_allow_html=True)

        # Query Input
        query = st.text_input("Search for recommendations by keyword (e.g., Python, R):", placeholder="Type a keyword and press Enter")

        repos_metadata = load_repos_metadata()  # Placeholder for your repo metadata
        metadata_list = load_modules_metadata()  # Placeholder for module metadata

        # Radial Button for Project Filter
        projects = ["All Projects"] + REPOS_IN_PORTFOLIO  # Placeholder for your repo projects
        selected_project = st.selectbox("Filter recommendations by project:", projects)

        # Container for Recommendations
        recsys_area = st.container()

        with recsys_area:
            recommendations = metadata_list  # Placeholder for the list of recommendations

            # Check if the selected project exists in repos_metadata
            project_metadata = None
            if selected_project != "All Projects":
                for repo in repos_metadata:
                    if repo["title"].lower() == selected_project.lower():
                        project_metadata = repo
                        break

            # Filter recommendations by selected project
            if selected_project != "All Projects":
                recommendations = [
                    rec
                    for rec in recommendations
                    if rec["repo_name"] == selected_project
                ]

            # Filter recommendations by search query
            if query:
                query_pattern = re.compile(re.escape(query), re.IGNORECASE)
                recommendations = [
                    rec
                    for rec in recommendations
                    if query_pattern.search(rec["title"])
                    or query_pattern.search(rec["description"])
                ]

            # Truncate recommendations to self.num_recommended_items
            recommendations = recommendations[:self.num_recommended_items]

            # Add project metadata as the first recommendation (if available)
            if project_metadata:
                project_card = {
                    "title": project_metadata["title"],
                    "description": project_metadata["description"],
                    "url": project_metadata.get("url", None),
                    "is_project": True,
                }
                recommendations.insert(0, project_card)

            # If project metadata is available, display it as a full-width row with video
            if project_metadata:
                # Generate the video filename based on the project title
                video_filename = f"{project_metadata['title'].replace(' ', '_').lower()}_theme.mp4"
                video_path = os.path.join('assets', video_filename)  # Path to the local MP4 file

                # Check if the video file exists in the assets folder
                if os.path.exists(video_path):
                    st.markdown(
                        f"""
                        <video width="100%" autoplay loop muted playsinline>
                            <source src="file://{video_path}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.warning(f"Video for {project_metadata['title']} not found.")

            # Render recommendations in a grid for the other items
            for i in range(0, len(recommendations), self.num_columns):
                cols = st.columns(self.num_columns)
                for col, rec in zip(cols, recommendations[i : i + self.num_columns]):
                    with col:
                        # Style the project card distinctly
                        background_color = (
                            "#fff5e6" if rec.get("is_project") else "white"
                        )
                        border_style = (
                            "2px solid gold" if rec.get("is_project") else "1px solid #ddd"
                        )

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
                            """,
                            unsafe_allow_html=True,
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
                                """,
                                unsafe_allow_html=True,
                            )

# Example usage
# Initialize RecSys with custom header and description
recsys = RecommendationSystem(
    #section_header="Customized Recommendations 🔍", 
    section_description="My research RecSys to make my portfolio discoverable. This RecSys versions uses exact pattern on item titles/descriptions, while more flexible, NLP type of matching is under development."
)

