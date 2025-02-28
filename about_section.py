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

def exceptional_but_subtle_quote(markdown_text: str):
    """
    Render a subtle notable quote:
    - 5% indentation on the left.
    - Very soft shadow effect on bottom and right.
    - No special font styling, blends with the text naturally.
    """
    subtle_style = """
        <div style="
            padding: 10px;
            margin-left: 5%;
            border-left: 3px solid #DDD;
            border-radius: 6px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.05);
        ">
            <p style="margin: 0;">{}</p>
        </div>
    """.format(markdown_text)

    st.markdown(subtle_style, unsafe_allow_html=True)



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
        exceptional_but_subtle_quote(load_key_interest())
        exceptional_but_subtle_quote(load_key_hypothesis())
        exceptional_but_subtle_quote(load_dev_environment())

# Instantiation
about = AboutSection()

