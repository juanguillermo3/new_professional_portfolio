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
from front_end_utils import render_section_separator, render_external_link_button, prettify_title, tags_in_twitter_style
from media_carousel import MediaCarousel  # Assuming this is the correct import
from visual_media import  VisualContentGallery
from front_end_for_recommended_content import html_for_item_data, html_for_milestones_from_project_metadata
from portfolio_section import PortfolioSection
from exceptional_ui import apply_custom_tooltip

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
        #self.section_header = section_header
        #self.section_description = section_description
        
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
    ⚙️ The RecSys engine recommends items based on visual prominence and freshness. 
    Items with highlighted content are ranked first, followed by those with the most recent updates. 
    Special ranking positions are applied where defined, and the results are filtered by project and search query.
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
        st.markdown(html_for_item_data(rec), unsafe_allow_html=True)
    
        unique_hash = hashlib.md5(rec['title'].encode()).hexdigest()
        button_id = f"galleria_{unique_hash}"
    
        if "image_path" in rec:
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
    # Updated render method
    #
    def render(self):
        """Render method with Galleria callback integration and smooth media transitions."""
        
        self._render_headers()  # Render headers from the portfolio section class
    
        # Display the ranker's logic
        st.markdown(f'{self.RANKER_LOGIC}', unsafe_allow_html=True)
    
        # Display control widgets as a grid
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
    
            # Emit event (differentiate project change vs. interaction)
            event_type = "ACTIVE_PROJECT_CHANGED" if project_changed else "ACTIVE_PROJECT_INTERACTED"
            st.session_state.project_event = f"{event_type}: {selected_project}"
    
        with cols[1]:
            query = st.text_input(
                "🔍 Search for by keyword/library (e.g., Python, R):",
                placeholder="Type a keyword and press Enter",
            )
    
        # Fetch recommendations
        recommendations = self.rank_items(query, selected_project)
    
        # Display project metadata if applicable
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
    

    def handle_galleria_click(self, rec):
        """
        Handle the click event for the galleria item and display its content.
        Instead of calling render_item_visual_content directly, use the GalleryCollection.
        Syncs active galleria with session state.
        """
        
        # Prepare galleria_params
        galleria_params = {
            'title': rec.get('title', None),
            'description': rec.get('description', None),
            'media_path': rec.get('image_path', None),
            'width': self.MEDIA_CONTAINER_WIDTH,
            'height': self.MEDIA_CONTAINER_HEIGHT
        }
    
        # Validate that the required parameters are present
        missing_params = [key for key, value in galleria_params.items() if value is None]
        if missing_params:
            # If any required parameters are missing, output a debug message
            st.write(f"Debug: Missing parameters for Galleria - {', '.join(missing_params)}")
            return  # Exit the function if the schema is not compliant
    
        # Create a new VisualContentGallery instance
        st.session_state["active_galleria"] = VisualContentGallery(
            title=rec['title'],
            description=rec['description'],
            media_path=rec['image_path'],
            width=self.MEDIA_CONTAINER_WIDTH,
            height=self.MEDIA_CONTAINER_HEIGHT
        )
    
        # Clear the media placeholder
        self.media_placeholder.empty()
    
        # Render the new gallery instance
        with st.spinner("Loading media..."):
            with self.media_placeholder.container():
                st.session_state["active_galleria"].render()

    def render(self):
        """Render method with Galleria callback integration and smooth media transitions."""
        
        self._render_headers()  # Render headers from the portfolio section class
    
        # Display the ranker's logic
        st.markdown(f'{self.RANKER_LOGIC}', unsafe_allow_html=True)
    
        # Display control widgets as a grid
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
    
            # Emit event (differentiate project change vs. interaction)
            event_type = "ACTIVE_PROJECT_CHANGED" if project_changed else "ACTIVE_PROJECT_INTERACTED"
            st.session_state.project_event = f"{event_type}: {selected_project}"
    
        with cols[1]:
            query = st.text_input(
                "🔍 Search for by keyword/library (e.g., Python, R):",
                placeholder="Type a keyword and press Enter",
            )
    
        # Fetch recommendations
        recommendations = self.rank_items(query, selected_project)
    
        # Display project metadata if applicable
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

    def render_project_metadata(self, project_metadata, display_milestones=True, margin_percent=10):
        """Render project title, description, tags, milestones, code sample count, and media content."""
        
        video_filename = f"{project_metadata['title'].replace(' ', '_').lower()}_theme.mp4"
        video_path = os.path.join('assets', video_filename)
        
        tags_html = tags_in_twitter_style(project_metadata.get("tags", []))
        description_html = markdown.markdown(f"{project_metadata['description']} {tags_html}")
    
        # Title and description
        st.markdown(
            f"""
            <div style="text-align: center;"><h3>{prettify_title(project_metadata['title'])}</h3></div>
            <div style="text-align: justify; margin-left: {margin_percent}%; margin-right: {margin_percent}%;">{description_html}</div>
            """,
            unsafe_allow_html=True,
        )
    
        # Milestones section
        milestone_margin = margin_percent * 1.5  
        if display_milestones:
            milestone_html = html_for_milestones_from_project_metadata(project_metadata)
            if milestone_html:  
                st.markdown(
                    f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%;'>{milestone_html}</div>",
                    unsafe_allow_html=True
                )
    
        # Code sample count section
        project_title = project_metadata['title'].lower()
        sample_count = self.project_item_counts.get(project_title, 0)
        sample_html = f"<div style='margin-left:{milestone_margin}%;margin-right:{milestone_margin}%; color:#3A86FF; font-size:105%; font-weight:95%;'>💾 {sample_count} code samples indexed</div>"
        st.markdown(sample_html, unsafe_allow_html=True)
    
        # Media placeholder
        st.markdown("<br>", unsafe_allow_html=True)
        self.media_placeholder = st.empty()
    
        # Render media content
        self._render_media_content(video_path)
    
    def _render_media_content(self, video_path):
        """Handles the rendering of media content (either Galleria or Video)."""
        
        active_galleria = st.session_state.get("active_galleria", False)
        project_event = st.session_state.get("project_event", "")
        
        # Determine if we should force a video render
        project_switched = project_event.startswith("ACTIVE_PROJECT_CHANGED")
        
        if active_galleria and not project_switched:
            with self.media_placeholder.container():
                active_galleria.render()
        elif os.path.exists(video_path):
            self.media_placeholder.video(video_path, loop=True, autoplay=True, muted=True)
        else:
            self.media_placeholder.warning("Video not found.")
        
        # Reset project event to avoid unnecessary re-triggers
        st.session_state["project_event"] = "ACTIVE_PROJECT_INTERACTED"


    
    

# Example usage
# Initialize RecSys with custom header and description
recsys = RecommendationSystem(
    #section_header="Customized Recommendations 🔍", 
    section_description="My research RecSys to make my portfolio discoverable. This RecSys versions uses exact pattern on item titles/descriptions, while more flexible, NLP type of matching is under development."
)

