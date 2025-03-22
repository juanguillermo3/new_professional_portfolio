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
            width: 600px; /* Fixed width */
            height: auto; /* Auto height based on image aspect ratio */
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


import base64
import os

def image_to_base64(image_path):
    """Converts an image file to a base64 string."""
    if not os.path.exists(image_path):
        return None
    
    with open(image_path, "rb") as image_file:
        return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"


def html_for_media_carousel(media_items, carousel_id="media-carousel"):
    """
    Generates a simple HTML and CSS-based media carousel with Base64 embedded images.

    :param media_items: List of dictionaries with media properties (src, alt).
    :param carousel_id: Unique ID for the carousel container.
    :return: HTML string for the carousel.
    """
    num_items = len(media_items)
    if num_items == 0:
        return "<p>No media available</p>"
    
    # Convert local images to base64
    for item in media_items:
        if os.path.isfile(item['src']):  # If it's a local file
            item['src'] = image_to_base64(item['src']) or ""
    
    # Generate radio inputs and carousel items
    slides_html = "".join([
        f'<input type="radio" id="{carousel_id}-slide{i}" name="{carousel_id}-radio" '
        f'{'checked' if i == 0 else ''}><div class="carousel-item">'
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
            width: 600px; /* Fixed width */
            height: auto; /* Auto height based on image aspect ratio */
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            text-align: center;
            background: rgba(255, 255, 255, .25); /* Fully transparent */
            backdrop-filter: blur(4px); /* Frosted glass effect */
            border: 2px solid rgba(255, 255, 255, 0.9); /* Subtle white border */
            box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.1); /* Soft glowing shadow */
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
            width: 24px;
            height: 24px;
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



def html_for_media_carousel(media_items, carousel_id="media-carousel"):
    """
    Generates an HTML/CSS-based media carousel with Base64 embedded images.

    :param media_items: List of dictionaries with media properties (src, alt).
    :param carousel_id: Unique ID for the carousel container.
    :return: HTML string for the carousel.
    """
    num_items = len(media_items)
    if num_items == 0:
        return "<p>No media available</p>"
    
    # Convert local images to Base64
    for item in media_items:
        if os.path.isfile(item['src']):  # If it's a local file
            item['src'] = image_to_base64(item['src']) or ""
    
    # Generate carousel items
    slides_html = "".join([
        f'<div class="carousel-item"><img src="{item["src"]}" alt="{item.get("alt", f"Image {i+1}")}"></div>'
        for i, item in enumerate(media_items)
    ])

    # Generate fade animations
    fade_animation = "".join([
        f'.carousel-item:nth-child({i+1}) {{ animation: fadeCarousel {num_items * 5}s infinite; animation-delay: {i * 5}s; }}'
        for i in range(num_items)
    ])

    return f"""
    <div class="carousel-container">
        <div class="carousel-slides">
            {slides_html}
        </div>
    </div>

    <style>
        .carousel-container {{
            position: relative;
            width: 600px; /* Fixed width */
            height: auto;
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            background: rgba(255, 255, 255, .25);
            backdrop-filter: blur(4px);
            border: 2px solid rgba(255, 255, 255, 0.9);
            box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.1);
        }}

        .carousel-slides {{
            display: flex;
            position: relative;
            width: 100%;
        }}

        .carousel-item {{
            position: absolute;
            width: 100%;
            opacity: 0;
            transition: opacity 1s ease-in-out;
        }}

        .carousel-item img {{
            width: 100%;
            height: auto;
            border-radius: 10px;
        }}

        .carousel-item:first-child {{ opacity: 1; }} /* Show first image by default */

        /* Keyframes for fade effect */
        @keyframes fadeCarousel {{
            0% {{ opacity: 0; }}
            10% {{ opacity: 1; }}
            30% {{ opacity: 1; }}
            40% {{ opacity: 0; }}
            100% {{ opacity: 0; }}
        }}

        /* Apply animation */
        {fade_animation}

        /* Pause animation on hover */
        .carousel-container:hover .carousel-item {{
            animation-play-state: paused;
        }}

    </style>
    """

