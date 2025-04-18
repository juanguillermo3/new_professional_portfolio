"""
title: Recommendation System
description: Implements a portfolio section to display recommended content (projects, code samples) from an  
             underlying professional portfolio. Assuming key project metadata is provided by external services  
             (i.e., the collector is external), this class applies the ranker and serves portions of a RecSys  
             system. Moreover, it creates visually appealing representations of the recommended content.  
"""

# Standard Library Imports
import os
import re
import time
import glob
import random
import hashlib
from datetime import datetime
import markdown

# Third-Party Imports
import streamlit as st
import streamlit.components.v1 as components

# Custom Project-Specific Imports
from git_api_utils import load_modules_metadata
from git_api_utils import load_repos_metadata as load_github_metadata
from app_end_metadata import load_repos_metadata as load_app_metadata
from front_end_utils import render_section_separator, prettify_title, tags_in_twitter_style
from media_carousel import MediaCarousel  # Assuming this is the correct import
from visual_media import  VisualContentGallery
from front_end_for_recommended_content import html_for_item_data, html_for_milestones_from_project_metadata, render_recommendation_card
from portfolio_section import PortfolioSection
from exceptional_ui import apply_custom_tooltip, _custom_tooltip_with_frost_glass_html
from biotech_lab import frost_glass_mosaic, _custom_tooltip_with_frost_glass_html
from expandable_text import expandable_text_html

import os
from dotenv import load_dotenv
load_dotenv()
MOCK_INFO_PREFIX = os.getenv("MOCK_INFO", "[MOCK INFO]")

#
# Instantiation of the semantic retriever -> helps to filter projects by meaning
#

from project_retrieval import SemanticRetriever
project_retriever=SemanticRetriever("index/projects.index","index/metadata.json")
code_retriever=SemanticRetriever("index/modules_index.index","index/modules_metadata.json")

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
class RecommendationSystem(PortfolioSection):

    EARLY_DEVELOPMENT_STAGE = False  # Override class defaults for this section
    DATA_VERIFIED=True # Set to False if uses AI mock-ups extensively
    
    # Default media dimensions (class-level static attributes)
    MEDIA_CONTAINER_WIDTH = "700px"
    MEDIA_CONTAINER_HEIGHT = "400px"
    #
    def __init__(self, 
                 semantic_project_retriever=None,
                 semantic_code_retriever=None, 
                 num_recommended_items=6, 
                 num_columns=3,
                 section_header="Project Galleria 🗂️ ",
                 section_description="Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category."):
        """
        A class responsible for rendering a gallery of projects and
        recommending them based on semantic similarity.

        Args:
            semantic_project_retriever: An instance of a semantic retriever component
                responsible for encoding queries and retrieving similar projects.
            num_recommended_items (int): Number of recommended items to display.
            num_columns (int): Number of columns in the gallery layout.
            section_header (str): Title for the section.
            section_description (str): Descriptive subtitle for the section.
        """
        super().__init__(
            title=section_header,
            description=section_description,
            verified=self.DATA_VERIFIED,
            early_dev=self.EARLY_DEVELOPMENT_STAGE,
            ai_content=not self.DATA_VERIFIED
        )

        self.semantic_project_retriever = semantic_project_retriever
        self.semantic_code_retriever = semantic_code_retriever
                   
        self.num_recommended_items = num_recommended_items
        self.num_columns = num_columns
        
        self.repos_metadata = combine_metadata()
        self.metadata_list = load_modules_metadata()

        self._sort_projects()
        self._prepare_project_titles_and_default()

        self.active_galleria = None  # Still optional unless you attach something dynamically

    #
    def _sort_projects(self):
        """Sort projects by ongoing status and number of related items."""
        self.project_item_counts = {
            repo["title"].lower(): sum(
                1 for item in self.metadata_list if item['repo_name'].lower() == repo["title"].lower()
            )
            for repo in self.repos_metadata
        }

        self.repos_metadata.sort(
            key=lambda x: (
                not x.get("ongoing", False),
                -self.project_item_counts.get(x["title"].lower(), 0)
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
    ⚙️ The recommendation system suggests some application modules from larger projects I’ve worked on. 
    Code samples are ranked based on availability of media content and freshness. 
    The system currently supports filtering by project and exact keyword matching in code metadata (titles/descriptions) and library names for Python and R code samples.
    """
    #
    # ranking logic aspect of the RecSys
    #
    def rank_items(self, query=None, selected_project=None):
        """Rank the items by priority on 'image_path' and 'last_updated', then apply filters."""
    
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
        #   - Priority: Items with "image_path" not empty come first.
        #   - Secondary: Sort by 'last_updated' in descending order.
        ranked_items = sorted(
            self.metadata_list,
            key=lambda x: (
                not bool(x.get("image_path")),  # Items without image_path get a higher value (sorted later)
                -datetime.strptime(
                    x.get("last_updated", "1970-01-01T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ"
                ).timestamp(),
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
                if query_pattern.search(item.get("title", "")) 
                or query_pattern.search(item.get("description", "")) 
                or any(query_pattern.search(lib) for lib in item.get("libraries", []))
            ]

        # Step 5: Return the top 'num_recommended_items' recommendations
        return final_ranked_items[:self.num_recommended_items]

    #
    # front end representation of items
    #
    def render_card(self, rec, **kwargs):
        """Render a single recommendation card with dynamic HTML generation."""

        render_recommendation_card(rec)
    
    def _style_ancillary_component(self, component_key):
        """Apply CSS styles to make the ancillary component visible with a smooth transition."""
        st.markdown(
            f"""
            <style>
            .st-key-{component_key} * {{
                opacity: 0;
                visibility: hidden;
                height: 0;
                overflow: hidden;
                transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out, height 0.5s ease-in-out;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )




    #
    def _fetch_files(self, repo_name):
        """Fetches all file paths associated with a given repository name.
        
        Parameters:
            - repo_name (str): The name of the repository.
        
        Returns:
            - list: A list of file paths belonging to the given repository.
        """
        return [ _ for _ in  [
            item.get("file_path", False)  # Safely get file_path, returns None if missing
            for item in self.metadata_list
            if item.get("repo_name", "").lower() == repo_name.lower() 
        ] if _ ]
      
    def _render_milestones_grid(self, project_metadata, top_margin=20, bottom_margin=20):
        """Render milestones in a row-based grid with unique styling per project and customizable margins."""
    
        # Generate a unique hash based on project metadata (e.g., project title and current time)
        unique_key = hashlib.md5(f"{project_metadata['title']}_{time.time()}".encode()).hexdigest()
    
        # Create a container with the unique key
        with st.container(key=unique_key):
            # Apply custom styling with unique key for each project's container, including top and bottom margins
            st.markdown(
                f"""
                <style>
                    .st-key-{unique_key} {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100%;
                        flex-direction: row;
                        gap: 20px;
                        margin-top: {top_margin}px;
                        margin-bottom: {bottom_margin}px;
                    }}
                    .st-key-{unique_key} .stColumn {{
                        flex: 1;
                        text-align: center;
                    }}
                </style>
                """,
                unsafe_allow_html=True
            )
    
            # Initialize the columns for milestones (4 columns including business impact)
            cols = st.columns(4)  # Now creating 4 columns for the grid layout
    
            # Define milestone data to be rendered, including the new "business_impact"
            milestones_data = [
                ("business_impact", "Business Impact"),  # New milestone category added
                ("achieved_milestones", "Achieved Milestones"),
                ("next_milestones", "Upcoming Milestones"),
                ("code_samples", "Code Samples")
            ]
    
            # Loop through milestone data and render each in a column
            for i, (milestone_type, _) in enumerate(milestones_data):
                with cols[i % len(cols)]:  # Cycle through the columns
    
                    # Special handling for "code_samples" to fetch files dynamically
                    if milestone_type == "code_samples":
                        files = self._fetch_files(project_metadata["title"])  # Fetch files dynamically
                        html_content = html_for_milestones_from_project_metadata(
                            milestones=files,  # Pass fetched file paths as milestones
                            milestone_type=milestone_type
                        )
                    else:
                        html_content = html_for_milestones_from_project_metadata(
                            project_metadata=project_metadata,
                            milestone_type=milestone_type
                        )
    
                    if html_content:
                        # Render the HTML content directly inside the column
                        st.markdown(html_content, unsafe_allow_html=True)

    #
    # front end representation of items
    #
    def render_card(self, rec, **kwargs):
        """Render a single recommendation card with dynamic HTML generation."""

        card_html, tooltip_html, tooltip_styles=html_for_item_data(rec)
        st.markdown(card_html, unsafe_allow_html=True)
        st.markdown(tooltip_html, unsafe_allow_html=True)
        st.markdown(tooltip_styles, unsafe_allow_html=True)

        unique_hash = hashlib.md5(rec['title'].encode()).hexdigest()
        button_id = f"galleria_{unique_hash}"
    

    def _fetch_highlighted_project(self):
        """Returns the title of the hardcoded highlighted project based on keyword match."""
        
        highlight_key = "random-forest"
    
        for project in self.repos_metadata:
            title = project.get("title", "").lower()
            tags = [tag.lower() for tag in project.get("tags", [])]
    
            if highlight_key in title or highlight_key in tags:
                return project["title"]
    
        # Fallback: return the title of the first project if nothing matches
        if self.repos_metadata:
            return self.repos_metadata[0]["title"]
    
        return None


    def _render_control_panel(self):
        unique_key = "control-panel"
    
        st.markdown(
            f"""
            <style>
                .st-key-{unique_key} {{
                    position: sticky;
                    top: 10px;
                    background-color: #e5e5e5;
                    border: 2px solid rgba(255, 255, 255, 0.9);
                    padding: 25px;
                    margin-top: 40px;
                    margin-bottom: 40px;
                    margin-left: auto;
                    margin-right: auto;
                    width: 82%;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                    border-radius: 14px;
                    z-index: 1000;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    cursor: grab;
                }}
    
                .st-key-{unique_key}:hover {{
                    transform: scale(1.02);
                    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.25);
                }}
    
                .stTextArea > div > textarea {{
                    transition: border 0.3s ease, box-shadow 0.3s ease;
                    border-radius: 6px;
                    height: 120px !important;
                    resize: vertical;
                }}
    
                .stTextArea > div > textarea:focus {{
                    border: 1px solid #4a90e2;
                    box-shadow: 0 0 6px rgba(74, 144, 226, 0.6);
                    outline: none;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
        with st.container(key=unique_key):
            query = st.text_area(
                label="🔍 Search examples by business requirement, methodology, or desired software implementation.",
                placeholder="As a small business owner, I want to forecast sales for the next season. The system should serve highly accurate forecasts from historical series data and forecasts should be displayed in a BI dashboard.",
                height=140,
                value=None  # Explicit default
            )
            st.caption("💡 Press Ctrl+Enter or click outside the box to apply your query.")
    
        return query

    
    def render(self):
        """Render method displaying all projects in a portfolio-style view with a featured 'Personal Highlight'.
    
        If no query is entered, a hardcoded highlight is shown first, followed by the rest (excluding highlight).
        If a query is entered, only the ranked projects are shown in order.
        """
    
        self._render_headers()
    
        # Step 1: Get user input only
        user_query = self._render_control_panel()
    
        # Step 2: Copy metadata to avoid mutating the original list
        projects_copy = self.repos_metadata.copy()
    
        # Step 3: Determine projects to render
        if user_query:
            ranked_project_lists = self.semantic_project_retriever.search(user_query)
            ranked_titles = [pair["title"] for pair in ranked_project_lists]
            projects_to_render = [
                project for title in ranked_titles
                for project in projects_copy
                if project["title"] == title
            ]
        else:
            # No query evaluated, fetch and render the highlighted project
            highlighted_title = self._fetch_highlighted_project()
            if highlighted_title:
                st.markdown(
                    "<div style='text-align: right;'><h4>🌟 <em>Personal Highlight</em></h4></div>",
                    unsafe_allow_html=True
                )
                highlighted_project = next(
                    (project for project in projects_copy if project["title"] == highlighted_title),
                    None
                )
                if highlighted_project:
                    self.render_project_metadata_and_recommendations(highlighted_project, user_query)
                    st.markdown("---")
    
                # Exclude highlighted project from further rendering
                projects_to_render = [
                    project for project in projects_copy if project["title"] != highlighted_title
                ]
            else:
                projects_to_render = projects_copy
    
        # Step 4: Render selected projects
        for project_metadata in projects_to_render:
            self.render_project_metadata_and_recommendations(project_metadata, user_query)
            st.markdown("---")

    def render_project_metadata_and_recommendations(self, project_metadata, query):
        """Render project title, video, metadata, and recommendations in an ancillary container."""
    
        # Prepare video filename and path
        sanitized_title = re.sub(r"[ \-]", "_", project_metadata['title'].lower())
        video_filename = f"{sanitized_title}_theme.mp4"
        video_path = os.path.join('assets', video_filename)
    
        # 🔧 DEBUG: Print expected video path
        if not os.path.exists(video_path):
            st.warning(f"⚠️ Video not found at: `{video_path}`. Check the filename and ensure the file exists.")
    
        # Prepare metadata and description
        tags_html = tags_in_twitter_style(project_metadata.get("tags", []))
        parsed_description = markdown.markdown(project_metadata['description'])
        description_html, description_styles = expandable_text_html(parsed_description)
        description_html = markdown.markdown(f"{description_html} ")
    
        # Unique media placeholder for each project
        media_placeholder = st.empty()
    
        # Attempt to show video
        if os.path.exists(video_path):
            media_placeholder.video(video_path, loop=True, autoplay=True, muted=True)
    
        # Render title and description
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 0px;">
                <h3>{prettify_title(project_metadata['title'])}</h3>
            </div>
            <p style="text-align: center; margin-top: 0px;">{tags_html}</p>
            """,
            unsafe_allow_html=True,
        )
    
        # Generate a unique key for ancillary container
        unique_key = hashlib.md5(f"{project_metadata['title']}_{time.time()}".encode()).hexdigest()
        with st.container(key=unique_key):
            st.markdown(
                f"""
                <div style="text-align: justify;">
                    {description_html}
                </div>
                {description_styles}
                """,
                unsafe_allow_html=True,
            )
    
            st.markdown("<br>", unsafe_allow_html=True)
            self._render_milestones_grid(project_metadata)
            st.markdown("<br>", unsafe_allow_html=True)
    
            recommendations = self.rank_items(None, project_metadata["title"])
    
            filter_message = f"Showing all results for project {prettify_title(project_metadata['title'])}"
            if query:
                filter_message += f" (and for keyword: {query})"
    
            st.markdown(
                f'<p style="font-style: italic; color: #555; font-size: 105%; font-weight: 550;">{filter_message}</p>',
                unsafe_allow_html=True
            )
    
            for i in range(0, len(recommendations), self.num_columns):
                cols = st.columns(self.num_columns)
                for col, rec in zip(cols, recommendations[i: i + self.num_columns]):
                    with col:
                        self.render_card(rec, is_project=rec.get("is_project", False))


    #
    # ranking logic aspect of the RecSys
    #
    def rank_items(self, query=None, selected_project=None):
        """Rank the items by priority on 'image_path' and 'last_updated', then apply filters."""
    
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
        #   - Priority: Items with "image_path" not empty come first.
        #   - Secondary: Sort by 'last_updated' in descending order.
        ranked_items = sorted(
            self.metadata_list,
            key=lambda x: (
                not bool(x.get("image_path")),  # Items without image_path get a higher value (sorted later)
                -datetime.strptime(
                    x.get("last_updated", "1970-01-01T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ"
                ).timestamp(),
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
                if query_pattern.search(item.get("title", "")) 
                or query_pattern.search(item.get("description", "")) 
                or any(query_pattern.search(lib) for lib in item.get("libraries", []))
            ]
  
        # Step 5: Return the top 'num_recommended_items' recommendations
        return final_ranked_items[:self.num_recommended_items]



# Assume project_retriever is an instance of your semantic retriever (already initialized)
recsys = RecommendationSystem(
    semantic_project_retriever=project_retriever,
    semantic_code_retriever=code_retriever, 
    section_description="Our Recommendation System (RecSys) helps you discover projects and code examples you may find interesting."
)
