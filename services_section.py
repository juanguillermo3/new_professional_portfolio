import streamlit as st
from front_end_for_recommended_content import html_for_item_data

class ServicesSection:
    SERVICE_LOGIC = """
    💳 The services I offer are designed to help you tackle complex business challenges.
    Each service focuses on delivering high-impact solutions, from expert consulting to data-driven insights.
    We use advanced tools and methodologies to ensure the highest quality results tailored to your needs.
    """

    def __init__(self, services):
        """
        Initialize the ServicesSection with a list of service dictionaries.

        Parameters:
        - services (list of dict): Each dict should contain:
            - "title" (str): The service title.
            - "description" (str): A brief service description.
            - "image" (str): URL to an image representing the service.
            - "highlighted_content" (bool, optional): Marks outstanding services.
        """
        self.services = services

    def render(self):
        """Render the services section using Streamlit."""
        st.subheader("Service Lines 🛠️")
        st.markdown("---")
        st.markdown(
            '<p style="color: gray;">Here are the key services I provide to my clients. '
            'Hover over the titles for more information.</p>',
            unsafe_allow_html=True
        )
        
        # Display the SERVICE_LOGIC string for section-level context
        st.markdown(self.SERVICE_LOGIC, unsafe_allow_html=True)
        
        # Space separator
        st.markdown("<br>", unsafe_allow_html=True)

        # Render services
        services_area = st.container()
        with services_area:
            service_cols = st.columns(3)
            for i, service in enumerate(self.services):
                with service_cols[i % 3]:
                    # Generate HTML using the shared item data structure
                    service_html = html_for_item_data(service)
                    st.markdown(service_html, unsafe_allow_html=True)

# Instantiation Example
services = ServicesSection(
    services=[
        {
            "title": "Consulting",
            "description": "Expert advice to help you grow your business.",
            "image": "https://via.placeholder.com/150",
            "highlighted_content": True  # Marked as outstanding
        },
        {
            "title": "Data Analysis",
            "description": "In-depth analysis of your business data to drive decisions.",
            "image": "https://via.placeholder.com/150"
        },
        {
            "title": "Software Development",
            "description": "Building robust and scalable software solutions.",
            "image": "https://via.placeholder.com/150"
        }
    ]
)

# To render the section
services.render()

