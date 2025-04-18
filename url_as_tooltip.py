import requests
from bs4 import BeautifulSoup
import streamlit as st

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import streamlit as st
import uuid

def fetch_url_metadata(url):
    """Fetch metadata including <title>, favicon, and OG description/url"""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Title from <title> tag
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else ''

        # 2. Logo from <link rel="icon"> or <link rel="shortcut icon">
        icon_link = soup.find('link', rel=lambda value: value and 'icon' in value.lower())
        if icon_link and icon_link.get('href'):
            image = urljoin(url, icon_link['href'])
        else:
            image = None

        # 3. OG Description
        og_description = soup.find('meta', property='og:description')
        description = og_description['content'] if og_description and og_description.get('content') else ''

        # 4. OG Canonical URL fallback
        og_url = soup.find('meta', property='og:url')
        canonical_url = og_url['content'] if og_url and og_url.get('content') else url

        return {
            'title': title,
            'description': description,
            'image': image,
            'url': canonical_url
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
#from your_module import fetch_url_metadata  # Adjust if necessary

def render_tooltip(visible_text, url):
    """Render a span with a hover-activated tooltip containing page metadata."""

    metadata = fetch_url_metadata(url)

    title = metadata.get("title", "")
    description = metadata.get("description", "")
    logo = metadata.get("image") or "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
    final_url = metadata.get("url", url)

    tooltip_id = f"tooltip_{uuid.uuid4().hex[:8]}"

    html = f"""
    <style>
    #{tooltip_id} {{
        position: relative;
        display: inline-block;
        cursor: pointer;
    }}

    #{tooltip_id} .tooltip-box {{
        visibility: hidden;
        opacity: 0;
        width: 360px;
        background-color: #fff;
        color: #333;
        text-align: left;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0px 6px 24px rgba(0, 0, 0, 0.2);
        position: absolute;
        top: 30px;
        left: 0;
        z-index: 999;
        font-family: Arial, sans-serif;
        transition: opacity 0.3s ease-in-out;
    }}

    #{tooltip_id}:hover .tooltip-box {{
        visibility: visible;
        opacity: 1;
    }}

    .tooltip-box .row-title {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 6px;
    }}

    .tooltip-box .row-title img {{
        width: 36px;
        height: 36px;
        border-radius: 8px;
        object-fit: cover;
    }}

    .tooltip-box .row-title a {{
        color: #1a73e8;
        font-weight: bold;
        text-decoration: none;
        font-size: 16px;
    }}

    .tooltip-box .url-display {{
        font-size: 12px;
        color: #888888;
        margin-bottom: 10px;
    }}

    .tooltip-box .hero-img {{
        width: 100%;
        height: auto;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 10px;
    }}

    .tooltip-box .description {{
        font-size: 13px;
        color: #666666;
        line-height: 1.4;
    }}
    </style>

    <span id="{tooltip_id}">
        <span style="text-decoration: underline; color: #1a73e8;">{visible_text}</span>
        <div class="tooltip-box">
            <div class="row-title">
                <img src="{logo}" alt="logo"/>
                <a href="{final_url}" target="_blank">{title or 'Página web'}</a>
            </div>
            <div class="url-display">{final_url}</div>
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png" alt="Main Image" class="hero-img" />
            <div class="description">{description}</div>
        </div>
    </span>
    """

    st.markdown(html, unsafe_allow_html=True)




# Example Usage in Streamlit
#url = "https://www.corewoman.org"
#visible_text = "CoreWoman | Brechas de género"

# Call the render_tooltip method to display the text with tooltip
#render_tooltip(visible_text, url)
