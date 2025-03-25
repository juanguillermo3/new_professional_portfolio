"""
title: Media Carousel
description: Implements `html_for_media_carousel` to generate an HTML-based media carousel from media files. 
             It returns raw HTML, enhancing composability with other components. 
             The carousel works in tandem with `flexible_file_discovery`, a service that discovers valid media files 
             that can be processed by the media carousel.
"""

#
# 0.
#
import streamlit as st
import glob
import re
import os
import base64
import hashlib
import time

# Global configuration for valid media files
VALID_MEDIA_FILES = {".jpg", ".jpeg", ".png", ".gif", ".mp4", ".webm", ".html"}

#
# 1.
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
# 2.
#

#
# (0.1)
#
def image_to_base64(image_path):
    """Converts an image file to a base64 string."""
    if not os.path.exists(image_path):
        return None
    
    with open(image_path, "rb") as image_file:
        return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
#
# (0.2)
#
def html_to_base64(file_path):
    """Reads a local HTML file and converts it to a base64-encoded data URL."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            encoded_html = base64.b64encode(html_content.encode()).decode()
            return f"data:text/html;base64,{encoded_html}"
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
#
# (1)
#
import os
import hashlib
import datetime

def html_for_media_carousel(media_items, container_id="media-container", duration=5):
    """
    Generates an HTML snippet for a media carousel that supports images and HTML files.

    :param media_items: List of dictionaries with media properties (src, alt).
    :param container_id: Unique ID for the media container.
    :param duration: Duration (in seconds) for each media transition.
    :return: HTML string for the media display.
    """
    if not media_items:
        return "<p>No media available</p>"

    media_items = media_items[:10]  # Limit to 10 items for safety
    unique_id = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:6]
    
    media_html = []
    for i, item in enumerate(media_items):
        media_path = item["src"]
        ext = os.path.splitext(media_path)[1].lower()

        if os.path.isfile(media_path):
            if ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]:
                base64_img = image_to_base64(media_path)  # Function you already have
                media_html.append(
                    f'<img src="{base64_img}" alt="{item.get("alt", f"Image {i+1}")}" '
                    f'class="carousel-item-{unique_id} item-{unique_id}-{i}">'
                )
            elif ext == ".html":
                base64_html = html_to_base64(media_path)
                if base64_html:
                    media_html.append(
                        f'<iframe src="{base64_html}" class="carousel-item-{unique_id} item-{unique_id}-{i}" '
                        f'frameborder="0" width="100%" height="auto"></iframe>'
                    )

    total_duration = len(media_items) * duration
    keyframes = "".join([
        f"""
        @keyframes fadeAnimation-{unique_id}-{i} {{
            0%, {(i * 100) // len(media_items)}% {{ opacity: 0; transform: scale(1); }}
            {(i * 100) // len(media_items) + 10}% {{ opacity: 1; transform: scale(1.02); }}
            {((i + 1) * 100) // len(media_items) - 10}% {{ opacity: 1; transform: scale(1.02); }}
            {((i + 1) * 100) // len(media_items)}%, 100% {{ opacity: 0; transform: scale(1); }}
        }}
        """
        for i in range(len(media_items))
    ])

    styles = "".join([
        f"""
        .item-{unique_id}-{i} {{
            animation: fadeAnimation-{unique_id}-{i} {total_duration}s infinite;
            transition: opacity 1s ease-in-out, transform 1s ease-in-out;
        }}
        """
        for i in range(len(media_items))
    ])

    return f"""
    <div id="{container_id}" class="media-container">
        {"".join(media_html)}
    </div>

    <style>
        .media-container {{
            position: relative;
            width: 800px;
            min-height: 600px;
            height: auto;
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            background: rgba(255, 255, 255, .5);
            backdrop-filter: blur(4px);
            border: 2px solid rgba(255, 255, 255, 0.9);
            text-align: center;
            padding: 10px;
        }}

        .media-container img, .media-container iframe {{
            width: 100%;
            height: 600px;
            object-fit: contain;
            border-radius: 10px;
            position: absolute;
            top: 0;
            left: 0;
            opacity: 0;
        }}

        {keyframes}
        {styles}
    </style>
    """




# Example usage:
dummy_media_list = [
    {"src": "https://media.istockphoto.com/id/1226328537/vector/image-place-holder-with-a-gray-camera-icon.jpg", "alt": "iStock Placeholder"},
    {"src": "https://archive.org/download/placeholder-image/placeholder-image.jpg", "alt": "Placeholder Image"}
]


