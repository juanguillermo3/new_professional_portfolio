import streamlit as st

def media_carousel(media_items, carousel_id="media-carousel"):
    """
    Generates a simple HTML and CSS-based media carousel with navigation.

    :param media_items: List of dictionaries with media properties (src, alt).
    :param carousel_id: Unique ID for the carousel container.
    :return: HTML string for the carousel.
    """
    # Generate carousel slides
    slides_html = "".join([
        f'<input type="radio" name="carousel" id="slide{i}" {"checked" if i == 0 else ""}>'
        f'<div class="carousel-item"><img src="{item["src"]}" alt="{item.get("alt", "Media Image")}"></div>'
        for i, item in enumerate(media_items)
    ])

    # Generate navigation labels
    nav_html = "".join([
        f'<label for="slide{i}" class="nav-btn"></label>'
        for i in range(len(media_items))
    ])

    return f"""
    <div class="carousel-container">
        <div class="carousel-track">
            {slides_html}
        </div>
        <div class="carousel-nav">
            {nav_html}
        </div>
    </div>

    <style>
        .carousel-container {{
            position: relative;
            width: 60%;
            max-width: 600px;
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            text-align: center;
        }}

        .carousel-track {{
            display: flex;
            transition: transform 0.5s ease-in-out;
            width: 100%;
        }}

        .carousel-item {{
            flex: 0 0 100%;
            display: none;
        }}

        .carousel-item img {{
            width: 100%;
            height: auto;
            border-radius: 10px;
        }}

        input[name="carousel"] {{
            display: none;
        }}

        /* Show the selected slide */
        input[name="carousel"]:nth-of-type(1):checked ~ .carousel-track .carousel-item:nth-of-type(1),
        input[name="carousel"]:nth-of-type(2):checked ~ .carousel-track .carousel-item:nth-of-type(2),
        input[name="carousel"]:nth-of-type(3):checked ~ .carousel-track .carousel-item:nth-of-type(3) {{
            display: block;
        }}

        /* Navigation buttons */
        .carousel-nav {{
            margin-top: 10px;
        }}

        .nav-btn {{
            display: inline-block;
            width: 12px;
            height: 12px;
            margin: 0 5px;
            background: gray;
            border-radius: 50%;
            cursor: pointer;
        }}

        .nav-btn:hover {{
            background: black;
        }}

        /* Selected indicator */
        input[name="carousel"]:nth-of-type(1):checked ~ .carousel-nav label:nth-of-type(1),
        input[name="carousel"]:nth-of-type(2):checked ~ .carousel-nav label:nth-of-type(2),
        input[name="carousel"]:nth-of-type(3):checked ~ .carousel-nav label:nth-of-type(3) {{
            background: black;
        }}
    </style>
    """

# Example usage:
media_items = [
    {"src": "https://via.placeholder.com/600x400", "alt": "Image 1"},
    {"src": "https://via.placeholder.com/600x400/FF5733", "alt": "Image 2"},
    {"src": "https://via.placeholder.com/600x400/33FF57", "alt": "Image 3"},
]

st.markdown(media_carousel(media_items), unsafe_allow_html=True)


# Example usage:
dummy_media_list = [
    {"src": "https://archive.org/download/placeholder-image/placeholder-image.jpg", "alt": "Placeholder Image"},
    {"src": "https://media.istockphoto.com/id/1226328537/vector/image-place-holder-with-a-gray-camera-icon.jpg", "alt": "iStock Placeholder"}
]

#st.markdown(html_for_media_carousel(dummy_media_list), unsafe_allow_html=True)

#carousel_html = html_for_media_carousel(media_list)
