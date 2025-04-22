import html

# Define available styles externally, this can be imported from a config module
STYLES_AVAILABLE = {
    "achieved_milestones": {
        "label": "Achieved Milestones", 
        "color": "#2E7D32",
        "pastel": "#A8D5BA",
        "icon": "https://img.icons8.com/?size=100&id=gbhGcQX6NZvT&format=png&color=000000", 
        "emoji": "✅",
        "default_text": "{n} milestones achieved"
    },
    "next_milestones": {
        "label": "Upcoming Milestones", 
        "color": "#C28F00",
        "pastel": "#F8E4B0",
        "icon": "https://img.icons8.com/?size=100&id=46910&format=png&color=000000", 
        "emoji": "🚧",
        "default_text": "{n} upcoming milestones"
    },
    "code_samples": {
        "label": "Code Samples", 
        "color": "#1565C0",
        "pastel": "#B0CDEF",
        "icon": "https://img.icons8.com/?size=100&id=ZSyCgjqn5i8Y&format=png&color=000000", 
        "emoji": "💾",
        "default_text": "{n} code samples"
    },
    "business_impact": {
        "label": "Business Impact", 
        "color": "#D32F2F",  
        "pastel": "#FFCDD2",  
        "icon": "https://img.icons8.com/?size=100&id=2dT788URbae8&format=png&color=000000", 
        "emoji": "🏆",
        "default_text": "{n} business impact milestones"
    },
    "technical_skills": {
        "label": "Technical Skills", 
        "color": "#6A1B9A",  
        "pastel": "#D8BFD8",  
        "icon": "https://img.icons8.com/?size=100&id=104252&format=png&color=000000", 
        "emoji": "🏅",
        "default_text": "{n} technical skills listed"
    },
    "breakthrough": {
    "label": "Breakthrough",
    "color": "#F9A825",        # Vivid Yellow
    "pastel": "#FFF8DC",       # Light Pastel Yellow (Cornsilk)
    "icon": "https://img.icons8.com/?size=100&id=20523&format=png&color=000000",
    "emoji": "💡",
    "default_text": "{n} major breakthroughs"
    },
    "performance": {
    "label": "Performance", 
    "color": "#0288D1",  # Deep Blue
    "pastel": "#B3E5FC",  # Light Pastel Blue
    "icon": "https://img.icons8.com/?size=100&id=XNkj51bATyA5&format=png&color=000000",  # Gauge Icon
    "emoji": "⚙️",  # Gear emoji
    "default_text": "{n} performance metrics"
    },
    "architecture": {
    "label": "Architecture", 
    "color": "#FF5722",  
    "pastel": "#FFCCBC",  
    "icon": "https://img.icons8.com/?size=100&id=gV1xxQ56XnrG&format=png&color=000000", 
    "emoji": "🏗️",
    "default_text": "{n} key architectural decisions made"
    },
    "models": {
    "label": "Models",
    "color": "#1976D2",  # Deep Blue
    "pastel": "#BBDEFB",  # Light Blue Pastel
    "icon": "https://img.icons8.com/?size=100&id=nlhCgr8avk8T&format=png&color=000000",  # Updated icon
    "emoji": "🌀",  # Cyclone emoji for abstraction
    "default_text": "{n} models used"
    }
}

def html_for_summary_list_tooltip(items, style_key="achieved_milestones", styles_available=STYLES_AVAILABLE):
    """
    Generates an HTML snippet to visually summarize a list with a styled tooltip.

    Parameters:
        - items (list): A list of strings to be displayed in the tooltip.
        - style_key (str): A key from styles_available defining how the block should look.
        - styles_available (dict): Dictionary of style configurations (externalized).

    Returns:
        - str: HTML snippet containing the figure with tooltip.
    """
    import html

    style = styles_available.get(style_key, {
        "label": "Items", 
        "color": "black", 
        "pastel": "#E0E0E0",
        "icon": "https://icons8.com/icon/gbhGcQX6NZvT/milestones", 
        "emoji": "📌",
        "default_text": "{n} items"
    })

    label = style["label"]
    color = style["color"]
    pastel_color = style["pastel"]
    icon_url = style["icon"]
    emoji = style["emoji"]
    default_text = style["default_text"]

    element_id = f"tooltip-{style_key}"

    if not items:
        return f"""
        <div id="{element_id}-container" style="width: 120px; height: 100px; display: inline-block; text-align: center; cursor: pointer;">
            <div style="color: gray; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                <img src="{icon_url}" alt="{label}" style="width: 30px; height: 30px; filter: grayscale(100%);" />
                <label style="font-size: 0.9em;">No {label.lower()}</label>
            </div>
        </div>
        """

    count = len(items)
    summary = default_text.format(n=count)

    visible_part = f"""
        <div style="width: 120px; height: 100px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: {color};">
            <img src="{icon_url}" alt="{label}" style="width: 30px; height: 30px;" />
            <label style="font-size: 0.9em; text-align: center;">{summary}</label>
        </div>
    """

    tooltip_content = "".join(
        f'<div style="color:{color};">{emoji} {html.escape(str(item))}</div>' for item in items
    )

    return f"""
    <div id="{element_id}-container" style="width: 120px; height: 100px; position: relative; display: inline-block; cursor: pointer; text-align: center;">
        <div id="{element_id}" style="border-bottom: 1px dashed gray;" class="hover-trigger">
            {visible_part}
        </div>
        <div class="tooltip">
            <strong>{label}:</strong>
            {tooltip_content}
        </div>
    </div>
    <style>
        #{element_id}-container:hover {{
            background-color: {pastel_color};
            transition: background-color 0.3s ease-in-out;
            border-radius: 5px;
        }}

        .tooltip {{
            visibility: hidden;
            opacity: 0;
            transform: translateY(5px) scale(0.95);
            transition: 
                opacity 0.3s ease-in-out, 
                visibility 0.3s ease-in-out, 
                transform 0.3s ease-in-out;
            background-color: rgba(240, 240, 240, 0.7);
            backdrop-filter: blur(1px);
            color: black;
            text-align: left;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            position: absolute;
            left: 50%;
            top: 100%;
            transform: translateX(-50%) translateY(5px);
            min-width: 300px;
            max-width: 400px;
            z-index: 1;
            border: 1px solid rgba(200, 200, 200, 0.5);
            transform-origin: top center;
        }}

        .hover-trigger:hover ~ .tooltip {{
            visibility: visible;
            opacity: 1;
            transform: translateX(-50%) translateY(0px) scale(1.1);
        }}
    </style>
    """


