import re
import os
import html

# File-type to icon mapping
FILE_TYPE_ICONS = {
    ".r": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/R_logo.svg/50px-R_logo.svg.png",
    ".py": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/50px-Python-logo-notext.svg.png",
    ".ipynb": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/50px-Jupyter_logo.svg.png",
    ".csv": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/CSV_Icon.svg/50px-CSV_Icon.svg.png",
}

# Google Colab icon
COLAB_ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Google_Colab_Logo.svg/50px-Google_Colab_Logo.svg.png"

def apply_badges_to_item_title(metadata, badge_rules=None):
    """
    Applies multiple badges (emoji + file icons) to the title based on metadata.

    Parameters:
    - metadata (dict): Dictionary containing item metadata.
    - badge_rules (list of tuples, optional): Each tuple contains:
        (regex (str), emoji (str), keys (list of str))

    Returns:
    - str: Title string with appropriate badges (including HTML img for file icons).
    """
    if badge_rules is None:
        badge_rules = [
            (".*", "⭐", ["galleria", "highlighted_content", "image_path"]),  # Outstanding content
        ]

    title = prettify_title(metadata.get('title', 'Untitled'))
    badges = []

    # Process emoji-based badges
    for regex, emoji, keys in badge_rules:
        if any(key in metadata and re.search(regex, str(metadata[key])) for key in keys):
            badges.append(emoji)

    # **Auto-detect file type from "file_path"**
    file_type = ""
    file_path = metadata.get("file_path", "").strip().lower()
    if file_path:
        file_type = os.path.splitext(file_path)[1]  # Extract file extension (includes the dot)

    # **Process file-type badges**
    if file_type in FILE_TYPE_ICONS:
        icon_url = FILE_TYPE_ICONS[file_type]
        file_icon = f'<img src="{icon_url}" style="width: 16px; height: 16px; vertical-align: middle;">'
        badges.append(file_icon)

    # **Check for Colab-specific case**
    if "colab_url" in metadata:
        colab_icon = f'<img src="{COLAB_ICON_URL}" style="width: 16px; height: 16px; vertical-align: middle;">'
        badges.append(colab_icon)

    # Generate the final decorated title
    return f"{' '.join(badges)} {title}" if badges else title
