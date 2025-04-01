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
from collections import deque

def expandable_text_html(detailed_text: str) -> tuple[str, str]:
    """
    Generates an HTML snippet with a hover-reveal effect for long text descriptions.
    The reveal will have a "sweep ink" effect where each word fades in with a slight delay.
    
    Returns:
        offering_html (str): The generated HTML structure.
        style_block (str): The required CSS styles.
    """
    brief, details = _chunk_texts(detailed_text)
    
    # Generate a unique element ID using a hash
    element_id = "hover-" + hashlib.md5(detailed_text.encode()).hexdigest()[:8]

    # Append a visually distinct ellipsis
    brief += ' <strong class="ellipsis">...</strong>'
    
    # Tokenize the detailed text (preserving HTML tags)
    tokenized_text = _tokenize_with_html(detailed_text)
    
    # Wrap each word in a span for individual control
    wrapped_words = ''.join([f'<span class="word">{word}</span>' for word in tokenized_text])

    text_container = (
        f'<div id="{element_id}" class="ancillary-container">'
        f'<p style="text-align: justify; margin: 0;">{brief}'
        f' <span class="{element_id}-hidden">{wrapped_words}</span>'
        f'</p></div>'
    )

    style_block = (
        f"#{element_id} {{ cursor: pointer; }}\n"  # Cursor change
        f".ellipsis {{ color: #555; font-weight: bold; font-size: 1.1em; }}\n"  # Noticeable ellipsis
        f".word {{ opacity: 0; display: inline-block; }}\n"  # Initial state of words
    )

    if details:
        style_block += (
            f".{element_id}-hidden {{"
            f" display: inline-block; overflow: hidden; }}\n"
            f"#{element_id}:hover .{element_id}-hidden .word {{"
            f" opacity: 1; transition: opacity 0.4s ease-out; }}\n"
        )

        # Add a delay to each word for the sweep effect
        delay_step = 0.05  # Adjust for speed of sweep effect
        style_block += _generate_word_delays(element_id, tokenized_text, delay_step)

    return text_container, style_block

def _tokenize_with_html(text: str) -> list:
    """
    Tokenizes the text at the word level but ensures HTML tags are treated as single tokens.
    """
    # Regex pattern to capture words and tags separately
    pattern = r'(<[^>]+>|[\w\']+|[^<\s]+)'
    return re.findall(pattern, text)

def _generate_word_delays(element_id: str, tokenized_text: list, delay_step: float) -> str:
    """
    Generates CSS delays for each word to create the ink sweep effect.
    """
    delay_rules = ""
    delay_time = 0

    for i, word in enumerate(tokenized_text):
        if word.strip():  # Ignore empty tokens (spaces, etc.)
            delay_rules += f"#{element_id}:hover .{element_id}-hidden .word:nth-child({i+1}) {{"
            delay_rules += f" transition-delay: {delay_time}s; }}\n"
            delay_time += delay_step

    return delay_rules
