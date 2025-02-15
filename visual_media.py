import os
import glob
import streamlit as st
import streamlit.components.v1 as components


def render_item_visual_content(title, description, media_path, width="700px", height="400px"):
    """
    Render visual content based on metadata with minimal spacing. Supports images, videos, and HTML.
    Allows navigation between multiple media files matched by a glob pattern using numbered buttons.
    
    This function:
    1. Resolves a file path pattern (supports glob patterns) to a list of media files.
    2. Displays a single media item at a time, such as an image, video, or HTML.
    3. Provides numbered buttons for navigation to jump directly to any media file.
    4. Uses Streamlit session state to track the current media index and enable navigation.
    5. Renders text metadata (title and description) with a styled minimal layout.
    """
    
    # Resolve file paths
    file_list = glob.glob(media_path) if '*' in media_path or '?' in media_path else [media_path]
    file_list = sorted(file_list)  # Sort for consistent order
    
    if not file_list:
        st.error(f"No files found for pattern: {media_path}")
        return

    # Session state for navigation
    if "media_index" not in st.session_state:
        st.session_state.media_index = 0

    total_files = len(file_list)
    current_file = file_list[st.session_state.media_index]
    file_ext = os.path.splitext(current_file)[-1].lower()

    # Define base styles
    st.markdown(
        f"""
        <style>
            .media-container {{
                width: {width};
                height: {height};
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                background: rgba(0, 0, 0, 0.05);
                border-radius: 10px;
                margin-bottom: 5px;
            }}
            .text-container {{
                background: rgba(0, 0, 0, 0.3);
                padding: 6px;
                border-radius: 8px;
                color: white;
                width: 100%;
                text-align: center;
                margin-top: 5px;
            }}
            .title-text {{
                font-size: 18px;
                font-weight: 600;
                color: #fff;
                display: block;
            }}
            .description-text {{
                font-size: 14px;
                font-weight: 400;
                color: #ddd;
                display: block;
                margin-top: 3px;
            }}
            .nav-buttons {{
                display: flex;
                justify-content: center;
                margin-top: 10px;
                gap: 5px;
            }}
            .nav-button {{
                background-color: navy;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 5px;
                cursor: pointer;
            }}
            .nav-button:hover {{
                background-color: darkblue;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Render media
    with st.container():
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            st.image(current_file, use_container_width=True)  # ✅ Fixed: Replaced deprecated use_column_width

        elif file_ext in ['.mp4', '.avi', '.mov', '.webm']:
            st.video(current_file)

        elif file_ext == '.html':
            try:
                with open(current_file, 'r') as file:
                    html_content = file.read()
                components.html(html_content, width=int(width.replace("px", "")), height=int(height.replace("px", "")))
            except Exception as e:
                st.error(f"Error loading HTML content: {str(e)}")

        else:
            st.error(f"Unsupported media type: {file_ext}")

    # Render navigation buttons as a grid of numbered buttons
    if total_files > 1:
        nav_buttons = st.columns(total_files)
        for idx, col in enumerate(nav_buttons):
            with col:
                # Apply secondary button style
                if st.button(f"{idx + 1}", key=f"nav_button_{idx}", help=f"Go to media {idx + 1}", use_container_width=True):
                    st.session_state.media_index = idx
                    st.experimental_rerun()
        
    # Render the text section
    st.markdown(
        f"""
        <div class="text-container">
            <span class="title-text">{title}</span>
            <span class="description-text">{description}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


class VisualContentGallery:
    def __init__(self, title, description, media_path, width="700px", height="400px"):
        self.title = title
        self.description = description
        self.width = width
        self.height = height
        self.file_list = self._find_media_files(media_path)
        self.current_index = 0

    def _find_media_files(self, media_path):
        file_list = glob.glob(media_path) if '*' in media_path or '?' in media_path else [media_path]
        return sorted(file_list)

    def parse_media(self, file_path, width_offset=0, height_offset=50):
        file_ext = os.path.splitext(file_path)[-1].lower()
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            st.image(file_path, use_container_width=True)
        elif file_ext in ['.mp4', '.avi', '.mov', '.webm']:
            st.video(file_path)
        elif file_ext == '.html':
            try:
                with open(file_path, 'r') as file:
                    html_content = file.read()
                components.html(
                    html_content, 
                    width=int(self.width.replace("px", "")) + width_offset, 
                    height=int(self.height.replace("px", "")) + height_offset
                )
            except Exception as e:
                st.error(f"Error loading HTML content: {str(e)}")
        else:
            st.error(f"Unsupported media type: {file_ext}")

    def render(self):

        # Apply styles globally to the app
        st.markdown(
            f"""
            <style>
                .media-container {{
                    width: {self.width};
                    height: {self.height};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                    background: rgba(0, 0, 0, 0.05);
                    border-radius: 10px;
                    margin-bottom: 5px;
                }}
                .text-container {{
                    background: rgba(0, 0, 0, 0.3);
                    padding: 6px;
                    border-radius: 8px;
                    color: white;
                    width: 100%;
                    text-align: center;
                    margin-top: 5px;
                }}
                .title-text {{
                    font-size: 18px;
                    font-weight: 600;
                    color: #fff;
                    display: block;
                }}
                .description-text {{
                    font-size: 14px;
                    font-weight: 400;
                    color: #ddd;
                    display: block;
                    margin-top: 3px;
                }}
                .nav-buttons {{
                    display: flex;
                    justify-content: center;
                    margin-top: 10px;
                    gap: 5px;
                }}
                .nav-button {{
                    background-color: navy;
                    color: white;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 5px;
                    cursor: pointer;
                }}
                .nav-button:hover {{
                    background-color: darkblue;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
        
        if not self.file_list:
            st.error("No media files found.")
            return

        current_file = self.file_list[self.current_index]
        self.parse_media(current_file)

        if len(self.file_list) > 1:
            nav_buttons = st.columns(len(self.file_list))
            for idx, col in enumerate(nav_buttons):
                with col:
                    if st.button(f"{idx + 1}", key=f"nav_button_{idx}", help=f"Go to media {idx + 1}", type="secondary", use_container_width=True):
                        self.current_index = idx
                        #st.experimental_rerun()

        st.markdown(
            f"""
            <div class="text-container">
                <span class="title-text">{self.title}</span>
                <span class="description-text">{self.description}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


class GalleryCollection:
    """
    A collection that manages multiple instances of VisualContentGallery.
    It provides a centralized access point for retrieving gallery instances by a unique key.
    Instances are cached to ensure that duplicate galleries are not created for the same key.

    Attributes:
        cache (dict): A dictionary that stores cached VisualContentGallery instances by key.

    Methods:
        get(key, galleria_params): Retrieves an existing VisualContentGallery instance from the cache 
                                   or creates a new one if it doesn't exist. Validates the provided parameters.
    """

    def __init__(self):
        """
        Initializes the GalleryCollection with an empty cache.
        """
        self.cache = {}

    def _validate_galleria_params(self, galleria_params):
        """
        Validates the required parameters for instantiating a VisualContentGallery.
        
        Raises:
            ValueError: If any of the required keys ('title', 'description', 'media_path') are missing.
        """
        required_keys = ['title', 'description', 'media_path']
        for key in required_keys:
            if key not in galleria_params:
                raise ValueError(f"Missing required parameter: '{key}' in galleria_params")

    def get(self, key, galleria_params):
        """
        Retrieves a VisualContentGallery instance by key. If the instance does not exist, it is created and cached.
        
        Args:
            key (str): The unique identifier for the gallery.
            galleria_params (dict): A dictionary containing parameters like 'title', 'description', and 'media_path'.
        
        Returns:
            VisualContentGallery: A cached or newly created VisualContentGallery instance.

        Raises:
            ValueError: If any required parameters are missing from galleria_params.
        """
        self._validate_galleria_params(galleria_params)
        
        if key not in self.cache:
            self.cache[key] = VisualContentGallery(
                title=galleria_params['title'],
                description=galleria_params['description'],
                media_path=galleria_params['media_path'],
                width=galleria_params.get('width', '700px'),
                height=galleria_params.get('height', '400px')
            )
        return self.cache[key]

test_gallery = VisualContentGallery(
    title="Geometric Modelling for Nutrition Data",
    description="Applies Geometric Modelling based on dimensionality reduction to analize nutritional preferences of the monkey species.",
    media_path="assets/gm_per_*.png",
    width="700px",
    height="400px"
)

        
