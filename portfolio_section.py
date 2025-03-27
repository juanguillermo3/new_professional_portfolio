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

        self.title=title
        self.description=description
        self.verified = self.DATA_VERIFIED if verified is None else verified
        self.early_dev = self.EARLY_DEVELOPMENT_STAGE if early_dev is None else early_dev
        self.ai_content = not self.verified if ai_content is None else ai_content  # AI content is assumed if not verified

    def _render_title_with_badges(self, spacing: int = 10):
        """
        Renders the given title with a row of badges below it.
        Uses instance attributes instead of class attributes.
        """
        st.markdown(f"### {self.title}", unsafe_allow_html=True)

        def _create_badge(text, color, emoji, tooltip):
            return (
                f'<span style="font-size: 0.8em; background: {color}; color: white; '
                f'display: inline-block; padding: 4px 9px; border-radius: 8px; cursor: pointer; '
                f'margin: 0;">'
                f'{emoji} {text}'
                f'</span>'
            )

        badges = []
        if self.verified:
            badges.append(_create_badge("Verified Content", "#28a745", "✔",
                "✅ This section has been reviewed for a responsible use of AI-generated content. It mostly provides accurate information."))
        if self.early_dev:
            badges.append(_create_badge("Early Development", "#ffc107", "🚧",
                "🚧 This section is new, and we are working on delivering its content."))
        if self.ai_content:
            badges.append(_create_badge("AI Content", "#17a2b8", "🤖",
                "🤖 This section may be using AI-generated content as placeholder data."))

        if badges:
            st.markdown(
                f'<div style="display: flex; gap: {spacing}px; margin-top: -5px; align-items: center;">' +
                "".join(badges) +
                "</div>",
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

    def _render_title_with_badges(self, spacing: int = 10):
        """
        Renders the given title with a row of badges below it.
        Uses instance attributes instead of class attributes.
        """
        st.markdown(f"### {self.title}", unsafe_allow_html=True)
        return 
        badge_html_template = """
            <span style="font-size: 0.8em; background: {bg_color}; color: {text_color}; 
            display: inline-block; padding: 4px 9px; border-radius: 8px; cursor: pointer; 
            margin: 0; margin-right: {spacing}px;" title="{tooltip}">
            {emoji} {label}</span>
        """
    
        badges = []
        if self.verified:
            badges.append(badge_html_template.format(
                bg_color="#28a745", text_color="white", spacing=spacing,
                tooltip="✅ This section has been reviewed for a responsible use of AI-generated content. It mostly provides accurate information.",
                emoji="✔", label="Verified Content"
            ))
        
        if self.early_dev:
            badges.append(badge_html_template.format(
                bg_color="#ffc107", text_color="black", spacing=spacing,
                tooltip="🚧 This section is new, and we are working on delivering its content.",
                emoji="🚧", label="Early Development"
            ))
    
        if self.ai_content:
            badges.append(badge_html_template.format(
                bg_color="#17a2b8", text_color="white", spacing=spacing,
                tooltip="🤖 This section may be using AI-generated content as placeholder data.",
                emoji="🤖", label="AI Content"
            ))
    
        if badges:
            full_html = f"""
            <div style="display: flex; flex-wrap: wrap; align-items: center; gap: {spacing}px; margin-top: -5px;">
                {''.join(badges)}
            </div>
            """
            st.markdown(full_html, unsafe_allow_html=True)
