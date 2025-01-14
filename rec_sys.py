import os
import streamlit as st
import re
from git_api_utils import load_repos_metadata, load_modules_metadata, REPOS_IN_PORTFOLIO

class RecommendationSystem:
    def __init__(self, num_recommended_items=6, num_columns=3, section_header="Recommendation System 🎯", section_description="Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category."):
        self.num_recommended_items = num_recommended_items
        self.num_columns = num_columns
        self.section_header = section_header
        self.section_description = section_description

    def prettify_title(self, title):
        """Prettify the title by removing underscores and capitalizing words."""
        return " ".join(word.capitalize() for word in title.replace("_", " ").split())

    def render_card(self, rec, is_project=False):
        """Render a single recommendation card."""
        background_color = "#fff5e6" if is_project else "white"
        border_style = "2px solid gold" if is_project else "1px solid #ddd"

        st.markdown(
            f"""
            <div style="background-color: {background_color}; border: {border_style}; 
                        border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                        padding: 10px; text-align: center;">
                <img src="https://via.placeholder.com/150" alt="{rec['title']}" 
                     style="border-radius: 10px; width: 100%; height: auto;">
                <h5>{self.prettify_title(rec['title'])}</h5>
                <p style="text-align: justify;">{rec['description']}</p>
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
        st.markdown("---")
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

            # If project metadata is available, display it as a full-width row
            
           # If project metadata is available, display it as a full-width row
            if project_metadata:
                # Generate the video filename based on the project title
                video_filename = f"{project_metadata['title'].replace(' ', '_').lower()}_theme.mp4"
                video_path = os.path.join('assets', video_filename)  # Path to the local MP4 file

                # Check if the video file exists in the assets folder
                if os.path.exists(video_path):
                    st.video(video_path, loop=True, autoplay=True, muted=True)  # Display the video as full-width
                else:
                    st.warning(f"Video for {project_metadata['title']} not found.")

            # Render recommendations in a grid for the other items
            for i in range(0, len(recommendations), self.num_columns):
                cols = st.columns(self.num_columns)
                for col, rec in zip(cols, recommendations[i : i + self.num_columns]):
                    with col:
                        self.render_card(rec, is_project=rec.get("is_project", False))
import os
import streamlit as st
import re
from git_api_utils import load_repos_metadata, load_modules_metadata, REPOS_IN_PORTFOLIO

class RecommendationSystem:
    def __init__(self, num_recommended_items=6, num_columns=3, section_header="Recommendation System 🎯", section_description="Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category."):
        self.num_recommended_items = num_recommended_items
        self.num_columns = num_columns
        self.section_header = section_header
        self.section_description = section_description

    def prettify_title(self, title):
        """Prettify the title by removing underscores and capitalizing words."""
        return " ".join(word.capitalize() for word in title.replace("_", " ").split())

    def render_card(self, rec, is_project=False):
        """Render a single recommendation card."""
        background_color = "#fff5e6" if is_project else "white"
        border_style = "2px solid gold" if is_project else "1px solid #ddd"

        st.markdown(
            f"""
            <div style="background-color: {background_color}; border: {border_style}; 
                        border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                        padding: 10px; text-align: center;">
                <img src="https://via.placeholder.com/150" alt="{rec['title']}" 
                     style="border-radius: 10px; width: 100%; height: auto;">
                <h5>{self.prettify_title(rec['title'])}</h5>
                <p style="text-align: justify;">{rec['description']}</p>
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
        st.markdown("---")
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
                #recommendations.insert(0, project_card)

            # If project metadata is available, display it with the video area
            if project_metadata:
                # Generate the video filename based on the project title
                video_filename = f"{project_metadata['title'].replace(' ', '_').lower()}_theme.mp4"
                video_path = os.path.join('assets', video_filename)  # Path to the local MP4 file

                # Render the title and description centered with some margins for the project
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <h3>{self.prettify_title(project_metadata['title'])}</h3>
                    </div>
                    <div style="text-align: justify; margin-left: 10%; margin-right: 10%; margin-bottom: 20px;">
                        <p>{project_metadata['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Check if the video file exists in the assets folder
                if os.path.exists(video_path):
                    st.video(video_path, loop=True, autoplay=True, muted=True)  # Display the video as full-width
                else:
                    st.warning(f"Video for {project_metadata['title']} not found.")

            # Render recommendations in a grid for the other items
            for i in range(0, len(recommendations), self.num_columns):
                cols = st.columns(self.num_columns)
                for col, rec in zip(cols, recommendations[i : i + self.num_columns]):
                    with col:
                        self.render_card(rec, is_project=rec.get("is_project", False))

# Example usage
# Initialize RecSys with custom header and description
recsys = RecommendationSystem(
    #section_header="Customized Recommendations 🔍", 
    section_description="My research RecSys to make my portfolio discoverable. This RecSys versions uses exact pattern on item titles/descriptions, while more flexible, NLP type of matching is under development."
)

