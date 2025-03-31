import hashlib
import re

#
# (0) helper function to chunk text into brief main statement, and details
#
def _chunk_texts(detailed_text: str, min_tokens: int = 10) -> tuple[str, str]:
    """Splits a paragraph into a brief (main statement) and details (remaining text).
    
    Ensures that the brief contains at least `min_tokens` words before considering a period 
    as a valid splitting point.
    """
    sentences = re.split(r"(?<=\.)\s+", detailed_text.strip())  # Split on periods with space
    brief, details = "", ""

    token_count = 0
    for i, sentence in enumerate(sentences):
        tokens = sentence.split()
        token_count += len(tokens)

        if token_count >= min_tokens or i == len(sentences) - 1:  
            brief = " ".join(sentences[:i+1])  # Grab enough content
            details = " ".join(sentences[i+1:])  # The rest goes here
            break

    return brief.strip(), details.strip()
#
# (1) render html for the text component and interactable behaviour
#
def expandable_text_html(detailed_text: str) -> tuple[str, str]:
    """
    Generates an HTML snippet with a hover-reveal effect for long text descriptions.
    
    Returns:
        offering_html (str): The generated HTML structure.
        style_block (str): The required CSS styles.
    """
    brief, details = _chunk_texts(detailed_text)
    
    # Generate a unique element ID using a hash
    element_id = "hover-" + hashlib.md5(detailed_text.encode()).hexdigest()[:8]

    # Append a visually distinct ellipsis
    brief += ' <strong class="ellipsis">...</strong>'

    text_container = (
        f'<div id="{element_id}" class="ancillary-container">'
        f'<p style="text-align: justify; margin: 0;">{brief}'
    )

    style_block = (
        f"#{element_id} {{ cursor: pointer; }}\n"  # Cursor change
        f".ellipsis {{ color: #555; font-weight: bold; font-size: 1.1em; }}\n"  # Noticeable ellipsis
    )

    if details:
        text_container += f' <span class="{element_id}-hidden">{details}</span>'
        style_block += (
            f".{element_id}-hidden {{"
            f" display: inline-block; opacity: 0; max-width: 0px; max-height: 0px; overflow: hidden;"
            f" transition: opacity 0.3s ease-in-out 0.2s, max-width 0.4s ease-out, max-height 0.4s ease-out; }}\n"
            f"#{element_id}:hover .{element_id}-hidden {{"
            f" opacity: 1; max-width: 100%; max-height: 400px; }}\n"
        )

    return text_container, style_block


import hashlib
import re

#
# (0) helper function to chunk text into brief main statement, and details
#
def _chunk_texts(detailed_text: str, min_tokens: int = 10) -> tuple[str, str]:
    """Splits a paragraph into a brief (main statement) and details (remaining text).
    
    Ensures that the brief contains at least `min_tokens` words before considering a period 
    as a valid splitting point.
    """
    sentences = re.split(r"(?<=\.)\s+", detailed_text.strip())  # Split on periods with space
    brief, details = "", ""

    token_count = 0
    for i, sentence in enumerate(sentences):
        tokens = sentence.split()
        token_count += len(tokens)

        if token_count >= min_tokens or i == len(sentences) - 1:  
            brief = " ".join(sentences[:i+1])  # Grab enough content
            details = " ".join(sentences[i+1:])  # The rest goes here
            break

    return brief.strip(), details.strip()

#
# (1) render html for the text component with emoji hint and interactable behavior
#
def expandable_text_html(detailed_text: str) -> tuple[str, str]:
    """
    Generates an HTML snippet with a hover-reveal effect for long text descriptions, 
    including an intermittent emoji to hint interaction.
    
    Returns:
        offering_html (str): The generated HTML structure.
        style_block (str): The required CSS styles.
    """
    brief, details = _chunk_texts(detailed_text)
    
    # Generate a unique element ID using a hash
    element_id = "hover-" + hashlib.md5(detailed_text.encode()).hexdigest()[:8]

    # Append a visually distinct ellipsis and an intermittent emoji (e.g., "pointing finger")
    brief += ' <strong class="ellipsis">...</strong> <span class="emoji-pointer">👉</span>'

    text_container = (
        f'<div id="{element_id}" class="ancillary-container">'
        f'<p style="text-align: justify; margin: 0;">{brief}'
    )

    style_block = (
        f"#{element_id} {{ cursor: pointer; }}\n"  # Cursor change
        f".ellipsis {{ color: #555; font-weight: bold; font-size: 1.1em; }}\n"  # Noticeable ellipsis
        f".emoji-pointer {{ font-size: 1.3em; animation: emoji-pulse 1.5s infinite; vertical-align: middle; }}\n"  # Pointer emoji animation
        f"@keyframes emoji-pulse {{\n"
        f"  0% {{ transform: scale(1); }}\n"
        f"  50% {{ transform: scale(1.5); }}\n"
        f"  100% {{ transform: scale(1); }}\n"
        f"}}\n"
    )

    if details:
        text_container += f' <span class="{element_id}-hidden">{details}</span>'
        style_block += (
            f".{element_id}-hidden {{"
            f" display: inline-block; opacity: 0; max-width: 0px; max-height: 0px; overflow: hidden;"
            f" transition: opacity 0.3s ease-in-out 0.2s, max-width 0.4s ease-out, max-height 0.4s ease-out; }}\n"
            f"#{element_id}:hover .{element_id}-hidden {{"
            f" opacity: 1; max-width: 100%; max-height: 400px; }}\n"
            f"#{element_id}:hover .emoji-pointer {{ opacity: 0; }}\n"  # Hide emoji on hover
        )

    return text_container, style_block


