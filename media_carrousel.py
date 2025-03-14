import streamlit as st

def html_for_media_carousel(media_items, index_key="carousel_index"):
    """
    Generates an HTML string for a media carousel using Streamlit session state.

    :param media_items: List of dictionaries with media properties (src, alt).
    :param index_key: Session state key for tracking the carousel index.
    :return: String containing the carousel HTML.
    """
    carousel_id = "media-carousel"

    # Initialize the index in session state if not set
    if index_key not in st.session_state:
        st.session_state[index_key] = 0

    # Generate media slides
    slides_html = "".join([
        f'<div class="carousel-item"><img src="{item["src"]}" alt="{item.get("alt", "Media Image")}"></div>'
        for item in media_items
    ])

    # JavaScript for handling state updates
    js_script = f"""
    <script>
        function moveSlide(step) {{
            let index = {st.session_state[index_key]};
            const totalItems = document.querySelectorAll("#{carousel_id} .carousel-item").length;
            index = (index + step + totalItems) % totalItems;
            document.getElementById("{carousel_id}-track").style.transform = "translateX(-" + (index * 100) + "%)";
            
            // Send the new index back to Streamlit
            fetch('/_st_update_state?key={index_key}&value=' + index);
        }}
    </script>
    """

    # Full carousel HTML
    return f"""
    <div class="carousel-container" id="{carousel_id}">
        <div class="carousel-track" id="{carousel_id}-track">{slides_html}</div>
        <button class="carousel-btn prev" onclick="moveSlide(-1)">&#10094;</button>
        <button class="carousel-btn next" onclick="moveSlide(1)">&#10095;</button>
    </div>

    {js_script}

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
            transform: translateX(-{st.session_state[index_key] * 100}%);
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
dummy_media_list = [
    {"src": "https://archive.org/download/placeholder-image/placeholder-image.jpg", "alt": "Placeholder Image"},
    {"src": "https://media.istockphoto.com/id/1226328537/vector/image-place-holder-with-a-gray-camera-icon.jpg", "alt": "iStock Placeholder"}
]

#st.markdown(html_for_media_carousel(dummy_media_list), unsafe_allow_html=True)

carousel_html = html_for_media_carousel(media_list)
