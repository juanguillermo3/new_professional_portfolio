
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
        """Rank the items by priority on 'galleria' and 'last_updated', then apply filters."""
        
        def parse_boolean(value):
            """Helper function to safely parse boolean values from strings."""
            return str(value).strip().lower() == "true"
    
        # Step 1: Sort by two criteria:
        #   - Priority to items with "galleria" evaluating to True.
        #   - Then, sort by 'last_updated' in descending order.
        ranked_items = sorted(
            self.metadata_list,
            key=lambda x: (
                not parse_boolean(x.get("galleria", "False")),  # False (desired) comes first
                datetime.strptime(x.get('last_updated', '1970-01-01T00:00:00Z'), "%Y-%m-%dT%H:%M:%SZ"),
            ),
            reverse=True,  # Reverse needed because we want latest dates first
        )
    
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

    #
    def render_card(self, rec, is_project=False):
        """Render a single recommendation card with fixed height and scrollable content."""
        background_color = "#f4f4f4" if not is_project else "#fff5e6"  # Silver background for non-project items
        border_style = "2px solid gold" if is_project else "1px solid #ddd"
        
        # Set the fixed height to half of the previous value (150px)
        card_height = "150px"  # New fixed height for the card
        overflow_style = "overflow-y: auto;"  # Allow scrolling for overflow content
    
        # Check if 'galleria' is present in the card
        galleria_present = "galleria" in rec
        
        # Modify the title to include a star if 'galleria' is present
        title = self.prettify_title(rec['title'])
        if galleria_present:
            title = f"⭐ {title}"
        
        # Render the card with a fixed height, semi-transparent title, and scrollable content
        st.markdown(
            f"""
            <div style="background-color: {background_color}; border: {border_style}; 
                        border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                        padding: 10px; text-align: center; height: {card_height}; {overflow_style}; 
                        position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; right: 0; background-color: rgba(255, 255, 255, 0.7); 
                            padding: 5px 10px; border-radius: 10px 10px 0 0; font-size: 16px; font-weight: bold; z-index: 10;">
                    {title}
                </div>
                <div style="margin-top: 40px; padding: 0 10px; overflow-y: auto; height: calc(100% - 40px); text-align: justify;">
                    {rec['description']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
        # JavaScript to reset scroll to top when hover ends
        st.markdown(
            """
            <script>
            const card = document.querySelector('div[data-testid="stMarkdownContainer"]');
            card.addEventListener('mouseenter', function() {
                card.scrollTop = 0;
            });
            </script>
            """,
            unsafe_allow_html=True,
        )
        
        # Generate a unique hash for the button ID based on the card title
        unique_hash = hashlib.md5(rec['title'].encode()).hexdigest()
        button_id = f"galleria_{unique_hash}"  # Unique button ID
        
        # Custom CSS for the Galleria button only
        if galleria_present:
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
                    width: 60% !important;  /* Fixed width for Galleria button */
                    margin: 5px auto;  /* Reduced margin */
                    display: block;
                }
                div[data-testid="stButton"] > button:hover {
                    background-color: #ffd700 !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
    
            # Streamlit button with a unique key
            if st.button("See Galleria", key=button_id):
                # Update media placeholder here, triggering a transition
                self.handle_galleria_click(rec)
    
        # Button row with fixed width buttons (for GitHub, Sheets, etc.)
        button_cols = st.columns(2) if "url" in rec and "report_url" in rec else [st.columns(1)[0]]
        
        if "url" in rec and rec["url"]:
            with button_cols[0]:
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center; margin-top: 5px;">
                        <a href="{rec['url']}" target="_blank" 
                           style="text-decoration: none; width: 200px; display: block; margin: 0 auto;">
                            <button style="background-color: #333; color: white; 
                                           border: none; padding: 10px 20px; 
                                           text-align: center; text-decoration: none; 
                                           font-size: 14px; cursor: pointer; 
                                           border-radius: 5px; width: 100%; margin: 0 auto;">
                                GitHub
                            </button>
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        
        if "report_url" in rec and rec["report_url"]:
            with button_cols[-1]:
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center; margin-top: 5px;">
                        <a href="{rec['report_url']}" target="_blank" 
                           style="text-decoration: none; width: 200px; display: block; margin: 0 auto;">
                            <button style="background-color: #34A853; color: white; 
                                           border: none; padding: 10px 20px; 
                                           text-align: center; text-decoration: none; 
                                           font-size: 14px; cursor: pointer; 
                                           border-radius: 5px; width: 100%; margin: 0 auto;">
                                Sheets
                            </button>
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        
        # Add more margin between the button area and the next row of card items
        st.markdown("<br><br>", unsafe_allow_html=True)
        
    def handle_galleria_click(self, rec):
        """
        Handle the click event for the galleria item and display its content.
        The content includes a title, a brief description, and a background image.
        Hardcoded mockup values are used for now.
        """
        # Clear any existing content in the media placeholder
        self.media_placeholder.empty()
    
        # Use the title and description from the rec object
        item_title = rec.get('title', 'No Title Available')
        item_description = rec.get('description', 'No description available.')
        image_path = rec.get('image_path', 'assets/mock_up_galleria.png')  # Adjust if image path is stored in rec
    
        # Begin using the placeholder context
        with self.media_placeholder.container():
    
            # Check if the image exists at the provided path and display it
            try:
                # Display the image
                st.image(image_path, use_container_width=True)
            except Exception as e:
                # Show a debug statement if there is an issue with loading the image
                st.error(f"Error loading image: {str(e)}")
    
            # Display the title and description in a single paragraph with inline styling
            st.markdown(
                f"""
                <div style="position: relative; background-color: rgba(0, 0, 0, 0.4); padding: 15px; border-radius: 8px; color: white;">
                    <div style="font-size: 20px; font-weight: 300; line-height: 1.6; text-align: center; margin: 0;">
                        <span style="font-size: 24px; font-weight: 600; color: #fff; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.6);">
                            {item_title}
                        </span>
                        <br>
                        <span style="font-size: 16px; font-weight: 300; color: #eee; text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);">
                            {item_description}
                        </span>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    
            # Add space after the media content (appendix space)
            st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

            
            
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
        #if selected_project and project_metadata:
        #    render_section_separator()
        #    #self.show_galleria(selected_project)

            
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

