
"""
title: Recommendation System
description: Current implementation of the RecSys, featuring a vanilla ranking that sorts items by the most recently updated, filters by query (exact matching), and allows filtering by project.
"""

# Standard Library Imports
import os
import re
import time
import glob
import random
import hashlib
from datetime import datetime

# Third-Party Imports
import streamlit as st
import streamlit.components.v1 as components

# Custom Project-Specific Imports
from git_api_utils import load_modules_metadata
from git_api_utils import load_repos_metadata as load_github_metadata
from app_end_metadata import load_repos_metadata as load_app_metadata
from front_end_utils import render_section_separator, render_external_link_button, prettify_title, tags_in_twitter_style
from media_carousel import MediaCarousel  # Assuming this is the correct import
from visual_media import render_item_visual_content
from front_end_for_recommended_content import html_for_item_data

#
# (0) ancillary function to merge metadata about underlyng items
#
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

#
# (1) RecSys
#
class RecommendationSystem:
    def __init__(self, 
                 num_recommended_items=6, 
                 num_columns=3, 
                 section_header="Recommendation System 🎯", 
                 section_description="Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category."
                ):

        # Default media dimensions (class-level static attributes)
        MEDIA_CONTAINER_WIDTH = "700px"
        MEDIA_CONTAINER_HEIGHT = "400px"
    
        self.num_recommended_items = num_recommended_items
        self.num_columns = num_columns
        self.section_header = section_header
        self.section_description = section_description
        
        # Cache the metadata
        self.repos_metadata = combine_metadata()  
        self.metadata_list = load_modules_metadata()  

        # Sort the projects
        self._sort_projects()
        
        # Prepare project titles and default project
        self._prepare_project_titles_and_default()
    #
    # sorting logica applied to the projects
    #
    def _sort_projects(self):
        """Sorts the projects by ongoing status and number of related items."""
        project_item_counts = {
            repo["title"].lower(): sum(1 for item in self.metadata_list if item['repo_name'].lower() == repo["title"].lower())
            for repo in self.repos_metadata
        }

        self.repos_metadata.sort(
            key=lambda x: (
                not x.get("ongoing", False),  # Sort ongoing projects first
                -project_item_counts.get(x["title"].lower(), 0)  # Descending by item count
            )
        )
    #
    def _prepare_project_titles_and_default(self):
        """Prepares project titles for selection and determines the default project."""
        self.project_titles = [
            f"{repo['title']} (Ongoing)" if repo.get("ongoing", False) else repo["title"]
            for repo in self.repos_metadata
        ]

        self.title_mapping = {
            prettify_title(title): repo["title"]
            for title, repo in zip(self.project_titles, self.repos_metadata)
        }

        self.default_project = self.repos_metadata[0]["title"] if self.repos_metadata else "No Projects"
    
    RANKER_LOGIC = """
    ⚙️ The RecSys engine recommends items based on visual prominence and freshness. 
    Items with highlighted content are ranked first, followed by those with the most recent updates. 
    Special ranking positions are applied where defined, and the results are filtered by project and search query.
    """
    #
    # ranking logic aspect of the RecSys
    #
    def rank_items(self, query=None, selected_project=None):
        """Rank the items by priority on 'galleria' and 'last_updated', then apply filters."""
        
        def parse_boolean(value):
            """Helper function to safely parse boolean values from strings."""
            return str(value).strip().lower() == "true"
        
        def parse_int(value):
            """Helper function to safely parse integers."""
            try:
                return int(value)
            except (TypeError, ValueError):
                return None
    
        # Step 1: Sort items based on:
        #   - Priority: Items with "galleria" == True come first.
        #   - Secondary: Sort by 'last_updated' in descending order.
        ranked_items = sorted(
            self.metadata_list,
            key=lambda x: (
                not parse_boolean(x.get("galleria", "False")),  # 'False' items get a higher value (sorted later)
                -datetime.strptime(x.get("last_updated", "1970-01-01T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ").timestamp(),
            ),
        )
    
        # Step 2: Apply forced rank heuristic
        forced_ranked_items = [None] * len(ranked_items)  # Create a list with placeholders
        unranked_items = []
        
        for item in ranked_items:
            forced_rank = parse_int(item.get("forced_rank"))
            if isinstance(forced_rank, int) and 0 <= forced_rank < len(ranked_items):
                if forced_ranked_items[forced_rank] is None:
                    forced_ranked_items[forced_rank] = item  # Place item in specified position
                else:
                    unranked_items.append(item)  # Handle collisions by adding to unranked
            else:
                unranked_items.append(item)  # Add items without forced_rank to unranked
        
        # Fill in the remaining slots with unranked items
        final_ranked_items = [item for item in forced_ranked_items if item is not None] + unranked_items
    
        # Step 3: Filter by project selection
        if selected_project and selected_project != "All Projects":
            final_ranked_items = [
                item for item in final_ranked_items if item["repo_name"].lower() == selected_project.lower()
            ]
    
        # Step 4: Filter by search query
        if query:
            query_pattern = re.compile(re.escape(query), re.IGNORECASE)
            final_ranked_items = [
                item for item in final_ranked_items
                if query_pattern.search(item["title"]) or query_pattern.search(item["description"])
            ]
    
        # Step 5: Return the top 'num_recommended_items' recommendations
        return final_ranked_items[:self.num_recommended_items]

    #
    # front end representation of items
    #
    def render_card(self, rec, **kwargs):
        """Render a single recommendation card with dynamic HTML generation."""
        st.markdown(html_for_item_data(rec), unsafe_allow_html=True)
        
        unique_hash = hashlib.md5(rec['title'].encode()).hexdigest()
        button_id = f"galleria_{unique_hash}"
        
        if "galleria" in rec:
            st.markdown(
                """
                <style>
                div[data-testid="stButton"] > button {
                    background-color: gold !important;
                    color: white !important;
                    border: none;
                    padding: 10px 20px;
                    font-size: 14px;
                    cursor: pointer;
                    border-radius: 5px;
                    width: 60% !important;
                    margin: 5px auto;
                    display: block;
                }
                div[data-testid="stButton"] > button:hover {
                    background-color: #ffd700 !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
    
            if st.button("See Galleria", key=button_id):
                self.handle_galleria_click(rec)
        
        buttons = []
        if "url" in rec and rec["url"]:
            buttons.append(("GitHub", rec["url"], "#333"))
        if "report_url" in rec and rec["report_url"]:
            buttons.append(("Sheets", rec["report_url"], "#34A853"))
        if "colab_url" in rec and rec["colab_url"]:
            buttons.append(("Colab Notebook", rec["colab_url"], "#F9AB00"))
        
        button_cols = st.columns(len(buttons)) if buttons else []
        
        for col, (label, url, color) in zip(button_cols, buttons):
            with col:
                st.markdown(render_external_link_button(url, label, color), unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
    
    def handle_galleria_click(self, rec, width=None, height=None):
        """
        Handle the click event for the galleria item and display its content.
        """
        self.media_placeholder.empty()
        
        width = width or self.MEDIA_CONTAINER_WIDTH
        height = height or self.MEDIA_CONTAINER_HEIGHT
        
        item_title = rec.get('title', 'No Title Available')
        item_description = rec.get('description', 'No description available.')
        image_path = rec.get('image_path', None)
        
        if not image_path:
            st.error("Error: 'image_path' key not found in the provided data.")
            return
        
        with st.spinner("Loading media..."):
            with self.media_placeholder.container():
                render_item_visual_content(item_title, item_description, image_path, width, height)

    def apply_transition_styles(self):
        """Apply the CSS transition styles to the media placeholder."""
        st.markdown(
            """
            <style>
            .media-placeholder {
                transition: opacity 2s ease-in-out, transform 2s ease-in-out;  /* Slowed down transition */
                opacity: 0;
                transform: scale(0.95);
            }
            .media-placeholder.show {
                opacity: 1;
                transform: scale(1);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    #
    # main public method to render the RecSys
    #
    def render(self):
        """Render method with Galleria callback integration."""
        st.subheader(self.section_header)
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.section_description}</p>', unsafe_allow_html=True)
        
        # Display technical note for ranking logic
        st.markdown(f'{self.RANKER_LOGIC}', unsafe_allow_html=True)

        # Add space to separate the section description from the controls
        st.markdown("")
        
        # Stack the control widgets (Project Filter and Keyword Search) in a single row
        cols = st.columns(2)  # Creates 2 equal-width columns
    
        # Project Filter in the first column
        with cols[0]:
            prettified_titles = [prettify_title(title) for title in self.project_titles]
            selected_pretty_project = st.selectbox("📂 Filter by project:", prettified_titles, index=0)
            selected_project = self.title_mapping[selected_pretty_project]
    
        # Keyword Search in the second column
        with cols[1]:
            query = st.text_input("🔍 Search for by keyword (e.g., Python, R):", placeholder="Type a keyword and press Enter")
        
        # Call rank_items to get the ranked and filtered recommendations
        recommendations = self.rank_items(query, selected_project)
        
        # Check if there is project metadata and show video
        project_metadata = next((repo for repo in self.repos_metadata if repo["title"].lower() == selected_project.lower()), None) if selected_project != "All Projects" else None
        
        # If project metadata is available, display it with the video area
        if project_metadata:
            # Generate the video filename based on the project title
            video_filename = f"{project_metadata['title'].replace(' ', '_').lower()}_theme.mp4"
            video_path = os.path.join('assets', video_filename)  # Path to the local MP4 file
        
            # Render the title and description
            self.render_title_and_description(project_metadata)
            
            # Define a fixed height and width for the media container (adjust as needed)
            MEDIA_CONTAINER_WIDTH = "700px"
            MEDIA_CONTAINER_HEIGHT = "400px"  # Adjust to match the video size
            
            # Create a placeholder for the media area with a fixed size
            self.media_placeholder = st.empty()
        
            # Check if the video file exists in the assets folder
            if os.path.exists(video_path):
                # Display the video in the placeholder
                self.media_placeholder.video(video_path, loop=True, autoplay=True, muted=True)
            else:
                # Show a warning if the video is not found
                self.media_placeholder.warning(f"Video for {project_metadata['title']} not found.")
        
        # Render recommendations in a grid
        for i in range(0, len(recommendations), self.num_columns):
            cols = st.columns(self.num_columns)
            for col, rec in zip(cols, recommendations[i: i + self.num_columns]):
                with col:
                    self.render_card(rec, is_project=rec.get("is_project", False))
                    
    def render(self):
        """Render method with Galleria callback integration and smooth media transitions."""
        st.subheader(self.section_header)
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.section_description}</p>', unsafe_allow_html=True)
        
        # Display technical note for ranking logic
        st.markdown(f'{self.RANKER_LOGIC}', unsafe_allow_html=True)
        
        # Space separator
        st.markdown("")
        
        # Stack the control widgets (Project Filter and Keyword Search) in a single row
        cols = st.columns(2)
        
        # Project Filter in the first column
        with cols[0]:
            prettified_titles = [prettify_title(title) for title in self.project_titles]
            selected_pretty_project = st.selectbox("📂 Filter by project:", prettified_titles, index=0)
            selected_project = self.title_mapping[selected_pretty_project]
        
        # Keyword Search in the second column
        with cols[1]:
            query = st.text_input("🔍 Search for by keyword (e.g., Python, R):", placeholder="Type a keyword and press Enter")
        
        # Call rank_items to get the ranked and filtered recommendations
        recommendations = self.rank_items(query, selected_project)
        
        # Check if there is project metadata and show video
        project_metadata = next((repo for repo in self.repos_metadata if repo["title"].lower() == selected_project.lower()), None) if selected_project != "All Projects" else None
        
        if project_metadata:
            video_filename = f"{project_metadata['title'].replace(' ', '_').lower()}_theme.mp4"
            video_path = os.path.join('assets', video_filename)
            
            # Render the title and description of the project, centered and with margins
            tags_html = tags_in_twitter_style(project_metadata.get("tags", []))
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <h3>{prettify_title(project_metadata['title'])}</h3>
                </div>
                <div style="text-align: justify; margin-left: 10%; margin-right: 10%;">
                    <p>{project_metadata['description']} {tags_html}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # Inject the placeholder div for the media content with the CSS class
            st.markdown(
                '<div class="media-placeholder" id="media-area"></div>',
                unsafe_allow_html=True
            )
            
            # Use an instance attribute for the media placeholder
            self.media_placeholder = st.empty()
            
            if os.path.exists(video_path):
                self.media_placeholder.video(video_path, loop=True, autoplay=True, muted=True)
            else:
                self.media_placeholder.warning(f"Video for {project_metadata['title']} not found.")
            
            # Inject JavaScript to trigger transition
            st.markdown(
                """
                <script>
                setTimeout(() => {
                    document.querySelector('.media-placeholder')?.classList.add('show');
                }, 100);
                </script>
                """,
                unsafe_allow_html=True
            )
        
        # Display active filters message after project info
        filter_message = f"Showing all results for project {selected_project} "
        if query:
            filter_message += f"(and for keyword: {query})"
        st.markdown(f'<p style="font-style: italic; color: #555;">{filter_message}</p>', unsafe_allow_html=True)
        
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

