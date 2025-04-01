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

    # Append the continuation emoji
    brief += ' <strong class="ellipsis">▶️</strong>'

    text_container = (
        f'<div id="{element_id}" class="ancillary-container">'
        f'<p style="text-align: justify; margin: 0; display: inline;">{brief}'
    )

    style_block = (
        f"#{element_id} {{ cursor: pointer; }}\n"  # Cursor change
        f".ellipsis {{ color: #555; font-weight: bold; font-size: 1.1em; }}\n"  # Continuation emoji styling
    )

    if details:
        text_container += f' <span class="{element_id}-hidden">{details}</span>'
        style_block += (
            f".{element_id}-hidden {{"
            f" display: none; opacity: 0; max-width: 0px; max-height: 0px; overflow: hidden;"
            f" transition: opacity 0.3s ease-in-out 0.2s, max-width 0.4s ease-out, max-height 0.4s ease-out; }}\n"
            f"#{element_id}:hover .{element_id}-hidden {{"
            f" display: inline; opacity: 1; max-width: none; max-height: 400px; }}\n"  # Vertical expansion
            f"#{element_id}:hover .ellipsis {{ opacity: 0; }}\n"  # Hide emoji when hovered
        )

    return text_container, style_block


