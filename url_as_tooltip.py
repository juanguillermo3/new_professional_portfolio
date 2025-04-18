import requests
from bs4 import BeautifulSoup
import streamlit as st

def fetch_url_metadata(url):
    """Private method to fetch OG metadata from the URL"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract OG metadata
        metadata = {
            'og_title': soup.find('meta', property='og:title'),
            'og_description': soup.find('meta', property='og:description'),
            'og_image': soup.find('meta', property='og:image'),
            'og_url': soup.find('meta', property='og:url')
        }
        
        # Extract content or default to empty strings if not available
        return {
            'title': metadata['og_title']['content'] if metadata['og_title'] else '',
            'description': metadata['og_description']['content'] if metadata['og_description'] else '',
            'image': metadata['og_image']['content'] if metadata['og_image'] else None,
            'url': metadata['og_url']['content'] if metadata['og_url'] else url  # Use the URL as fallback
        }
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return {
            'title': 'Unknown Title',
            'description': 'No description available.',
            'image': None,
            'url': url
        }

import streamlit as st
import uuid

def render_tooltip(visible_text, url):
    """Render inline span with a fixed-position tooltip preview on hover."""

    metadata = fetch_url_metadata(url)

    title = metadata.get("title", "")
    description = metadata.get("description", "")
    image = metadata.get("image") or "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
    final_url = metadata.get("url", url)

    tooltip_id = f"tooltip_{uuid.uuid4().hex[:8]}"

    html = f"""
    <style>
    .tooltip-wrapper {{
        position: relative;
        display: inline-block;
        cursor: pointer;
    }}
    .tooltip-box {{
        visibility: visible;
        width: 320px;
        background-color: #fff;
        color: #333;
        text-align: left;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.15);
        position: absolute;
        top: 25px;
        left: 0;
        z-index: 999;
        font-family: Arial, sans-serif;
    }}
    .tooltip-box img {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 10px;
    }}
    .tooltip-box a {{
        color: #1a73e8;
        font-weight: bold;
        text-decoration: none;
    }}
    </style>

    <span class="tooltip-wrapper" id="{tooltip_id}">
        <span style="text-decoration: underline; color: #1a73e8;">{visible_text}</span>
        <div class="tooltip-box">
            <div style="font-size: 16px; font-weight: bold;">{title}</div>
            <div style="margin: 6px 0;">{description}</div>
            <img src="{image}" alt="logo"/>
            <div style="margin-top: 10px;"><a href="{final_url}" target="_blank">Visitar sitio →</a></div>
        </div>
    </span>
    """

    st.markdown(html, unsafe_allow_html=True)


# Example Usage in Streamlit
#url = "https://www.corewoman.org"
#visible_text = "CoreWoman | Brechas de género"

# Call the render_tooltip method to display the text with tooltip
#render_tooltip(visible_text, url)
