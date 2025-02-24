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
    
    This class allows different sections of the portfolio to inherit a standard structure, 
    including a title, a horizontal separator, and a description with a consistent grayish style. 
    
    Subclasses can extend this functionality by adding specific content while keeping the 
    default layout intact.
    """

    DESCRIPTION_STYLE = "color: gray;"
    EARLY_DEVELOPMENT_STAGE = True  # Override this in subclasses if the section is complete
    DATA_VERIFIED = False  # Controls both the mocked data message and the verified badge
    
    def __init__(self, title: str, description: str):
        """
        Initialize the portfolio section with a title and description.

        :param title: The section title.
        :param description: The section description.
        """
        self.title = title
        self.description = description

    @staticmethod
    def _render_title_with_badge(title: str, verified: bool):
        """
        Renders the given title with a subtle verified badge below it.

        :param title: The section title to be displayed.
        :param verified: Whether the section data has been verified.
        """
        # Render the title
        st.markdown(f"### {title}", unsafe_allow_html=True)

        # Render a small, well-integrated badge below the title
        if verified:
            st.markdown(
                '<p style="font-size: 0.8em; background: #28a745; color: white; display: inline-block; '
                'padding: 4px 9px; border-radius: 8px; margin-top: -5px; cursor: pointer;" '
                'title="✅ This section has been reviewed for a responsible use of AI-generated content. '
                'It mostly provides accurate information.">'
                '✔ Verified Content</p>',
                unsafe_allow_html=True
            )
            
    def _render_headers(self):
        """Render the section, including the title with a badge, description, and optional messages."""
        self._render_title_with_badge(self.title, self.DATA_VERIFIED)  # Uses class attribute automatically
        st.markdown("---")
        st.markdown(f'<p style="{self.DESCRIPTION_STYLE}">{self.description}</p>', unsafe_allow_html=True)

    def _render_messages(self):
        """Render housekeeping messages, such as warnings for unfinished sections."""
        if self.EARLY_DEVELOPMENT_STAGE:
            st.warning("🚧 This is a new section we are working on. Content may be incomplete.")

        if not self.DATA_VERIFIED:
            st.info("🤖 This section is still being reviewed and may contain AI-generated or placeholder data.")

    def render(self):
        """Render the section, including standard headers and optional messages."""
        self._render_headers()  # Render title, rule, and description
        self._render_messages()  # Render any section-specific messages


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
    
    This class allows different sections of the portfolio to inherit a standard structure, 
    including a title, a horizontal separator, and a description with a consistent grayish style. 
    
    Subclasses can extend this functionality by adding specific content while keeping the 
    default layout intact.
    """

    DESCRIPTION_STYLE = "color: gray;"
    EARLY_DEVELOPMENT_STAGE = True  # Override this in subclasses if the section is complete
    DATA_VERIFIED = False  # Controls both the mocked data message and the verified badge
    
    def __init__(self, title: str, description: str):
        """
        Initialize the portfolio section with a title and description.

        :param title: The section title.
        :param description: The section description.
        """
        self.title = title
        self.description = description

    @staticmethod
    def _render_title_with_badge(title: str, verified: bool):
        """
        Renders the given title with a subtle verified badge below it.

        :param title: The section title to be displayed.
        :param verified: Whether the section data has been verified.
        """
        # Render the title
        st.markdown(f"### {title}", unsafe_allow_html=True)

        # Render a small, well-integrated badge below the title
        if verified:
            st.markdown(
                '<p style="font-size: 0.8em; background: #28a745; color: white; display: inline-block; '
                'padding: 4px 9px; border-radius: 8px; margin-top: -5px; cursor: pointer;" '
                'title="✅ This section has been reviewed for a responsible use of AI-generated content. '
                'It mostly provides accurate information.">'
                '✔ Verified Content</p>',
                unsafe_allow_html=True
            )
            
    def _render_headers(self):
        """Render the section, including the title with a badge, description, and optional messages."""
        self._render_title_with_badge(self.title, self.DATA_VERIFIED)  # Uses class attribute automatically
        st.markdown("---")
        st.markdown(f'<p style="{self.DESCRIPTION_STYLE}">{self.description}</p>', unsafe_allow_html=True)

    def _render_messages(self):
        """Render housekeeping messages, such as warnings for unfinished sections."""
        if self.EARLY_DEVELOPMENT_STAGE:
            st.warning("🚧 This is a new section we are working on. Content may be incomplete.")

        if not self.DATA_VERIFIED:
            st.info("🤖 This section is still being reviewed and may contain AI-generated or placeholder data.")

    def render(self):
        """Render the section, including standard headers and optional messages."""
        self._render_headers()  # Render title, rule, and description
        self._render_messages()  # Render any section-specific messages


import streamlit as st

class PortfolioSection:
    """
    A base class for portfolio sections, providing common rendering behavior.
    """

    DESCRIPTION_STYLE = "color: gray;"
    EARLY_DEVELOPMENT_STAGE = True  # Override this in subclasses if the section is complete
    DATA_VERIFIED = False  # Controls both the mocked data message and the verified badge

    def __init__(self, title: str, description: str):
        """
        Initialize the portfolio section with a title and description.
        """
        self.title = title
        self.description = description

    @staticmethod
    def _render_title_with_badges(
        title: str, 
        verified: bool = DATA_VERIFIED, 
        early_dev: bool = EARLY_DEVELOPMENT_STAGE, 
        ai_content: bool = not DATA_VERIFIED, 
        spacing: int = 10
    ):
        """
        Renders the given title with a row of badges below it.
        """
        st.markdown(f"### {title}", unsafe_allow_html=True)

        badges = []
        if verified:
            badges.append(
                '<p style="font-size: 0.8em; background: #28a745; color: white; display: inline-block; '
                'padding: 4px 9px; border-radius: 8px; cursor: pointer;"
                'title="✅ This section has been reviewed for a responsible use of AI-generated content. '
                'It mostly provides accurate information.">
                ✔ Verified Content</p>'
            )
        if early_dev:
            badges.append(
                '<p style="font-size: 0.8em; background: #ffc107; color: black; display: inline-block; '
                'padding: 4px 9px; border-radius: 8px; cursor: pointer;"
                'title="🚧 This section is new, and we are working on delivering its content.">
                🚧 Early Development</p>'
            )
        if ai_content:
            badges.append(
                '<p style="font-size: 0.8em; background: #17a2b8; color: white; display: inline-block; '
                'padding: 4px 9px; border-radius: 8px; cursor: pointer;"
                'title="🤖 This section may be using AI-generated content as placeholder data.">
                🤖 AI Content</p>'
            )
        
        if badges:
            st.markdown(
                f'<div style="display: flex; gap: {spacing}px; margin-top: -5px;">' + "".join(badges) + "</div>",
                unsafe_allow_html=True
            )
    
    def _render_headers(self):
        """Render the section title and associated badges."""
        self._render_title_with_badges(
            self.title, 
            verified=self.DATA_VERIFIED, 
            early_dev=self.EARLY_DEVELOPMENT_STAGE, 
            ai_content=not self.DATA_VERIFIED
        )
        st.markdown("---")
        st.markdown(f'<p style="{self.DESCRIPTION_STYLE}">{self.description}</p>', unsafe_allow_html=True)

    def _render_messages(self):
        """Render housekeeping messages, now replaced by badges."""
        if self.EARLY_DEVELOPMENT_STAGE:
            st.warning("🚧 This is a new section we are working on. Content may be incomplete.")
        if not self.DATA_VERIFIED:
            st.info("🤖 This section is still being reviewed and may contain AI-generated or placeholder data.")
    
    def render(self):
        """Render the section, now using badges for information."""
        self._render_headers()
        # self._render_messages()  # Commented out in favor of badges
