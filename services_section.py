import streamlit as st

class ServicesSection:
    def __init__(self, services):
        self.services = services

    def render(self):
        st.subheader("Service Lines 🛠️")
        st.markdown("---")
        st.markdown('<p style="color: gray;">Here are the key services I provide to my clients. Hover over the titles for more information.</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        services_area = st.container()
        with services_area:
            service_cols = st.columns(3)
            for i, service in enumerate(self.services):
                with service_cols[i % 3]:
                    st.markdown(
                        f"""
                        <div style="border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); padding: 10px; text-align: center;">
                            <img src="{service['image']}" alt="{service['title']}" style="border-radius: 10px; width: 100%; height: auto;">
                            <h5>{service['title']}</h5>
                            <p>{service['description']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

# Instantiation
services = ServicesSection(
    services=[
        {"image": "https://via.placeholder.com/150", "title": "Consulting", "description": "Expert advice to help you grow your business."},
        {"image": "https://via.placeholder.com/150", "title": "Data Analysis", "description": "In-depth analysis of your business data to drive decisions."},
        {"image": "https://via.placeholder.com/150", "title": "Software Development", "description": "Building robust and scalable software solutions."},
    ]
)
