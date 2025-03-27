
import streamlit as st
from PIL import Image

# Load freely available icons
HOME_ICON = "https://img.icons8.com/?size=100&id=hmZnke9jb8oq&format=png&color=000000"
RECSYS_ICON = "https://img.icons8.com/?size=100&id=NaOfOQ3MMYaq&format=png&color=000000"  # Updated icon for emphasis
SERVICES_ICON = "https://cdn-icons-png.flaticon.com/128/3135/3135706.png"


def render_multi_page_navigation():
    # Define Custom CSS for a Frosted Glass Effect Navbar
    st.markdown(
        """
        <style>
            .fixed-navbar {
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 255, 255, 0.1);  /* Transparent background */
                backdrop-filter: blur(4px);  /* Frosted glass effect */
                border: 2px solid rgba(255, 255, 255, 0.9);
                box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.1);
                padding: 10px 20px;
                border-radius: 15px;
                display: flex;
                gap: 20px;
                align-items: center;
            }
            .nav-button {
                background: none;
                border: none;
                cursor: pointer;
            }
            .nav-button img {
                width: 50px;
                height: 50px;
                transition: transform 0.2s ease-in-out;
            }
            .nav-button img:hover {
                transform: scale(1.1);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # **JavaScript to Update the Hidden Input Field**
    st.markdown(
        """
        <script>
            function setSection(section) {
                document.getElementById("selected_section").value = section;
                document.getElementById("section_form").dispatchEvent(new Event("submit"));
            }
        </script>
        """,
        unsafe_allow_html=True,
    )

    # **Hidden Form for Section Selection**
    st.markdown(
        """
        <form id="section_form">
            <input type="hidden" name="selected_section" id="selected_section">
        </form>
        """,
        unsafe_allow_html=True,
    )

    # **Navigation Buttons (Calling JavaScript)**
    st.markdown(
        f"""
        <div class="fixed-navbar">
            <button class="nav-button" onclick="setSection('Home')">
                <img src="{HOME_ICON}" alt="Home">
            </button>
            <button class="nav-button" onclick="setSection('RecSys')">
                <img src="{RECSYS_ICON}" alt="Recommender System">
            </button>
            <button class="nav-button" onclick="setSection('Services&Rates')">
                <img src="{SERVICES_ICON}" alt="Services and Rates">
            </button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # **Retrieve Selected Section in Python**
    query_params = st.experimental_get_query_params()
    selected_section = query_params.get("selected_section", [None])[0]

    if selected_section:
        st.session_state["selected_sections"] = [selected_section]
        st.experimental_rerun()

