import streamlit as st
from portfolio_section import PortfolioSection
from about_section_data_loader import load_general_info, load_key_interest, load_key_hypothesis, load_dev_environment
from about_section_data_loader import (
    load_general_info, 
    load_key_interest, 
    load_key_hypothesis, 
    load_dev_environment
)

import streamlit as st

def exceptional_quote(markdown_text: str):
    """
    Render a notable quote with a distinctive styling:
    - 5% indentation on the left.
    - Rounded borders.
    - Shadow effect on bottom and right for depth.
    """
    quote_style = """
        <div style="
            padding: 15px;
            margin-left: 5%;
            border-left: 4px solid #FFD700;
            border-radius: 10px;
            background-color: rgba(255, 255, 204, 0.2);
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
        ">
            <p style="font-style: italic; font-size: 1.1em; margin: 0;">{}</p>
        </div>
    """.format(markdown_text)

    st.markdown(quote_style, unsafe_allow_html=True)


class AboutSection(PortfolioSection):

    EARLY_DEVELOPMENT_STAGE = False  # Override class defaults for this section
    DATA_VERIFIED = True  

    def __init__(self):
        """
        Ensure AboutSection inherits and overrides class-level defaults.
        """
        super().__init__(
            title="About this portfolio 💡",
            description=load_general_info(),
            verified=self.DATA_VERIFIED,  # Use subclass defaults
            early_dev=self.EARLY_DEVELOPMENT_STAGE,
            ai_content=not self.DATA_VERIFIED  # This ensures consistency
        )

    def render(self):
        """Render the about section with notable quotes."""
        self._render_headers()
        exceptional_quote(load_key_interest())
        exceptional_quote(load_key_hypothesis())
        exceptional_quote(load_dev_environment())

# Instantiation
about = AboutSection()

