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
# (1)
#
def image_to_base64(image_path):
    """Converts an image file to a base64 string."""
    if not os.path.exists(image_path):
        return None
    
    with open(image_path, "rb") as image_file:
        return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
#
# (2)
#
def html_for_media_carousel(media_items, container_id="media-container"):
    """
    Generates an HTML snippet for a styled media carousel with smooth transitions and dynamic height.

    :param media_items: List of dictionaries with media properties (src, alt).
    :param container_id: Unique ID for the media container.
    :return: HTML string for the media display.
    """
    if not media_items:
        return "<p>No media available</p>"

    # Limit to 10 media items for safety
    media_items = media_items[:10]

    # Convert local images to Base64 if needed
    for item in media_items:
        if os.path.isfile(item['src']):
            item['src'] = image_to_base64(item['src']) or ""

    # Generate image elements with unique animation delays
    images_html = "".join([
        f'<img src="{item["src"]}" alt="{item.get("alt", f"Image {i+1}")}" class="carousel-item" style="animation-delay: {i * 4}s;">'
        for i, item in enumerate(media_items)
    ])

    return f"""
    <div id="{container_id}" class="media-container">
        {images_html}
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

        .media-container img {{
            width: 100%;
            height: auto;
            object-fit: contain;
            border-radius: 10px;
            position: absolute;
            top: 0;
            left: 0;
            opacity: 0;
            animation: fadeAnimation {len(media_items) * 3}s infinite;
        }}

        /* Keyframe animation for smooth fade */
        @keyframes fadeAnimation {{
            0%   {{ opacity: 0; }}
            10%  {{ opacity: 1; }}
            90%  {{ opacity: 1; }} /* Hold full opacity */
            100% {{ opacity: 0; }} /* Fade out only at the end */
        }}
    </style>
    """

def html_for_media_carousel(media_items, container_id="media-container", duration=3):
    """
    Generates an HTML snippet for a styled media carousel with smooth transitions and dynamic height.

    :param media_items: List of dictionaries with media properties (src, alt).
    :param container_id: Unique ID for the media container.
    :param duration: Duration (in seconds) for each media transition.
    :return: HTML string for the media display.
    """
    if not media_items:
        return "<p>No media available</p>"

    # Limit to 10 media items for safety
    media_items = media_items[:10]

    # Convert local images to Base64 if needed
    for item in media_items:
        if os.path.isfile(item['src']):
            item['src'] = image_to_base64(item['src']) or ""

    total_duration = len(media_items) * duration
    images_html = "".join([
        f'<img src="{item["src"]}" alt="{item.get("alt", f"Image {i+1}")}" class="carousel-item item-{i}">' 
        for i, item in enumerate(media_items)
    ])

    keyframes = "".join([
        f"""
        @keyframes fadeAnimation-{i} {{
            0%, {(i * 100) // len(media_items)}% {{ opacity: 0; }}
            {(i * 100) // len(media_items) + 10}% {{ opacity: 1; }}
            {((i + 1) * 100) // len(media_items) - 10}% {{ opacity: 1; }}
            {((i + 1) * 100) // len(media_items)}%, 100% {{ opacity: 0; }}
        }}
        """
        for i in range(len(media_items))
    ])

    styles = "".join([
        f"""
        .item-{i} {{
            animation: fadeAnimation-{i} {total_duration}s infinite;
        }}
        """
        for i in range(len(media_items))
    ])

    return f"""
    <div id="{container_id}" class="media-container">
        {images_html}
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

        .media-container img {{
            width: 100%;
            height: auto;
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

def html_for_media_carousel(media_items, container_id="media-container", duration=3):
    """
    Generates an HTML snippet for a styled media carousel that supports:
      - Local images (converted to Base64)
      - Local HTML files (embedded in <iframe>)
    
    :param media_items: List of dictionaries with media properties (src, alt).
    :param container_id: Unique ID for the media container.
    :param duration: Duration (in seconds) for each media transition.
    :return: HTML string for the media display.
    """
    if not media_items:
        return "<p>No media available</p>"

    valid_media = []
    
    # Process only local files (images & HTML)
    for item in media_items:
        src = item.get("src", "")
        if os.path.isfile(src):  
            if src.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")):
                base64_src = image_to_base64(src)
                if base64_src:
                    valid_media.append({
                        "type": "image",
                        "content": f"data:image/png;base64,{base64_src}",
                        "alt": item.get("alt", "Local Image")
                    })
            elif src.lower().endswith(".html"):  
                valid_media.append({
                    "type": "html",
                    "content": src,  # Use file path in <iframe> (must be local)
                    "alt": item.get("alt", "Local HTML Content")
                })

    if not valid_media:
        return "<p>No valid local media available</p>"

    # Limit to 10 media items for safety
    valid_media = valid_media[:10]

    total_duration = len(valid_media) * duration
    media_html = ""

    for i, item in enumerate(valid_media):
        if item["type"] == "image":
            media_html += f'<img src="{item["content"]}" alt="{item["alt"]}" class="carousel-item item-{i}">'
        elif item["type"] == "html":
            media_html += f'<iframe src="{item["content"]}" class="carousel-item item-{i}" sandbox="allow-scripts allow-same-origin"></iframe>'

    keyframes = "".join([
        f"""
        @keyframes fadeAnimation-{i} {{
            0%, {(i * 100) // len(valid_media)}% {{ opacity: 0; }}
            {(i * 100) // len(valid_media) + 10}% {{ opacity: 1; }}
            {((i + 1) * 100) // len(valid_media) - 10}% {{ opacity: 1; }}
            {((i + 1) * 100) // len(valid_media)}%, 100% {{ opacity: 0; }}
        }}
        """
        for i in range(len(valid_media))
    ])

    styles = "".join([
        f"""
        .item-{i} {{
            animation: fadeAnimation-{i} {total_duration}s infinite;
        }}
        """
        for i in range(len(valid_media))
    ])

    return f"""
    <div id="{container_id}" class="media-container">
        {media_html}
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
            height: 100%;
            object-fit: contain;
            border-radius: 10px;
            position: absolute;
            top: 0;
            left: 0;
            opacity: 0;
            border: none;
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


