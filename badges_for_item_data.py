"""
title: Badges for Items
description: The badges system distributes visual cues based on emojisto the front end representations of the recommmended items.
             The badges are provided according to rules on item metadata. They help to convey more rich information about items in
             a subtle manner, thus enhancing further experience.
"""

import re
import os
import html
from html import escape
from front_end_utils import prettify_title

# File-type to icon mapping
FILE_TYPE_ICONS = {
    ".r": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/R_logo.svg/50px-R_logo.svg.png",
    ".py": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/50px-Python-logo-notext.svg.png",
    ".ipynb": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/50px-Jupyter_logo.svg.png",
    ".csv": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/CSV_Icon.svg/50px-CSV_Icon.svg.png",
}

# Google Colab icon
COLAB_ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Google_Colaboratory_SVG_Logo.svg/50px-Google_Colaboratory_SVG_Logo.svg.png"

import os
import re
from datetime import datetime, timezone

def apply_badges_to_item_title(metadata, badge_rules=None, recent_fix_hours=72, recent_creation_hours=72):
    """
    Applies multiple badges (emoji + file icons) to the title based on metadata.

    Parameters:
    - metadata (dict): Dictionary containing item metadata.
    - badge_rules (list of tuples, optional): Each tuple contains:
        (regex (str), emoji (str), keys (list of str))
    - recent_fix_hours (int, optional): Hours threshold for considering an item recently updated.
    - recent_creation_hours (int, optional): Hours threshold for considering an item recently created.

    Returns:
    - str: Title string with appropriate badges (including HTML img for file icons).
    """
    # **Determine "recently updated" status (🔧)**
    recently_fixed = False
    last_updated_str = metadata.get("last_updated")

    if last_updated_str:
        try:
            last_updated_dt = datetime.fromisoformat(last_updated_str.replace("Z", "+00:00"))
            now_dt = datetime.now(timezone.utc)
            hours_elapsed = (now_dt - last_updated_dt).total_seconds() / 3600
            recently_fixed = hours_elapsed < recent_fix_hours
        except ValueError:
            pass  # Ignore invalid date formats

    # **Determine "recently created" status (🍞)**
    freshly_baked = False
    creation_date_str = metadata.get("creation_date")

    if creation_date_str:
        try:
            creation_date_dt = datetime.fromisoformat(creation_date_str.replace("Z", "+00:00"))
            now_dt = datetime.now(timezone.utc)
            hours_elapsed = (now_dt - creation_date_dt).total_seconds() / 3600
            freshly_baked = hours_elapsed < recent_creation_hours
        except ValueError:
            pass  # Ignore invalid date formats

    # **Define default badge rules (Always Exists)**
    if badge_rules is None:
        badge_rules = [
            (".*", "⭐", ["galleria", "highlighted_content", "image_path"]),  # Outstanding content
            (".*", "🔧", ["recently_fixed"]),  # Recently updated content
            (".*", "🍞", ["freshly_baked"]),  # Recently created content
        ]

    title = prettify_title(metadata.get('title', 'Untitled'))  # Ensure prettify_title exists
    badges = []

    # **Process emoji-based badges**
    for regex, emoji, keys in badge_rules:
        if any(
            re.search(regex, str(metadata.get(key, ""))) or
            (key == "recently_fixed" and recently_fixed) or
            (key == "freshly_baked" and freshly_baked)
            for key in keys
        ):
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

    # **Generate the final decorated title**
    return f"{' '.join(badges)} {title}" if badges else title


