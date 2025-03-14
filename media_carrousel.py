import streamlit as st

def html_for_media_carousel(media_items):
    """
    Generates an HTML string for a simple media carousel with hardcoded inline styles.
    
    :param media_items: List of dictionaries with media properties (src, alt).
    :return: String containing the carousel HTML.
    """
    slides_html = "".join([
        f'<div class="carousel-item"><img src="{item["src"]}" alt="{item.get("alt", "Media Image")}"></div>'
        for item in media_items
    ])

    return f"""
    <div class="carousel-container">
        <div class="carousel-track">{slides_html}</div>
        <button class="prev" onclick="moveSlide(-1)">&#10094;</button>
        <button class="next" onclick="moveSlide(1)">&#10095;</button>
    </div>

    <style>
        .carousel-container {{
            position: relative;
            width: 60%;
            max-width: 600px;
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        }}

        .carousel-track {{
            display: flex;
            transition: transform 0.5s ease-in-out;
        }}

        .carousel-item {{
            min-width: 100%;
        }}

        .carousel-item img {{
            width: 100%;
            height: auto;
            border-radius: 10px;
        }}

        .prev, .next {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0, 0, 0, 0.5);
            color: white;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 18px;
            border-radius: 50%;
        }}

        .prev {{ left: 10px; }}
        .next {{ right: 10px; }}
    </style>
    """



# Example usage:
dummy_media_list = [
    {"src": "https://archive.org/download/placeholder-image/placeholder-image.jpg", "alt": "Placeholder Image"},
    {"src": "https://media.istockphoto.com/id/1226328537/vector/image-place-holder-with-a-gray-camera-icon.jpg", "alt": "iStock Placeholder"}
]

#st.markdown(html_for_media_carousel(dummy_media_list), unsafe_allow_html=True)

#carousel_html = html_for_media_carousel(media_list)
