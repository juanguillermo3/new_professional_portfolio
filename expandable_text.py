import hashlib

def _chunk_texts(detailed_text: str) -> tuple[str, str]:
    """Splits a paragraph into a brief (first sentence) and details (remaining text)."""
    parts = detailed_text.split(".", 1)
    brief = parts[0] + "." if parts else ""
    details = parts[1] if len(parts) > 1 else ""
    return brief, details

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

    offering_html = (
        f'<li id="{element_id}" class="offering-container" style="padding: 8px; '
        f'border-radius: 4px; margin-bottom: 10px;">'
        f'<p style="text-align: justify; margin: 0;">{brief}'
    )

    style_block = ""

    if details:
        offering_html += f' <span class="{element_id}-hidden">{details}</span>'
        style_block = (
            f".{element_id}-hidden {{"
            f" display: inline-block; opacity: 0; max-width: 0px; max-height: 0px; overflow: hidden;"
            f" transition: opacity 0.3s ease-in-out 0.2s, max-width 0.4s ease-out, max-height 0.4s ease-out; }}\n"
            f"#{element_id}:hover .{element_id}-hidden {{"
            f" opacity: 1; max-width: 100%; max-height: 100px; }}\n"
        )

    return offering_html, style_block
