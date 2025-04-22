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
from external_url_as_tooltip import render_url_as_tooltip
from summary_list_tooltip import html_for_summary_list_tooltip

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

    
    def _render_recommendation_grid(self, recommendations):
        """Helper to render recommendations in a responsive grid."""
        for i in range(0, len(recommendations), self.num_columns):
            cols = st.columns(self.num_columns)
            for col, rec in zip(cols, recommendations[i: i + self.num_columns]):
                with col:
                    self.render_card(rec, is_project=rec.get("is_project", False))

    def _render_portfolio_disclaimer(self, clarification: str = None):
        """Render a subtle disclaimer about the production orientation of the portfolio.
    
        Parameters:
            clarification (str, optional): Custom message to override the default disclaimer.
        """
        message = clarification or (
            "This portfolio showcases modular, production-oriented designs. "
            "Although these aren't live systems, each project simulates real-world architecture, "
            "ready to be adapted to your context."
        )
    
        st.markdown(
            f"""
            <blockquote style="border-left: 4px solid #d3d3d3; padding-left: 1em; color: #555; margin-bottom: 1.5em;">
                {message}
            </blockquote>
            """,
            unsafe_allow_html=True
        )
    
    def render(self):
        """Render method displaying all projects in a portfolio-style view with a featured 'Personal Highlight'.
    
        If no query is entered, a hardcoded highlight is shown first, followed by the rest (excluding highlight).
        If a query is entered, only the ranked projects are shown in order.
        """
    
        self._render_headers()
        self._render_portfolio_disclaimer()
    
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
            st.markdown("<hr style='border: 0.5px solid #ccc;'/>", unsafe_allow_html=True)

    #
    def render_project_metadata_and_recommendations(self, project_metadata, query):
        """Render project title, video, metadata, dashboard (if available), and recommendations in an ancillary container."""
    
        # Render project video (refactored to a helper method)
        self._render_project_video(project_metadata)
    
        tags_html = tags_in_twitter_style(project_metadata.get("tags", []))
        description = project_metadata.get("description", "No description available.")
        parsed_description = markdown.markdown(description)
        description_html, description_styles = expandable_text_html(parsed_description)
        description_html = markdown.markdown(f"{description_html} ")
    
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 0px;">
                <h3>{prettify_title(project_metadata['title'])}</h3>
            </div>
            <p style="text-align: center; margin-top: 0px;">{tags_html}</p>
            """,
            unsafe_allow_html=True,
        )
    
        unique_key = hashlib.md5(project_metadata['title'].encode()).hexdigest()
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
    
            self._render_executive_dashboard(project_metadata)
    
            colab_links = project_metadata.get("notebooks", [])
            if colab_links:
                notebook_list = "".join(
                    f"<li><a href='{nb['url']}' target='_blank'>{nb['title']}</a></li>" if isinstance(nb, dict)
                    else f"<li><a href='{nb}' target='_blank'>{nb}</a></li>"
                    for nb in colab_links
                )
                st.markdown(
                    f"""
                    <div style="margin-top: 0.5em;">
                        <p style="font-size: 110%; font-weight: 500; color: #444;">
                            🔗 <em>Notebook Previews</em>
                        </p>
                        <ul style="margin-top: -0.5em; margin-left: 1.2em; color: #444;">
                            {notebook_list}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
            st.markdown("<br>", unsafe_allow_html=True)
            self._render_milestones_grid(project_metadata)
    
            recommendations = self.rank_items(None, project_metadata["title"])
            filter_message = f"Showing all results for project {prettify_title(project_metadata['title'])}"
            #if query:
            #    filter_message += f" (and for keyword: {query})"
    
            st.markdown(
                f'<p style="font-style: italic; color: #555; font-size: 105%; font-weight: 550;">{filter_message}</p>',
                unsafe_allow_html=True
            )
    
            self._render_recommendation_grid(recommendations)
    
            # Subtle call to action
            self._render_cta_box(project_metadata)
    #
    def _render_project_video(self, project_metadata):
        sanitized_title = re.sub(r"[ \-]", "_", project_metadata['title'].lower())
        video_extensions = ['.mp4', '.webm', '.mov']
    
        video_path = next(
            (
                os.path.join('assets', f"{sanitized_title}_theme{ext}")
                for ext in video_extensions
                if os.path.exists(os.path.join('assets', f"{sanitized_title}_theme{ext}"))
            ),
            None
        )
    
        if not video_path:
            st.warning(f"⚠️ Video not found for project `{project_metadata['title']}` in supported formats.")
            return
    
        media_placeholder = st.empty()
        media_placeholder.video(video_path, loop=True, autoplay=True, muted=True)
    # 
    def _render_executive_dashboard(self, project_metadata):
        dashboard = project_metadata.get("dashboard", {})
        media_url = dashboard.get("media", None)
        bullets = dashboard.get("bullets", [])
    
        if media_url and bullets:
            project_title = project_metadata.get("title", "dashboard")
            key_namespace = re.sub(r"\W+", "_", project_title.lower())
            key_imagebox = f"{key_namespace}_dashboard_imagebox"
            key_bulletsbox = f"{key_namespace}_dashboard_bulletsbox"
    
            st.markdown(
                f"""
                <style>
                    .st-key-{key_imagebox} {{
                        background-color: #f9f9f9;
                        padding: 1em;
                        border-radius: 8px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100%;
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                        cursor: pointer;
                    }}
                    .st-key-{key_imagebox}:hover {{
                        transform: scale(1.5);
                        box-shadow: 0px 12px 24px rgba(0, 0, 0, 0.3);
                        z-index: 20;
                    }}
                    .st-key-{key_imagebox} img {{
                        max-height: 280px;
                        border-radius: 8px;
                        box-shadow: 0px 0px 10px rgba(0,0,0,0.08);
                        object-fit: contain;
                    }}
                    .st-key-{key_bulletsbox} ul {{
                        padding-left: 1.2em;
                        color: #333;
                        margin-top: 0;
                    }}
                    .st-key-{key_bulletsbox} li {{
                        margin-bottom: 0.5em;
                    }}
                </style>
                """,
                unsafe_allow_html=True,
            )

    
            col_img, col_bullets = st.columns([0.6, 0.4], gap="small", vertical_alignment="center" )
    
            with col_img:
                with st.container(key=key_imagebox):
                    st.image(media_url, use_container_width=True)
    
            with col_bullets:
                with st.container(key=key_bulletsbox):
                    st.markdown(
                        """
                        <p style="font-size: 1.1em; font-weight: 600; color: #555; border-left: 4px solid #ccc; padding-left: 0.5em; margin-bottom: 1em;">
                            Exec Summary
                        </p>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        "<ul>" +
                        "".join(
                            f"<li>{markdown.markdown(bullet)}</li>"
                            for bullet in bullets
                        ) +
                        "</ul>",
                        unsafe_allow_html=True
                    ) 
    #
    def _render_cta_box(self, project_metadata):
        """Render a subtle call-to-action box prompting WhatsApp contact."""
        call_to_action = project_metadata.get("call_to_action")
        if not call_to_action:
            return
    
        wa_number = "573053658650"  # no '+' in wa.me link
        wa_url = f"https://wa.me/{wa_number}?text=Hi!%20I'm%20interested%20in%20your%20project%20'{project_metadata['title']}'"
    
        st.markdown(
            f"""
            <div style="margin: 2em auto 1em auto; padding: 0.9em 1.2em; max-width: 600px;
                        background-color: #f9fbfc; border-left: 4px solid #cce4f7; border-radius: 8px;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.03); text-align: center;">
                <p style="margin-bottom: 0.6em; font-size: 0.95em; color: #444;">
                    {call_to_action}
                </p>
                <a href="{wa_url}" target="_blank" style="text-decoration: none;">
                    <button style="background-color: #25D366; border: none; color: white;
                                   padding: 0.5em 1.2em; font-size: 0.95em; border-radius: 20px;
                                   cursor: pointer;">
                        💬 Contact via WhatsApp
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
    #
    def _render_milestones_grid(
        self,
        project_metadata,
        top_margin=20,
        bottom_margin=20,
        col_count=4,
        gap_px=20,
        padding_px=10,
        show_titles=True
    ):
        """Render milestones in a column-wise vertical grid with consistent spacing, using row-major layout."""
    
        import hashlib, time
        import streamlit as st
        import math
    
        # Add code samples to metadata
        project_metadata["code_samples"] = self._fetch_files(project_metadata["title"])
    
        # Unique styling scope
        unique_key = hashlib.md5(f"{project_metadata['title']}_{time.time()}".encode()).hexdigest()
    
        # Style block
        st.markdown(
            f"""
            <style>
                .st-key-{unique_key} {{
                    display: flex;
                    justify-content: center;
                    align-items: flex-start;
                    flex-direction: row;
                    gap: {gap_px}px;
                    margin-top: {top_margin}px;
                    margin-bottom: {bottom_margin}px;
                }}
                .st-key-{unique_key} .stColumn {{
                    flex: 1;
                    padding: {padding_px}px;
                    text-align: center;
                }}
                .st-key-{unique_key} ul {{
                    padding-left: 0;
                    list-style: none;
                }}
                .st-key-{unique_key} li {{
                    margin: 10px 0;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
        # Create milestone types
        milestones_types = [
            "business_impact",
            "achieved_milestones",
            "next_milestones",
            "code_samples",
            "breakthrough"
        ]
    
        # Collect all items into a flat list of (label, items) pairs
        all_items = []
        for milestone_type in milestones_types:
            items = project_metadata.get(milestone_type, [])
            if items:
                all_items.append((milestone_type, items))
    
        # Flatten all labeled items
        flat_entries = []
        for label, items in all_items:
            for item in items:
                flat_entries.append((label, item))
    
        # Determine number of rows
        total_items = len(flat_entries)
        row_count = math.ceil(total_items / col_count)
    
        # Create empty list for each column
        columns_data = [[] for _ in range(col_count)]
    
        # Row-major fill
        for idx, (label, item) in enumerate(flat_entries):
            col_index = idx % col_count
            columns_data[col_index].append((label, item))
    
        # Create columns
        cols = st.columns(col_count)
    
        # Fill each column
        for col, items in zip(cols, columns_data):
            with col:
                last_label = None
                for label, item in items:
                    # Optional section title
                    if show_titles and label != last_label:
                        st.markdown(f"**{label.replace('_', ' ').title()}**")
                        last_label = label
    
                    # Render HTML per item
                    html_content = html_for_summary_list_tooltip(
                        items=[item],
                        style_key=label
                    )
                    st.markdown(html_content, unsafe_allow_html=True)

   



# Assume project_retriever is an instance of your semantic retriever (already initialized)
recsys = RecommendationSystem(
    semantic_project_retriever=project_retriever,
    semantic_code_retriever=code_retriever, 
    section_description="Our Recommendation System (RecSys) helps you discover projects and code examples you may find interesting."
)
