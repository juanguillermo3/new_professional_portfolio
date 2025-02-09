
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
from front_end_utils import render_section_separator, render_external_link_button, prettify_title
from media_carousel import MediaCarousel  # Assuming this is the correct import

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

    RANKER_LOGIC="""
    ### Recommender System Overview
    The recommender system prioritizes items based on their relevance and freshness, ensuring that the most important and recently updated content appears first. It allows for manual adjustments to the ranking, accommodating special preferences. The system can also filter results based on user-defined projects or search queries to ensure that recommendations are highly relevant and tailored to individual needs. The final output is a personalized list of the top recommendations.
    """"

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


    #
    # front end representation of items
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
        title = prettify_title(rec['title'])
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
    
        # Determine how many buttons will be displayed
        buttons = []
        if "url" in rec and rec["url"]:
            buttons.append(("GitHub", rec["url"], "#333"))  # Dark Gray
        if "report_url" in rec and rec["report_url"]:
            buttons.append(("Sheets", rec["report_url"], "#34A853"))  # Google Sheets Green
        if "colab_url" in rec and rec["colab_url"]:
            buttons.append(("Colab Notebook", rec["colab_url"], "#F9AB00"))  # Colab Yellow-Orange
    
        # Create columns dynamically based on the number of buttons
        button_cols = st.columns(len(buttons)) if buttons else []
    
        for col, (label, url, color) in zip(button_cols, buttons):
            with col:
                st.markdown(render_external_link_button(url, label, color), unsafe_allow_html=True)
    
        # Add more margin between the button area and the next row of card items
        st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Default media dimensions (class-level static attributes)
    MEDIA_CONTAINER_WIDTH = "700px"
    MEDIA_CONTAINER_HEIGHT = "400px"

    def handle_galleria_click(self, rec, width=None, height=None):
        """
        Handle the click event for the galleria item and display its content.
        The content includes a title, a brief description, and a background image or other media.
        
        Parameters:
        - rec (dict): The dictionary containing media metadata.
        - width (str): Optional. The width of the media container (default: class-level).
        - height (str): Optional. The height of the media container (default: class-level).
        """
        # Clear any existing content in the media placeholder
        self.media_placeholder.empty()
    
        # Use defaults if width/height not provided
        width = width or self.MEDIA_CONTAINER_WIDTH
        height = height or self.MEDIA_CONTAINER_HEIGHT
    
        # Extract metadata from `rec`
        item_title = rec.get('title', 'No Title Available')
        item_description = rec.get('description', 'No description available.')
        image_path = rec.get('image_path', None)  # Ensure correct key is used
    
        # Debug statement if image_path is missing
        if not image_path:
            st.error("Error: 'image_path' key not found in the provided data.")
            return
    
        # Show spinner while loading content
        with st.spinner("Loading media..."):
            # Begin using the placeholder context
            with self.media_placeholder.container():
                # **Insert a full-width dummy div to reset layout constraints**
                st.markdown(
                    "<div style='width: 100%; height: 1px;'></div>",
                    unsafe_allow_html=True
                )
    
                # Define CSS to enforce fixed media dimensions
                media_css = f"""
                    <style>
                        .media-container {{
                            width: {width};
                            height: {height};
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            overflow: hidden;
                            border-radius: 8px;
                            background-color: rgba(0, 0, 0, 0.1);
                        }}
                        .media-container img, .media-container video {{
                            max-width: 100%;
                            max-height: 100%;
                            object-fit: contain;
                        }}
                    </style>
                """
                st.markdown(media_css, unsafe_allow_html=True)
    
                # Identify file type
                ext = image_path.split('.')[-1].lower()
    
                # Media rendering inside a fixed-size div
                if ext in ['jpg', 'jpeg', 'png', 'gif']:
                    try:
                        st.image(image_path, use_container_width=False)
                    except Exception as e:
                        st.error(f"Error loading image: {str(e)}")
    
                elif ext in ['mp4', 'avi']:
                    try:
                        st.video(image_path)
                    except Exception as e:
                        st.error(f"Error loading video: {str(e)}")
    
                elif ext == 'html':
                    try:
                        with open(image_path, 'r') as file:
                            html_content = file.read()
                        components.html(html_content, width=int(width.replace("px", "")), height=int(height.replace("px", "")))
                    except FileNotFoundError:
                        st.error(f"Error: File '{image_path}' not found.")
                    except Exception as e:
                        st.error(f"Error loading HTML content: {str(e)}")
    
                else:
                    st.error(f"Unsupported media type: {ext}")
    
                st.markdown("</div>", unsafe_allow_html=True)
    
                # Display the title and description
                st.markdown(
                    f"""
                    <div style="position: relative; background-color: rgba(0, 0, 0, 0.4); padding: 15px; border-radius: 8px; color: white; width: 100%;">
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
    
                # Add spacing after media
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

    #
    # main public method to render the RecSys
    #
    def render(self):
        """Render method with Galleria callback integration."""
        st.subheader(self.section_header)
        st.markdown("---")
        st.markdown(f'<p style="color: gray;">{self.section_description}</p>', unsafe_allow_html=True)
        
        # Add the technical note with the ranker logic description
        st.markdown(f'### Recommender System Technical Note\n{self.RANKER_LOGIC}', unsafe_allow_html=True)
        
        # Add space to separate the section description from the controls
        st.markdown("")
        
        # Project Filter - Comes First
        prettified_titles = [prettify_title(title) for title in self.project_titles]
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

            
 




# Example usage
# Initialize RecSys with custom header and description
recsys = RecommendationSystem(
    #section_header="Customized Recommendations 🔍", 
    section_description="My research RecSys to make my portfolio discoverable. This RecSys versions uses exact pattern on item titles/descriptions, while more flexible, NLP type of matching is under development."
)

