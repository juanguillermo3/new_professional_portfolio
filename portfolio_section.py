"""
title: Portfolio Section
description: An abstraction for the front-end representation of a portfolio section in a web app. 
It provides a default render method that can be overridden and distributes generic behavior to 
portfolio sections, such as housekeeping messages.
"""

import streamlit as st

class PortfolioSection:
    """
    A base class for portfolio sections, providing common rendering behavior.
    """

    DESCRIPTION_STYLE = "color: gray;"
    EARLY_DEVELOPMENT_STAGE = True  # Override this in subclasses if the section is complete
    DATA_VERIFIED = False  # Controls both the mocked data message and the verified badge

    def __init__(self, title: str, description: str, verified: bool = None, early_dev: bool = None, ai_content: bool = None):
        """
        Initialize the portfolio section with a title and description.
        Defaults will be inherited from the class but can be overridden per instance.
        """
        
        super().__init__(
            title=title,
            description=description,
            verified=self.DATA_VERIFIED,  # Use subclass defaults
            early_dev=self.EARLY_DEVELOPMENT_STAGE,
            ai_content=not self.DATA_VERIFIED  # This ensures consistency
        )

        self.verified = self.DATA_VERIFIED if verified is None else verified
        self.early_dev = self.EARLY_DEVELOPMENT_STAGE if early_dev is None else early_dev
        self.ai_content = not self.verified if ai_content is None else ai_content  # AI content is assumed if not verified

    def _render_title_with_badges(self, spacing: int = 10):
        """
        Renders the given title with a row of badges below it.
        Uses instance attributes instead of class attributes.
        """
        st.markdown(f"### {self.title}", unsafe_allow_html=True)

        badges = []
        if self.verified:
            badges.append(
                """
                <p style="font-size: 0.8em; background: #28a745; color: white; display: inline-block; 
                padding: 4px 9px; border-radius: 8px; cursor: pointer;" 
                title="✅ This section has been reviewed for a responsible use of AI-generated content. 
                It mostly provides accurate information.">
                ✔ Verified Content</p>
                """
            )
        if self.early_dev:
            badges.append(
                """
                <p style="font-size: 0.8em; background: #ffc107; color: black; display: inline-block; 
                padding: 4px 9px; border-radius: 8px; cursor: pointer;" 
                title="🚧 This section is new, and we are working on delivering its content.">
                🚧 Early Development</p>
                """
            )
        if self.ai_content:
            badges.append(
                """
                <p style="font-size: 0.8em; background: #17a2b8; color: white; display: inline-block; 
                padding: 4px 9px; border-radius: 8px; cursor: pointer;" 
                title="🤖 This section may be using AI-generated content as placeholder data.">
                🤖 AI Content</p>
                """
            )
        
        if badges:
            st.markdown(
                f'<div style="display: flex; gap: {spacing}px; margin-top: -5px;">' + "".join(badges) + "</div>",
                unsafe_allow_html=True
            )
    
    def _render_headers(self):
        """Render the section title and associated badges."""
        self._render_title_with_badges()
        st.markdown("---")
        st.markdown(f'<p style="{self.DESCRIPTION_STYLE}">{self.description}</p>', unsafe_allow_html=True)

    def _render_messages(self):
        """Render housekeeping messages, now replaced by badges."""
        if self.early_dev:
            st.warning("🚧 This is a new section we are working on. Content may be incomplete.")
        if not self.verified:
            st.info("🤖 This section is still being reviewed and may contain AI-generated or placeholder data.")

    def render(self):
        """Render the section, now using badges for information."""
        self._render_headers()
