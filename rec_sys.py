
"""
title: Recommendation System
description: Current implementation of the RecSys, featuring a vanilla ranking that sorts items by the most recently updated, filters by query (exact matching), and allows filtering by project.
"""

import os
import re
import random
import streamlit as st
from datetime import datetime
from git_api_utils import load_modules_metadata
from git_api_utils import load_repos_metadata as load_github_metadata
from app_end_metadata import load_repos_metadata as load_app_metadata
import hashlib
from front_end_utils import render_section_separator
from media_carousel import MediaCarousel  # Assuming this is the correct import
import time

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

        # Sort the projects
        self._sort_projects()
        
        # Prepare project titles and default project
        self._prepare_project_titles_and_default()

        # Pre-instantiate the media carousels for all projects with galleria folders
        self.galleria_carousels = self._initialize_galleria_carousels()

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

    def _prepare_project_titles_and_default(self):
        """Prepares project titles for selection and determines the default project."""
        self.project_titles = [
            f"{repo['title']} (Ongoing)" if repo.get("ongoing", False) else repo["title"]
            for repo in self.repos_metadata
        ]

        self.title_mapping = {
            self.prettify_title(title): repo["title"]
            for title, repo in zip(self.project_titles, self.repos_metadata)
        }

        self.default_project = self.repos_metadata[0]["title"] if self.repos_metadata else "No Projects"

    def _initialize_galleria_carousels(self):
        """Prepares media carousels for projects with galleria folders."""
        carousels = {}
        for repo in self.repos_metadata:
            galleria_folder = os.path.join('assets', f"{repo['title'].replace(' ', '_').lower()}_galleria")
            if os.path.exists(galleria_folder):
                carousels[repo["title"]] = MediaCarousel(galleria_folder)
        return carousels

    def rank_items(self, query=None, selected_project=None):
        """Rank the items by the last updated date and apply filters."""
        # Step 1: Sort items by 'last_updated' from newest to oldest,
        # Treat items without 'last_updated' as if they are the oldest.
        ranked_items = sorted(self.metadata_list, key=lambda x: datetime.strptime(x.get('last_updated', '1970-01-01T00:00:00Z'), "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
    
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


    def render_title_and_description(self, project_metadata):
        """Renders the title and description of a project, centered and with margins, with inline hashtags."""

        # Professional and innovative color palette
        color_palette = [
            "#1E3A8A",  # Deep Blue (Tech/Professional)
            "#065F46",  # Dark Green (Trust/Innovation)
            "#9333EA",  # Purple (Creative/Modern)
            "#0EA5E9",  # Cyan Blue (Fresh/Innovative)
            "#B91C1C",  # Deep Red (Bold/Strong)
            "#7C3AED",  # Vibrant Indigo (Techy Feel)
            "#2563EB",  # Solid Blue (Corporate/Stable)
            "#059669",  # Teal Green (Sophisticated)
        ]

        # Generate inline tags with improved styling
        tags_html = " ".join(
            f'<span style="color: {random.choice(color_palette)}; font-size: 0.9em; font-weight: 600;">#{tag}</span>'
            for tag in project_metadata.get("tags", [])
        )

        # Render HTML with inline styling
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <h3>{self.prettify_title(project_metadata['title'])}</h3>
            </div>
            <div style="text-align: justify; margin-left: 10%; margin-right: 10%; margin-bottom: 20px;">
                <p>{project_metadata['description']} {tags_html}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render(self):
        """
        Render the Hero area in Streamlit with the main content always visible
        and the code samples + contact button inside expandable content.
        """
        # Two-column layout for quote and avatar
        col1, col2 = st.columns([2, 1])
    
        # Render the quote (always visible)
        with col1:
            st.markdown("""<style>
            .hero-quote {
                font-style: italic;
                font-size: 1.5em;
                line-height: 1.8;
                margin: 0 auto;
                max-width: 800px;
                color: #333333;
                text-align: justify;
                padding-bottom: 20px;
            }
            .hero-avatar-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            </style>""", unsafe_allow_html=True)
    
            # Render each paragraph separately in the quote
            for paragraph in self.quote:
                st.markdown(f'<p class="hero-quote">{paragraph}</p>', unsafe_allow_html=True)
    
        # Render the avatar with caption (always visible)
        if self.avatar_image:
            with col2:
                st.markdown('<div class="hero-avatar-container">', unsafe_allow_html=True)
                st.image(f"assets/{self.avatar_image}", caption=self.avatar_caption, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
        # Render the expandable content (with fixed silver background color and opened by default)
        with st.expander("Explore more", expanded=True):  
            # Add silver background color to the expandable section
            st.markdown("""
            <style>
            .css-1v3fvcr {
                background-color: #C0C0C0 !important;  /* Silver color */
            }
            .css-1v3fvcr .streamlit-expanderHeader {
                background-color: #C0C0C0 !important;  /* Silver color */
                color: black;
            }
            </style>
            """, unsafe_allow_html=True)
    
            # Render the 5+1 key differentials section
            st.markdown(self.detailed_offering)
    
            # Render the code samples (hidden by default)
            self.render_code_samples()
    
        # Render the contact button (hidden by default)
        self.render_contact_button()
    
        # Galleria button with fixed width of 60% of the container
        st.markdown("""
        <style>
        .galleria-button {
            width: 60% !important;  /* Fixed width of 60% */
        }
        </style>
        """, unsafe_allow_html=True)
        st.button("Galleria", key="galleria", use_container_width=True)
    
        # Buttons with external links (simplified labels and fixed width)
        st.markdown("""
        <style>
        .external-button {
            width: 200px !important;  /* Fixed width of 200px */
        }
        </style>
        """, unsafe_allow_html=True)
    
        # GitHub button
        st.button("GitHub", key="github", use_container_width=True, help="Go to GitHub", css_class="external-button")
    
        # Sheets button
        st.button("Sheets", key="sheets", use_container_width=True, help="Go to Sheets", css_class="external-button")

    
                
    def handle_galleria_click(self):
        """Handle the transition when the Galleria button is clicked."""
        if self.media_placeholder:
            self.media_placeholder.empty()  # Clear previous content
    
        # Apply transition effect
        self.apply_transition_styles()
    
        time.sleep(0.5)  # Short delay for the transition effect
    
        # Switch content while maintaining the fixed container size
        content_type = "image"  # Example: Can be "image", "text", etc.
    
        MEDIA_CONTAINER_WIDTH = "700px"
        MEDIA_CONTAINER_HEIGHT = "400px"
    
        if content_type == "image":
            self.media_placeholder.markdown(
                f"""
                <div id="media-container" style="width: {MEDIA_CONTAINER_WIDTH}; height: {MEDIA_CONTAINER_HEIGHT};">
                    <img src="https://via.placeholder.com/300" 
                         style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px;">
                </div>
                """,
                unsafe_allow_html=True
            )
        elif content_type == "text":
            self.media_placeholder.markdown(
                f"""
                <div id="media-container" style="width: {MEDIA_CONTAINER_WIDTH}; height: {MEDIA_CONTAINER_HEIGHT};">
                    <p style="font-size: 18px; text-align: center; color: #333;">
                        This is a placeholder text. Replace it with a video or other media.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


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

    
    def render(self):
        """Render method with Galleria callback integration."""
        st.subheader(self.section_header)
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.section_description}</p>', unsafe_allow_html=True)
    
        # Add space to separate the section description from the controls
        st.markdown("")
        
        # Project Filter - Comes First
        prettified_titles = [self.prettify_title(title) for title in self.project_titles]
        selected_pretty_project = st.selectbox("📂 Filter recommendations by project:", prettified_titles, index=0)
        selected_project = self.title_mapping[selected_pretty_project]
                
        # Keyword Search - Comes After
        query = st.text_input("🔍 Search for recommendations by keyword (e.g., Python, R):", placeholder="Type a keyword and press Enter")
    
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
                    
        # Incorporate Galleria if the folder exists
        if selected_project and project_metadata:
            render_section_separator()
            self.show_galleria(selected_project)

            
    def show_galleria(self, project_title):
        """Check if the galleria folder exists and render the details."""
        galleria_path = os.path.join('assets', f"{project_title}_galleria")
        if os.path.exists(galleria_path):
            st.markdown(f"### Galleria for {project_title}")
            self.galleria_carousels[project_title].render()
        else:
            st.warning(f"Galleria for {project_title} not found.")

# Example usage
# Initialize RecSys with custom header and description
recsys = RecommendationSystem(
    #section_header="Customized Recommendations 🔍", 
    section_description="My research RecSys to make my portfolio discoverable. This RecSys versions uses exact pattern on item titles/descriptions, while more flexible, NLP type of matching is under development."
)

