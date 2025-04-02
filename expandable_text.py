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
import hashlib

def expandable_text_html(detailed_text: str, wrap_style: bool = True) -> tuple[str, str]:
    """
    Generates an HTML snippet with a hover-reveal effect for long text descriptions.
    
    Args:
        detailed_text (str): The full text content.
        wrap_style (bool): If True, wraps the styles in <style> tags.

    Returns:
        offering_html (str): The generated HTML structure.
        style_block (str): The required CSS styles, optionally wrapped.
    """
    brief, details = _chunk_texts(detailed_text)
    
    # Generate a unique element ID using a hash
    element_id = "hover-" + hashlib.md5(detailed_text.encode()).hexdigest()[:8]
    
    if details:
        brief += ' <span class="ellipsis">▶️</span>'
    
    text_container = (
        f'<div id="{element_id}" class="ancillary-container">'
        f'<p style="text-align: justify; margin: 0; display: inline;">{brief}'
    )
    
    style_block = (
        f"#{element_id} {{ cursor: pointer; }}\n"
        f".ellipsis {{ color: #555; font-weight: bold; font-size: 1.1em; display: inline-block;\n"
        f" animation: bounceHint 0.67s infinite ease-in-out; }}\n"
        f"@keyframes bounceHint {{\n"
        f"  0% {{ transform: translateY(0); }}\n"
        f"  40% {{ transform: translateY(-4px); }}\n"
        f"  100% {{ transform: translateY(0); }}\n"
        f"}}\n"
    )
    
    if details:
        text_container += f' <span class="{element_id}-hidden">{details}</span>'
        style_block += (
            f".{element_id}-hidden {{\n"
            f" display: none; opacity: 0; max-width: 0px; max-height: 0px; overflow: hidden;\n"
            f" transition: opacity 0.3s ease-in-out 0.2s, max-width 0.4s ease-out, max-height 0.4s ease-out; }}\n"
            f"#{element_id}:hover .{element_id}-hidden {{\n"
            f" display: inline; opacity: 1; max-width: none; max-height: 400px; }}\n"
            f"#{element_id}:hover .ellipsis {{ opacity: 0; display: none; }}\n"
        )
    
    if wrap_style:
        style_block = f"<style>{style_block}</style>"
    
    return text_container, style_block







