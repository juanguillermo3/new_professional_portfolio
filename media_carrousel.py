"""
title: Media Carrousel
description: Raw html implementation of a media carrousel which allows client navigation trough multiple media items.
debrief:
"""

def html_for_media_carousel(media_items):
    """
    Generates an HTML string for a media carousel.

    :param media_items: List of dictionaries with media properties (src, alt).
    :return: String containing the carousel HTML.
    """
    carousel_id = "media-carousel"
    
    # Generate media slides
    slides_html = "".join([
        f'<div class="carousel-item"><img src="{item["src"]}" alt="{item.get("alt", "Media Image")}"></div>'
        for item in media_items
    ])

    # Full carousel HTML
    return f"""
    <div class="carousel-container" id="{carousel_id}">
        <div class="carousel-track">{slides_html}</div>
        <button class="carousel-btn prev" onclick="moveSlide(-1)">&#10094;</button>
        <button class="carousel-btn next" onclick="moveSlide(1)">&#10095;</button>
    </div>

    <script>
        let index = 0;
        const track = document.querySelector("#{carousel_id} .carousel-track");
        const items = document.querySelectorAll("#{carousel_id} .carousel-item");
        const totalItems = items.length;

        function moveSlide(step) {{
            index = (index + step + totalItems) % totalItems;
            track.style.transform = `translateX(-${index * 100}%)`;
        }}
    </script>

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

        .carousel-btn {{
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

        .carousel-btn:hover {{
            background: rgba(0, 0, 0, 0.8);
        }}

        .prev {{ left: 10px; }}
        .next {{ right: 10px; }}
    </style>
    """

# Example usage:
media_list = [
    {"src": "https://archive.org/download/placeholder-image/placeholder-image.jpg", "alt": "Placeholder Image"},
    {"src": "https://media.istockphoto.com/id/1226328537/vector/image-place-holder-with-a-gray-camera-icon.jpg", "alt": "iStock Placeholder"}
]

carousel_html = html_for_media_carousel(media_list)
