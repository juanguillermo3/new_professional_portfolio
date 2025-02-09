import random
import streamlit as st
import os
from dotenv import load_dotenv
from front_end_for_recommended_content import html_for_item_data
from services_data_loader import load_service_items

# Load environment variables
load_dotenv()

# Default OFFERINGS_SAMPLE_SIZE if not set in .env
OFFERINGS_SAMPLE_SIZE = int(os.getenv('OFFERINGS_SAMPLE_SIZE', 6))

# Default hourly rate and monthly compensation
DEFAULT_HOURLY_RATE = 17
DEFAULT_MONTHLY_COMPENSATION = 1500

class ServicesSection:
    SERVICE_LOGIC = """
    💳 The services I offer are designed to help you tackle complex business challenges.
    Each service focuses on delivering high-impact solutions, from expert consulting to data-driven insights.
    We use advanced tools and methodologies to ensure the highest quality results tailored to your needs.
    """

    def __init__(self):
        """
        Initialize the ServicesSection by loading the service items.
        """
        self.services = load_service_items()
        self.services_to_display = random.sample(self.services, OFFERINGS_SAMPLE_SIZE)  # Always random sample on init

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
            # Button to roll the dice for random service offerings
            if st.button("🎲 Sample Offerings", key="sample_offerings", help="Click to roll for a sample set of services!"):
                self.display_random_services()

            # Display the services grid (start with a random sample or updated if button clicked)
            self.display_services_grid()

            # Display the Rates and Wages section
            self.display_rates_and_wages()

    def display_random_services(self):
        """Display a randomized subset of services."""
        self.services_to_display = random.sample(self.services, OFFERINGS_SAMPLE_SIZE)

    def display_services_grid(self):
        """Render the service offerings in a grid."""
        services_area = st.container()
        with services_area:
            service_cols = st.columns(3)
            services_to_render = self.services_to_display  # Use the random sample stored in the class
            
            for i, service in enumerate(services_to_render):
                with service_cols[i % 3]:
                    # Generate HTML using the shared item data structure
                    service_html = html_for_item_data(service)
                    st.markdown(service_html, unsafe_allow_html=True)
                
                # Add vertical spacing between rows (after every 3rd item)
                if (i + 1) % 3 == 0 and i + 1 != len(services_to_render):
                    st.markdown("<br><br>", unsafe_allow_html=True)  # Adding vertical margin between rows

    def display_rates_and_wages(self):
        """Display a section with the hourly rate and monthly compensation."""
        st.markdown(
            '<p style="font-size: 16px; font-weight: bold;">Rates and Expected Wages 💰: '
            'I am able to work as freelance or full-time contractor under very flexible arrangements. '
            'I typically deliver my work in advance of payment. Below are some minimal parameters.</p>',
            unsafe_allow_html=True
        )
        
        # Set up the grid layout for hourly rate, monthly compensation
        col1, col2 = st.columns(2)

        # Hourly Rate display
        with col1:
            self.display_info_component("Hourly Rate", f"${DEFAULT_HOURLY_RATE:.2f}", "background-color: #e0e0e0; padding: 10px; border-radius: 5px;")

        # Monthly Compensation display
        with col2:
            self.display_info_component("Monthly Compensation", f"${DEFAULT_MONTHLY_COMPENSATION:.2f}", "background-color: #e0e0e0; padding: 10px; border-radius: 5px;")

    def display_info_component(self, label, value, style):
        """Display a simple info block with label and value."""
        st.markdown(
            f'<div style="{style}"><strong>{label}</strong>: {value}</div>',
            unsafe_allow_html=True
        )

           
# To render the section
services = ServicesSection()

