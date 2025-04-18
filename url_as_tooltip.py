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

def render_tooltip(visible_text, url):
    """Renders the text with a tooltip that is always visible next to the text."""
    
    metadata = fetch_url_metadata(url)

    # Fallback image
    image = metadata['image'] or 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png'

    # Core styles
    html = f"""
    <div style="display: flex; align-items: flex-start; gap: 20px; margin: 10px 0;">
        <!-- Trigger Text -->
        <span style="color: #1a73e8; text-decoration: underline; font-weight: 500; font-size: 16px;">
            {visible_text}
        </span>

        <!-- Tooltip Content -->
        <div style="width: 320px; background-color: #ffffff; padding: 12px; border-radius: 10px;
                    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15); font-family: Arial, sans-serif;">
            
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="{image}" alt="Preview image" style="width: 48px; height: 48px; object-fit: cover; border-radius: 8px;">
                <div>
                    <div style="font-weight: bold; color: #202124; font-size: 15px;">{metadata['title'] or 'Untitled'}</div>
                    <div style="color: #5f6368; font-size: 13px; margin-top: 2px;">{metadata['description'] or ''}</div>
                </div>
            </div>

            <div style="margin-top: 10px; text-align: right;">
                <a href="{metadata['url'] or url}" target="_blank" 
                   style="color: #1a73e8; text-decoration: none; font-size: 13px; font-weight: 500;">
                    Visitar enlace →
                </a>
            </div>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

# Example Usage in Streamlit
#url = "https://www.corewoman.org"
#visible_text = "CoreWoman | Brechas de género"

# Call the render_tooltip method to display the text with tooltip
#render_tooltip(visible_text, url)
