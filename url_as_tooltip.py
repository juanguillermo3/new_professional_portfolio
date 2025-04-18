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
    """Renders the text with a tooltip that displays metadata on hover"""
    
    # Fetch metadata using the private method
    metadata = fetch_url_metadata(url)
    
    # Create the HTML for the tooltip
    tooltip_html = f"""
    <div style="width: 300px; padding: 10px; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; font-size: 14px;">
        <!-- Title -->
        <div style="font-size: 16px; font-weight: bold; color: #333333;">
            {metadata['title'] if metadata['title'] else visible_text}
        </div>
        
        <!-- Description -->
        <div style="margin-top: 5px; color: #555555; line-height: 1.4;">
            {metadata['description']}
        </div>
        
        <!-- Image (Placeholder) -->
        <div style="margin-top: 10px; text-align: center;">
            <img src="{metadata['image'] if metadata['image'] else 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png'}" alt="Logo" style="width: 60px; height: 60px; object-fit: cover; border-radius: 50%;" />
        </div>
        
        <!-- URL -->
        <div style="margin-top: 10px; text-align: center;">
            <a href="{metadata['url']}" target="_blank" style="color: #1a73e8; text-decoration: none; font-weight: bold;">
                Visit Link
            </a>
        </div>
    </div>
    """
    
    # Create the span with the tooltip (title attribute)
    span_html = f'<span style="color: #1a73e8; text-decoration: underline;" title="{metadata["title"]}: {metadata["description"]}">{visible_text}</span>'
    
    # Render everything in Streamlit using markdown
    st.markdown(f"Hover over this text: {span_html}", unsafe_allow_html=True)

# Example Usage in Streamlit
#url = "https://www.corewoman.org"
#visible_text = "CoreWoman | Brechas de género"

# Call the render_tooltip method to display the text with tooltip
#render_tooltip(visible_text, url)
