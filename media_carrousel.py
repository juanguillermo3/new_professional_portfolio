"""
title: Media Carousel
description: Implements `html_for_media_carousel` to generate an HTML-based media carousel from media files. 
             It returns raw HTML, enhancing composability with other components. 
             The carousel works in tandem with `flexible_file_discovery`, a service that discovers valid media files 
             that can be processed by the media carousel.
"""

import streamlit as st
import glob
import re
import os

# Global configuration for valid media files
VALID_MEDIA_FILES = {".jpg", ".jpeg", ".png", ".gif", ".mp4", ".webm"}

#
# (1)
#
def flexible_file_discovery(file_pattern, valid_files=None, search_dir="assets"):
    """
    Discover files matching a flexible pattern using both glob and regex filtering.

    :param file_pattern: The pattern to match files (supports both glob and regex).
    :param valid_files: Set of valid file extensions (defaults to global VALID_MEDIA_FILES).
    :param search_dir: Directory to search in.
    :return: List of discovered file paths.
    """
    valid_files = valid_files or VALID_MEDIA_FILES  # Use global config if not provided

    # Adjust search_dir if file_pattern already includes a directory
    if os.path.sep in file_pattern:
        search_dir = os.path.dirname(file_pattern)
        file_pattern = os.path.basename(file_pattern)

    # Step 1: Glob-based discovery
    glob_pattern = os.path.join(search_dir, "**", file_pattern)
    glob_matches = glob.glob(glob_pattern, recursive=True)

    # Step 2: Convert file pattern to regex if it doesn’t contain glob characters
    regex_pattern = None
    if not any(char in file_pattern for char in "*?[]"):
        regex_pattern = re.compile(file_pattern)

    # Step 3: Filter results
    filtered_files = []
    for file_path in glob_matches:
        file_name = os.path.basename(file_path)

        # Validate against regex pattern
        if regex_pattern and not regex_pattern.match(file_name):
            continue

        # Validate against valid file types
        if valid_files and not any(file_name.lower().endswith(ext) for ext in valid_files):
            continue

        filtered_files.append(file_path)

    return filtered_files
#
# (2)
#
def html_for_media_carousel(media_items, carousel_id="media-carousel"):
    """
    Generates a simple HTML and CSS-based media carousel with navigation.

    :param media_items: List of dictionaries with media properties (src, alt).
    :param carousel_id: Unique ID for the carousel container.
    :return: HTML string for the carousel.
    """
    num_items = len(media_items)
    if num_items == 0:
        return "<p>No media available</p>"

    # Generate radio inputs and carousel items
    slides_html = "".join([
        f'<input type="radio" id="{carousel_id}-slide{i}" name="{carousel_id}-radio" '
        f'{"checked" if i == 0 else ""}><div class="carousel-item">'
        f'<img src="{item["src"]}" alt="{item.get("alt", f"Image {i+1}")}"></div>'
        for i, item in enumerate(media_items)
    ])

    # Generate navigation buttons
    nav_html = "".join([
        f'<label for="{carousel_id}-slide{i}" class="nav-btn"></label>'
        for i in range(num_items)
    ])

    return f"""
    <div class="carousel-container">
        {slides_html}
        <div class="carousel-nav">{nav_html}</div>
    </div>

    <style>
        .carousel-container {{
            position: relative;
            width: 60%;
            max-width: 600px;
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            text-align: center;
        }}

        .carousel-item {{
            display: none;
        }}

        .carousel-item img {{
            width: 100%;
            height: auto;
            border-radius: 10px;
        }}

        input[name="{carousel_id}-radio"] {{
            display: none;
        }}

        /* Show the selected slide */
        {''.join([
            f'input[id="{carousel_id}-slide{i}"]:checked ~ .carousel-item:nth-of-type({i+1}) {{ display: block; }}'
            for i in range(num_items)
        ])}

        /* Navigation buttons */
        .carousel-nav {{
            margin-top: 10px;
        }}

        .nav-btn {{
            display: inline-block;
            width: 12px;
            height: 12px;
            margin: 0 5px;
            background: gray;
            border-radius: 50%;
            cursor: pointer;
        }}

        .nav-btn:hover {{
            background: black;
        }}

        /* Selected indicator */
        {''.join([
            f'input[id="{carousel_id}-slide{i}"]:checked ~ .carousel-nav label:nth-of-type({i+1}) {{ background: black; }}'
            for i in range(num_items)
        ])}
    </style>
    """


# Example usage:
dummy_media_list = [
    {"src": "https://media.istockphoto.com/id/1226328537/vector/image-place-holder-with-a-gray-camera-icon.jpg", "alt": "iStock Placeholder"},
    {"src": "https://archive.org/download/placeholder-image/placeholder-image.jpg", "alt": "Placeholder Image"}
]

#st.markdown(html_for_media_carousel(dummy_media_list), unsafe_allow_html=True)

#carousel_html = html_for_media_carousel(media_list)
