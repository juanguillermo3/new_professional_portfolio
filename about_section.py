"""
title: About Section
description: Portfolio section designed to display housekeeping information and important messages. It helps users
             understand the purpose of the web application.
"""

import streamlit as st
from portfolio_section import PortfolioSection
from about_section_data_loader import load_general_info, load_key_interest, load_key_hypothesis, load_dev_environment
from about_section_data_loader import (
    load_general_info, 
    load_key_interest, 
    load_key_hypothesis, 
    load_dev_environment
)
from exceptional_quote import exceptional_but_subtle_quote

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
        exceptional_but_subtle_quote(load_dev_environment())
        exceptional_but_subtle_quote(load_key_hypothesis())


# Instantiation
about = AboutSection()

