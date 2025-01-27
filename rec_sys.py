"""
title: Recommendation System
description: Current implementation of the RecSys, featuring a vanilla ranking that sorts items by the most recently updated, filters by query (exact matching), and allows filtering by project.
"""

import os
import re
import streamlit as st
from datetime import datetime
from git_api_utils import load_modules_metadata
from git_api_utils import load_repos_metadata as load_github_metadata
from app_end_metadata import load_repos_metadata as load_app_metadata
import hashlib

def combine_metadata():
    # Load both sets of metadata
    github_metadata = load_github_metadata()
    app_metadata = load_app_metadata()

    # Convert app metadata to a dictionary for fast lookup
    app_metadata_dict = {item["title"]: item for item in app_metadata}

    # Perform a left join: update GitHub metadata with matching app metadata
    combined_metadata = []
    for project in github_metadata:
        title = project["title"]
        # Update GitHub metadata with app metadata if available
        updated_project = {**project, **app_metadata_dict.get(title, {})}
        combined_metadata.append(updated_project)

    return combined_metadata


class RecommendationSystem:
    def __init__(self, num_recommended_items=6, num_columns=3, section_header="Recommendation System 🎯", section_description="Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category."):
        self.num_recommended_items = num_recommended_items
        self.num_columns = num_columns
        self.section_header = section_header
        self.section_description = section_description
        
        # Cache the metadata
        self.repos_metadata = combine_metadata()  
        self.metadata_list = load_modules_metadata()  

        # Sort the projects by the number of related items in metadata_list
        project_item_counts = {}
        for repo in self.repos_metadata:
            repo_name = repo["title"].lower()
            related_items_count = sum(1 for item in self.metadata_list if item['repo_name'].lower() == repo_name)
            project_item_counts[repo_name] = related_items_count

        # Calculate project-related item counts and status
        project_item_counts = {}
        for repo in self.repos_metadata:
            repo_name = repo["title"].lower()
            related_items_count = sum(1 for item in self.metadata_list if item['repo_name'].lower() == repo_name)
            project_item_counts[repo_name] = related_items_count

        # Sort repos by ongoing status (True for ongoing first), then by item count
        self.repos_metadata.sort(
            key=lambda x: (
                not x.get("ongoing", False),  # False for ongoing (sorts first), True otherwise
                -project_item_counts.get(x["title"].lower(), 0)  # Descending by item count
            )
        )
        
        # Prepare titles for the selector with "(Ongoing)" appended if applicable
        self.project_titles = [
            f"{repo['title']} (Ongoing)" if repo.get("ongoing", False) else repo["title"]
            for repo in self.repos_metadata
        ]
        
        # Map prettified titles to actual titles
        self.title_mapping = {
            self.prettify_title(title): repo["title"]
            for title, repo in zip(self.project_titles, self.repos_metadata)
        }
        
        # Set default to the project with the highest number of items
        self.default_project = self.repos_metadata[0]["title"] if self.repos_metadata else "No Projects"

    def rank_items(self, query=None, selected_project=None):
        """Rank the items by the last updated date and apply filters."""
        # Step 1: Sort items by 'last_updated' from newest to oldest,
        # Treat items without 'last_updated' as if they are the oldest.
        ranked_items = sorted(self.metadata_list, key=lambda x: datetime.strptime(x.get('last_updated', '1970-01-01T00:00:00Z'), "%Y-%m-%dT%H:%M:%SZ"), reverse=False)
    
        # Step 2: Filter by project selection
        if selected_project and selected_project != "All Projects":
            ranked_items = [
                item for item in ranked_items if item['repo_name'].lower() == selected_project.lower()
            ]
    
        # Step 3: Filter by search query
        if query:
            query_pattern = re.compile(re.escape(query), re.IGNORECASE)
            ranked_items = [
                item for item in ranked_items
                if query_pattern.search(item["title"]) or query_pattern.search(item["description"])
            ]
    
        # Step 4: Return the top 'num_recommended_items' recommendations
        return ranked_items[:self.num_recommended_items]

    def prettify_title(self, title):
        """Prettify the title by removing underscores and capitalizing words."""
        return " ".join(word.capitalize() for word in title.replace("_", " ").split())

    def render_card(self, rec, is_project=False):
        """Render a single recommendation card with fixed height and scrollable content."""
        background_color = "#f4f4f4" if not is_project else "#fff5e6"  # Silver background for non-project items
        border_style = "2px solid gold" if is_project else "1px solid #ddd"
        
        # Fixed height for the card and allow vertical scrolling
        card_height = "200px"  # You can adjust this value to set the desired height
        overflow_style = "overflow-y: auto;"  # Enables vertical scrolling for overflowing content
    
        # Check if 'galleria' is present in the card
        galleria_present = "galleria" in rec
        
        # Modify the title to include a star if 'galleria' is present
        title = self.prettify_title(rec['title'])
        if galleria_present:
            title = f"⭐ {title}"
    
        st.markdown(
            f"""
            <div style="background-color: {background_color}; border: {border_style}; 
                        border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                        padding: 10px; text-align: center; height: {card_height}; {overflow_style}">
                <img src="https://via.placeholder.com/150"
                     style="border-radius: 10px; width: 100%; height: auto;">
                <h5>{title}</h5>
                <p style="text-align: justify; height: 100%; overflow-y: auto;">{rec['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Generate a unique hash for the button ID based on the card title
        unique_hash = hashlib.md5(rec['title'].encode()).hexdigest()
        button_id = f"galleria_{unique_hash}"  # Unique button ID

        # HTML for the custom button
        if galleria_present:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; margin-top: 10px;">
                    <button style="background-color: gold; color: white; 
                                   border: none; padding: 10px 20px; 
                                   text-align: center; text-decoration: none; 
                                   font-size: 14px; cursor: pointer; 
                                   border-radius: 5px;"
                            onclick="window.parent.postMessage({{'type': 'galleria_click', 'button_id': 'galleria_{unique_hash}'}}, '*');">
                        See Galleria
                    </button>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
            # JavaScript to handle the postMessage event
            st.markdown(
                """
                <script>
                    window.addEventListener('message', function(event) {
                        if (event.data.type === 'galleria_click') {
                            const buttonId = event.data.button_id;
                            const streamlitContainer = window.parent.document.querySelector('iframe');
                            streamlitContainer.contentWindow.postMessage({type: 'streamlit_callback', button_id: buttonId}, '*');
                        }
                    });
                </script>
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
    
        # Add "See Report" button if report_url is present
        if "report_url" in rec and rec["report_url"]:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; margin-top: 10px;">
                    <a href="{rec['report_url']}" target="_blank" 
                       style="text-decoration: none;">
                        <button style="background-color: #34A853; color: white; 
                                       border: none; padding: 10px 20px; 
                                       text-align: center; text-decoration: none; 
                                       font-size: 14px; cursor: pointer; 
                                       border-radius: 5px;">
                            See Report
                        </button>
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def render_card(self, rec, is_project=False):
        """Render a single recommendation card with fixed height and scrollable content."""
        background_color = "#f4f4f4" if not is_project else "#fff5e6"  # Silver background for non-project items
        border_style = "2px solid gold" if is_project else "1px solid #ddd"
        
        # Fixed height for the card and allow vertical scrolling
        card_height = "200px"  # You can adjust this value to set the desired height
        overflow_style = "overflow-y: auto;"  # Enables vertical scrolling for overflowing content
    
        # Check if 'galleria' is present in the card
        galleria_present = "galleria" in rec
        
        # Modify the title to include a star if 'galleria' is present
        title = self.prettify_title(rec['title'])
        if galleria_present:
            title = f"⭐ {title}"
    
        st.markdown(
            f"""
            <div style="background-color: {background_color}; border: {border_style}; 
                        border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                        padding: 10px; text-align: center; height: {card_height}; {overflow_style}">
                <img src="https://via.placeholder.com/150"
                     style="border-radius: 10px; width: 100%; height: auto;">
                <h5>{title}</h5>
                <p style="text-align: justify; height: 100%; overflow-y: auto;">{rec['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Generate a unique hash for the button ID based on the card title
        unique_hash = hashlib.md5(rec['title'].encode()).hexdigest()
        button_id = f"galleria_{unique_hash}"  # Unique button ID
        
        # HTML for the custom button
        if galleria_present:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; margin-top: 10px;">
                    <button style="background-color: gold; color: white; 
                                   border: none; padding: 10px 20px; 
                                   text-align: center; text-decoration: none; 
                                   font-size: 14px; cursor: pointer; 
                                   border-radius: 5px;">
                        See Galleria
                    </button>
                </div>
                """,
                unsafe_allow_html=True,
            )
        # Listen for the button click event
        
        if 'button_click' in st.session_state:
            if st.session_state.button_click:
                st.write("Button Clicked!")
                # Reset the session state after click to prevent rerun from continuing the action
                st.session_state.button_clicked = False
                st.experimental_rerun()
        
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
    
        # Add "See Report" button if report_url is present
        if "report_url" in rec and rec["report_url"]:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; margin-top: 10px;">
                    <a href="{rec['report_url']}" target="_blank" 
                       style="text-decoration: none;">
                        <button style="background-color: #34A853; color: white; 
                                       border: none; padding: 10px 20px; 
                                       text-align: center; text-decoration: none; 
                                       font-size: 14px; cursor: pointer; 
                                       border-radius: 5px;">
                            See Report
                        </button>
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def show_galleria_details(self, rec):
        """Show details of the project or galleria when the button is clicked."""
        # Display a modal-style content below the card for simplicity
        st.markdown(
            f"""
            <div style="background-color: #fff; border: 1px solid #ccc; 
                        padding: 20px; border-radius: 10px; max-width: 500px; margin: 20px auto;">
                <h3>Project Specifics for {rec['title']}</h3>
                <p>{rec.get('galleria_details', 'No details available for this project.')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render_title_and_description(self, project_metadata):
        """Renders the title and description of a project, centered and with margins."""
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
        
    def render(self):
        st.subheader(self.section_header)
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.section_description}</p>', unsafe_allow_html=True)
    
        # Query Input
        query = st.text_input("Search for recommendations by keyword (e.g., Python, R):", placeholder="Type a keyword and press Enter")
    
        prettified_titles = [self.prettify_title(title) for title in self.project_titles]
        selected_pretty_project = st.selectbox("Filter recommendations by project:", prettified_titles, index=0)
        selected_project = self.title_mapping[selected_pretty_project]
    
        # Call rank_items to get the ranked and filtered recommendations
        recommendations = self.rank_items(query, selected_project)
    
        # Check if there is project metadata and show video
        project_metadata = None
        if selected_project != "All Projects":
            for repo in self.repos_metadata:
                if repo["title"].lower() == selected_project.lower():
                    project_metadata = repo
                    break
    
        # If project metadata is available, display it with the video area
        if project_metadata:
            # Generate the video filename based on the project title
            video_filename = f"{project_metadata['title'].replace(' ', '_').lower()}_theme.mp4"
            video_path = os.path.join('assets', video_filename)  # Path to the local MP4 file

            # Render the title and description
            self.render_title_and_description(project_metadata)
            
            # Create a placeholder for the video area
            self.video_placeholder = st.empty()
        
            # Check if the video file exists in the assets folder
            if os.path.exists(video_path):
                # Display the video in the placeholder
                self.video_placeholder.video(video_path, loop=True, autoplay=True, muted=True)
            else:
                # Show a warning if the video is not found
                self.video_placeholder.warning(f"Video for {project_metadata['title']} not found.")
    
        # Render recommendations in a grid
        for i in range(0, len(recommendations), self.num_columns):
            cols = st.columns(self.num_columns)
            for col, rec in zip(cols, recommendations[i: i + self.num_columns]):
                with col:
                    self.render_card(rec, is_project=rec.get("is_project", False))



# Example usage
# Initialize RecSys with custom header and description
recsys = RecommendationSystem(
    #section_header="Customized Recommendations 🔍", 
    section_description="My research RecSys to make my portfolio discoverable. This RecSys versions uses exact pattern on item titles/descriptions, while more flexible, NLP type of matching is under development."
)

