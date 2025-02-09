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
            # Apply custom styling for the button
            self.apply_custom_button_styles()

            # Button to roll the dice for random service offerings
            if st.button("🎲 Sample Offerings", key="sample_offerings", help="Click to roll for a sample set of services!"):
                self.display_random_services()

            # Display the services grid (start with all or sample if button clicked)
            self.display_services_grid()

    def apply_custom_button_styles(self):
        """Apply casino-style button styling."""
        st.markdown(
            """
            <style>
            div[data-testid="stButton"] > button {
                background-color: #ff5733 !important; /* Red-orange background */
                color: white !important;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                cursor: pointer;
                border-radius: 8px;
                width: 50% !important;
                margin: 10px auto;
                display: block;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); /* Shadow effect for depth */
                transition: background-color 0.3s ease, transform 0.2s ease; /* Smooth transitions */
            }
            div[data-testid="stButton"] > button:hover {
                background-color: #ff8c1a !important; /* Lighter hover color */
                transform: scale(1.05); /* Button "pop" effect */
            }
            div[data-testid="stButton"] > button:active {
                background-color: #cc4b00 !important; /* Darker active color */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    def display_random_services(self):
        """Display a randomized subset of services."""
        random_services = random.sample(self.services, OFFERINGS_SAMPLE_SIZE)
        self.services_to_display = random_services  # Store the selected services in an attribute
    
    def display_services_grid(self):
        """Render the service offerings in a grid."""
        services_area = st.container()
        with services_area:
            service_cols = st.columns(3)
            services_to_render = getattr(self, 'services_to_display', self.services)  # Default to all if no roll happened
            
            for i, service in enumerate(services_to_render):
                with service_cols[i % 3]:
                    # Generate HTML using the shared item data structure
                    service_html = html_for_item_data(service)
                    st.markdown(service_html, unsafe_allow_html=True)
                
                # Add vertical spacing between rows
                if (i + 1) % 3 == 0 and i + 1 != len(services_to_render):
                    st.markdown("<br><br>", unsafe_allow_html=True)  # Adding vertical margin between rows
                    
# To render the section
services = ServicesSection()

