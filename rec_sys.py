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
from front_end_for_recommended_content import html_for_item_data, html_for_milestones_from_project_metadata
from portfolio_section import PortfolioSection
from exceptional_ui import apply_custom_tooltip, _custom_tooltip_with_frost_glass_html
from biotech_lab import frost_glass_mosaic, _custom_tooltip_with_frost_glass_html
from expandable_text import expandable_text_html

import os
from dotenv import load_dotenv
load_dotenv()
MOCK_INFO_PREFIX = os.getenv("MOCK_INFO", "[MOCK INFO]")

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
    def __init__(self, num_recommended_items=6, num_columns=3,
                 section_header="Recommendation System 🎯",
                 section_description="Discover content tailored to your needs. Use the search bar to find recommendations and filter by project category."):

        super().__init__(
            title=section_header,
            description=section_description,
            verified=self.DATA_VERIFIED,  # Use subclass defaults
            early_dev=self.EARLY_DEVELOPMENT_STAGE,
            ai_content=not self.DATA_VERIFIED  # This ensures consistency
        )
                     
        self.num_recommended_items = num_recommended_items
        self.num_columns = num_columns
        
        self.repos_metadata = combine_metadata()  
        self.metadata_list = load_modules_metadata()  

        self._sort_projects()
        self._prepare_project_titles_and_default()

        #self.gallery_collection = GalleryCollection()
        self.active_galleria = None
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

        card_html, tooltip_html, tooltip_styles=html_for_item_data(rec)
        #st.markdown(card_html, unsafe_allow_html=True)
        #st.markdown(tooltip_html, unsafe_allow_html=True)
        #st.markdown(tooltip_styles, unsafe_allow_html=True)

        unique_hash = hashlib.md5(rec['title'].encode()).hexdigest()
        button_id = f"galleria_{unique_hash}"
    

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
    
    
    def _render_control_panel(self):
        """Render the control panel with sticky positioning inside its section."""
        
        # Inject CSS to make the control panel sticky
        st.markdown(
            """
            <style>
            .control-panel {
                position: sticky;
                top: 10px;  /* Controls how soon it sticks */
                background: white;
                padding: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                z-index: 1000;  /* Ensures it stays above other elements */
                border-radius: 8px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
        # Render control panel inside a styled div
        #st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    
        cols = st.columns(2)
    
        with cols[0]:
            prettified_titles = [prettify_title(title) for title in self.project_titles]
            selected_pretty_project = st.selectbox(
                "📂 Filter by project:", prettified_titles, index=0, key="active_project"
            )
            selected_project = self.title_mapping[selected_pretty_project]
    
            # Ensure event propagation always occurs
            previous_project = st.session_state.get("last_active_project", None)
            project_changed = previous_project != selected_project
            
            st.session_state.last_active_project = selected_project  # Update state
            
            # Emit event
            event_type = "ACTIVE_PROJECT_CHANGED" if project_changed else "ACTIVE_PROJECT_INTERACTED"
            st.session_state.project_event = f"{event_type}: {selected_project}"
    
        with cols[1]:
            query = st.text_input(
                "🔍 Search for by keyword/library (e.g., Python, R):",
                placeholder="Type a keyword and press Enter",
            )
    
        st.markdown('</div>', unsafe_allow_html=True)  # Close the control panel div
    
        return selected_project, query

    def render(self):
        """Render method with smooth project transitions using Streamlit's key-based styling."""
        
        #self._render_headers()  # Render headers from the portfolio section class
        
        # Display ranker's logic
        #st.markdown(f'{self.RANKER_LOGIC}', unsafe_allow_html=True)
    
        # Create a container with a unique key (Streamlit auto-assigns a CSS class)
        with st.container(key="project_data_container"):
            # Render the sticky control panel and retrieve user selections
            selected_project, query = self._render_control_panel()
            
            # Fetch recommendations
            recommendations = self.rank_items(query, selected_project)
    
            # Fetch project metadata
            project_metadata = next(
                (repo for repo in self.repos_metadata if repo["title"].lower() == selected_project.lower()), 
                None
            ) if selected_project != "All Projects" else None
    
            if project_metadata:
                self.render_project_metadata(project_metadata)
    
            # Render filtering message
            filter_message = f"Showing all results for project {prettify_title(selected_project)}"
            if query:
                filter_message += f" (and for keyword: {query})"
    
            st.markdown(
                f'<p style="font-style: italic; color: #555; font-size: 105%; font-weight: 550;">{filter_message}</p>',
                unsafe_allow_html=True
            )
    
            # Render recommendations in a grid
            for i in range(0, len(recommendations), self.num_columns):
                cols = st.columns(self.num_columns)
                for col, rec in zip(cols, recommendations[i: i + self.num_columns]):
                    with col:
                        self.render_card(rec, is_project=rec.get("is_project", False))

    def render_project_metadata(self, project_metadata, display_milestones=True, margin_percent=0):
        """Render project title, description, tags, milestones, code sample count, and media content."""
        
        video_filename = f"{project_metadata['title'].replace(' ', '_').lower()}_theme.mp4"
        video_path = os.path.join('assets', video_filename)
        
        tags_html = tags_in_twitter_style(project_metadata.get("tags", []))
        
        # Parse description as Markdown first
        parsed_description = markdown.markdown(project_metadata['description'])
    
        # Generate expandable text effect for the description
        description_html, description_styles = expandable_text_html(parsed_description)
        
        # Convert to Markdown and append tags
        description_html = markdown.markdown(f"{tags_html} {description_html} ")


        # Media placeholder
        #st.markdown("<br>", unsafe_allow_html=True)
        self.media_placeholder = st.empty()
    
        # Render media content
        if os.path.exists(video_path):
            self.media_placeholder.video(video_path, loop=True, autoplay=True, muted=True)
    
        # Title and description with expandable effect
        st.markdown(
            f"""
            <div style="text-align: center;"><h3>{prettify_title(project_metadata['title'])}</h3></div>
            <div style="text-align: justify; margin-left: {margin_percent}%; margin-right: {margin_percent}%;">
                {description_html}
            </div>
            <style>{description_styles}</style>
            """,
            unsafe_allow_html=True,
        )
    
        # Milestones section
        milestone_margin = margin_percent * 1.5  
        
        if display_milestones:
          
            # Render achieved milestones
            achieved_html = html_for_milestones_from_project_metadata(project_metadata=project_metadata, milestone_type="achieved_milestones")
            if achieved_html:
                st.markdown(
                    f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%;'>{achieved_html}</div>",
                    unsafe_allow_html=True
                )
        
            # Render upcoming milestones
            upcoming_html = html_for_milestones_from_project_metadata(project_metadata=project_metadata, milestone_type="next_milestones")
            if upcoming_html:
                st.markdown(
                    f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%;'>{upcoming_html}</div>",
                    unsafe_allow_html=True
                )
        
            # Fetch and render code samples from repository
            code_samples = self._fetch_files(project_metadata['title'])
            code_samples_html = html_for_milestones_from_project_metadata(milestones=code_samples, milestone_type="code_samples")
            if code_samples_html:
                st.markdown(
                    f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%;'>{code_samples_html}</div>",
                    unsafe_allow_html=True
                )



    def _render_control_panel(self):
        """Render the control panel with sticky positioning inside its section."""
        
        # Inject CSS to make the control panel sticky
        st.markdown(
            """
            <style>
            .control-panel {
                position: sticky;
                top: 10px;
                background: white;
                padding: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                z-index: 1000;
                border-radius: 8px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
        # Render keyword search only
        query = st.text_input(
            "🔍 Search for by keyword/library (e.g., Python, R):",
            placeholder="Type a keyword and press Enter",
        )
        
        return query
    
    def render(self):
        """Render method displaying all projects in a portfolio-style view."""
        
        # Render the sticky control panel and retrieve user query
        query = self._render_control_panel()
        
        # Iterate over all projects and render them one by one
        for project_metadata in self.repos_metadata:
            # Fetch recommendations per project
            recommendations = self.rank_items(query, project_metadata["title"])
            
            # Render metadata for each project
            self.render_project_metadata(project_metadata)
            
            # Render filtering message
            filter_message = f"Showing all results for project {prettify_title(project_metadata['title'])}"
            if query:
                filter_message += f" (and for keyword: {query})"
            
            st.markdown(
                f'<p style="font-style: italic; color: #555; font-size: 105%; font-weight: 550;">{filter_message}</p>',
                unsafe_allow_html=True
            )
            
            # Render recommendations in a grid
            for i in range(0, len(recommendations), self.num_columns):
                cols = st.columns(self.num_columns)
                for col, rec in zip(cols, recommendations[i: i + self.num_columns]):
                    with col:
                        self.render_card(rec, is_project=rec.get("is_project", False))
            
            # Horizontal separator between projects
            st.markdown("---")
    

    def render_project_metadata(self, project_metadata, display_milestones=True, margin_percent=0):
        """Render project title, video, and metadata in an ancillary container."""
        
        video_filename = f"{project_metadata['title'].replace(' ', '_').lower()}_theme.mp4"
        video_path = os.path.join('assets', video_filename)
        
        tags_html = tags_in_twitter_style(project_metadata.get("tags", []))
        parsed_description = markdown.markdown(project_metadata['description'])
        description_html, description_styles = expandable_text_html(parsed_description)
        description_html = markdown.markdown(f"{tags_html} {description_html} ")
    
        # Unique media placeholder for each project
        media_placeholder = st.empty()
        
        if os.path.exists(video_path):
            media_placeholder.video(video_path, loop=True, autoplay=True, muted=True)
        
        st.markdown(
            f"""
            <div style="text-align: center;"><h3>{prettify_title(project_metadata['title'])}</h3></div>
            """,
            unsafe_allow_html=True,
        )

        # Generate a unique key for the ancillary container
        unique_key = hashlib.md5(f"{project_metadata['title']}_{time.time()}".encode()).hexdigest()
        with st.container(key=unique_key):

            st.write("Inside ancillary container")
              
            st.markdown(
                f"""
                <div style="text-align: justify; margin-left: {margin_percent}%; margin-right: {margin_percent}%;">
                    {description_html}
                </div>
                <style>{description_styles}</style>
                """,
                unsafe_allow_html=True,
            )
    
            milestone_margin = margin_percent * 1.5  
            
            if display_milestones:
                achieved_html = html_for_milestones_from_project_metadata(project_metadata=project_metadata, milestone_type="achieved_milestones")
                if achieved_html:
                    st.markdown(
                        f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%;'>{achieved_html}</div>",
                        unsafe_allow_html=True
                    )
            
                upcoming_html = html_for_milestones_from_project_metadata(project_metadata=project_metadata, milestone_type="next_milestones")
                if upcoming_html:
                    st.markdown(
                        f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%;'>{upcoming_html}</div>",
                        unsafe_allow_html=True
                    )
            
                code_samples = self._fetch_files(project_metadata['title'])
                code_samples_html = html_for_milestones_from_project_metadata(milestones=code_samples, milestone_type="code_samples")
                if code_samples_html:
                    st.markdown(
                        f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%;'>{code_samples_html}</div>",
                        unsafe_allow_html=True)
                
            st.write("Inside ancillary container"+ unique_key)      
        self._style_ancillary_component(unique_key)

    def _style_ancillary_component(self, component_key):
        """Apply CSS styles to ensure the ancillary component takes no space and appears smoothly when triggered."""
        st.markdown(
            f"""
            <style>
            .st-key-{component_key} {{
                opacity: 0;
                visibility: hidden;
                max-height: 0;
                overflow: hidden;
                padding: 0;
                margin: 0;
                transition: opacity 0.5s ease-in-out, max-height 0.5s ease-in-out, visibility 0.5s ease-in-out;
            }}
            
            .st-key-{component_key} * {{
                opacity: 0;
                visibility: hidden;
                max-height: 0;
                overflow: hidden;
                padding: 0;
                margin: 0;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    def render(self):
        """Render method displaying all projects in a portfolio-style view."""
        
        # Render the sticky control panel and retrieve user query
        query = self._render_control_panel()
        
        # Iterate over all projects and render them one by one
        for project_metadata in self.repos_metadata:
            self.render_project_metadata_and_recommendations(project_metadata, query)
            
            # Horizontal separator between projects
            st.markdown("---")
    
    def render_project_metadata_and_recommendations(self, project_metadata, query, display_milestones=True, margin_percent=0):
        """Render project title, video, metadata, and recommendations in an ancillary container."""
        
        video_filename = f"{project_metadata['title'].replace(' ', '_').lower()}_theme.mp4"
        video_path = os.path.join('assets', video_filename)
        
        tags_html = tags_in_twitter_style(project_metadata.get("tags", []))
        parsed_description = markdown.markdown(project_metadata['description'])
        description_html, description_styles = expandable_text_html(parsed_description)
        description_html = markdown.markdown(f"{tags_html} {description_html} ")
    
        # Unique media placeholder for each project
        media_placeholder = st.empty()
        
        if os.path.exists(video_path):
            media_placeholder.video(video_path, loop=True, autoplay=True, muted=True)
        
        st.markdown(
            f"""
            <div style="text-align: center;"><h3>{prettify_title(project_metadata['title'])}</h3></div>
            """,
            unsafe_allow_html=True,
        )

        # Generate a unique key for the ancillary container
        unique_key = hashlib.md5(f"{project_metadata['title']}_{time.time()}".encode()).hexdigest()
        with st.container(key=unique_key):
            
            st.markdown(
                f"""
                <div style="text-align: justify; margin-left: {margin_percent}%; margin-right: {margin_percent}%;">
                    {description_html}
                </div>
                <style>{description_styles}</style>
                """,
                unsafe_allow_html=True,
            )
    
            milestone_margin = margin_percent * 1.5  
            
            if display_milestones:
                achieved_html = html_for_milestones_from_project_metadata(project_metadata=project_metadata, milestone_type="achieved_milestones")
                if achieved_html:
                    st.markdown(
                        f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%;'>{achieved_html}</div>",
                        unsafe_allow_html=True
                    )
                
                upcoming_html = html_for_milestones_from_project_metadata(project_metadata=project_metadata, milestone_type="next_milestones")
                if upcoming_html:
                    st.markdown(
                        f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%;'>{upcoming_html}</div>",
                        unsafe_allow_html=True
                    )
                
                code_samples = self._fetch_files(project_metadata['title'])
                code_samples_html = html_for_milestones_from_project_metadata(milestones=code_samples, milestone_type="code_samples")
                if code_samples_html:
                    st.markdown(
                        f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%;'>{code_samples_html}</div>",
                        unsafe_allow_html=True)

            # Fetch recommendations per project
            recommendations = self.rank_items(query, project_metadata["title"])
            
            # Render filtering message
            filter_message = f"Showing all results for project {prettify_title(project_metadata['title'])}"
            if query:
                filter_message += f" (and for keyword: {query})"
            
            st.markdown(
                f'<p style="font-style: italic; color: #555; font-size: 105%; font-weight: 550;">{filter_message}</p>',
                unsafe_allow_html=True
            )
            
            # Render recommendations in a grid
            for i in range(0, len(recommendations), self.num_columns):
                cols = st.columns(self.num_columns)
                for col, rec in zip(cols, recommendations[i: i + self.num_columns]):
                    with col:
                        self.render_card(rec, is_project=rec.get("is_project", False))
        
        #self._style_ancillary_component(unique_key)
    
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





# Example usage
# Initialize RecSys with custom header and description
recsys = RecommendationSystem(
    #section_header="Customized Recommendations 🔍", 
    section_description="This section implements a Recommendation System (RecSys) to make my portfolio discoverable."
)

