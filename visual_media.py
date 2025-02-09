import streamlit as st
import streamlit.components.v1 as components

def render_item_visual_content(title, description, image_path, width="700px", height="400px"):
    """
    Render the visual content based on the provided metadata with minimal spacing.
    """
    st.markdown(
        f"""
        <style>
            .media-container {{
                width: {width};
                height: {height};
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                background-color: rgba(0, 0, 0, 0.1);
                margin-bottom: 5px; /* Reduce bottom spacing */
            }}
            .media-container img, .media-container video {{
                max-width: 100%;
                max-height: 100%;
                object-fit: contain;
            }}
            .text-container {{
                background-color: rgba(0, 0, 0, 0.4);
                padding: 8px; /* Reduced padding */
                border-radius: 5px;
                color: white;
                width: 100%;
                text-align: center;
                margin-top: 5px; /* Reduce top spacing */
            }}
            .title-text {{
                font-size: 20px;
                font-weight: 500;
                color: #fff;
                text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
                display: inline-block;
            }}
            .description-text {{
                font-size: 14px;
                font-weight: 300;
                color: #ddd;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4);
                display: inline-block;
                margin-top: 2px;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Identify file type
    ext = image_path.split('.')[-1].lower()

    # Media rendering inside a fixed-size div
    if ext in ['jpg', 'jpeg', 'png', 'gif']:
        try:
            st.image(image_path, use_container_width=False)
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")

    elif ext in ['mp4', 'avi']:
        try:
            st.video(image_path)
        except Exception as e:
            st.error(f"Error loading video: {str(e)}")

    elif ext == 'html':
        try:
            with open(image_path, 'r') as file:
                html_content = file.read()
            components.html(html_content, width=int(width.replace("px", "")), height=int(height.replace("px", "")))
        except FileNotFoundError:
            st.error(f"Error: File '{image_path}' not found.")
        except Exception as e:
            st.error(f"Error loading HTML content: {str(e)}")

    else:
        st.error(f"Unsupported media type: {ext}")

    # Render the text section with minimal spacing
    st.markdown(
        f"""
        <div class="text-container">
            <div class="title-text">{title}</div><br>
            <div class="description-text">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
