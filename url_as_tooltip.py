import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def extract_all_metadata(url):
    """Fetch title, favicon, metadata, og tags, and best-guess hero image (first <img>)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Title
        title = soup.title.string.strip() if soup.title else ''

        # 2. Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else ''

        # 3. Open Graph
        og_data = {
            (tag.get('property') or '').lower(): tag.get('content', '').strip()
            for tag in soup.find_all('meta') if tag.get('property') and tag.get('content')
        }

        # 4. Twitter Card
        twitter_data = {
            (tag.get('name') or '').lower(): tag.get('content', '').strip()
            for tag in soup.find_all('meta') if tag.get('name', '').lower().startswith('twitter:') and tag.get('content')
        }

        # 5. Canonical URL
        canonical_tag = soup.find('link', rel='canonical')
        canonical_url = canonical_tag['href'].strip() if canonical_tag and canonical_tag.get('href') else ''

        # 6. Icon (favicon)
        icon_link = soup.find('link', rel=lambda val: val and 'icon' in val.lower())
        icon_url = urljoin(url, icon_link['href']) if icon_link and icon_link.get('href') else None

        # Apple fallback
        apple_icon = soup.find('link', rel='apple-touch-icon')
        if not icon_url and apple_icon and apple_icon.get('href'):
            icon_url = urljoin(url, apple_icon['href'])

        # 7. Preview image
        preview_image = og_data.get('og:image') or twitter_data.get('twitter:image')

        # 8. Hero image: first <img> with a valid-looking src
        valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        blacklist_keywords = ('blank', 'spacer', 'pixel', 'loader', 'placeholder')

        hero_image = None
        for tag in soup.find_all("img", src=True):
            src = tag['src'].lower()
            parsed_path = urlparse(src).path
            ext = os.path.splitext(parsed_path)[1]

            if ext in valid_extensions and not any(keyword in src for keyword in blacklist_keywords):
                hero_image = urljoin(url, tag['src'])
                break

        return {
            'title': og_data.get('og:title') or twitter_data.get('twitter:title') or title,
            'description': og_data.get('og:description') or twitter_data.get('twitter:description') or meta_description,
            'image': preview_image,
            'hero_image': hero_image,
            'icon': icon_url,
            'url': og_data.get('og:url') or canonical_url or url
        }

    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return {
            'title': 'Unknown Title',
            'description': 'No description available.',
            'image': None,
            'hero_image': None,
            'icon': None,
            'url': url
        }



import streamlit as st
import uuid

def render_tooltip(visible_text, url):
    """Render a span with a hover-activated tooltip containing page metadata."""
    metadata = extract_all_metadata(url)

    title = metadata.get("title", "")
    description = metadata.get("description", "")
    logo = metadata.get("icon") or "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
    hero = metadata.get("hero_image")  # No default
    final_url = metadata.get("url", url)

    tooltip_id = f"tooltip_{uuid.uuid4().hex[:8]}"

    hero_img_html = f'<img src="{hero}" alt="Main Image" class="hero-img" />' if hero else ""

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
            {hero_img_html}
            <div class="description">{description}</div>
        </div>
    </span>
    """

    st.markdown(html, unsafe_allow_html=True)


def _url_as_tooltip_html(visible_text, url):
    """Return the HTML string for a tooltip with embedded metadata from a URL."""
    metadata = extract_all_metadata(url)

    title = metadata.get("title", "")
    description = metadata.get("description", "")
    logo = metadata.get("icon") or "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
    hero = metadata.get("hero_image")
    final_url = metadata.get("url", url)

    tooltip_id = f"tooltip_{uuid.uuid4().hex[:8]}"
    hero_img_html = f'<img src="{hero}" alt="Main Image" class="hero-img" />' if hero else ""

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
            {hero_img_html}
            <div class="description">{description}</div>
        </div>
    </span>
    """
    return html


def render_tooltip(visible_text, url):
    """Render the tooltip using Streamlit markdown."""
    html = _url_as_tooltip_html(visible_text, url)
    
# Example Usage in Streamlit
#url = "https://www.corewoman.org"
#visible_text = "CoreWoman | Brechas de género"

# Call the render_tooltip method to display the text with tooltip
#render_tooltip(visible_text, url)
