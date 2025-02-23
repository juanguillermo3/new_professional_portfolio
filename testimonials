from portfolio_section import PortfolioSection
import streamlit as st

class Testimonials(PortfolioSection):
    """
    A portfolio section to display testimonials from people who have worked with me.
    Testimonials provide insight into collaboration, expertise, and professionalism.
    """

    EARLY_DEVELOPMENT_STAGE = True  # This section is still under development

    def __init__(self, testimonials: list[dict]):
        """
        Initialize the Testimonials section.

        :param testimonials: A list of dictionaries, each containing:
            - "name": The person's name
            - "role": Their role or company
            - "quote": Their testimonial about working with me
        """
        super().__init__(title="Testimonials 💬", description="Feedback from colleagues and clients.")
        self.testimonials = testimonials

    def render(self):
        """Render the testimonials section."""
        self._render_headers()
        self._render_messages()

        for testimonial in self.testimonials:
            with st.expander(f"⭐ {testimonial['name']} - {testimonial['role']}"):
                st.markdown(f"_{testimonial['quote']}_")

# Module-level instance of TestimonialsSection
testimonials = Testimonials(
    testimonials=[
        {"name": "Alice Johnson", "role": "Software Engineer at TechCorp", 
         "quote": "Working with Juan has been an incredible experience. His expertise in AI is remarkable!"},
        {"name": "Michael Smith", "role": "Data Scientist", 
         "quote": "Juan has a strong understanding of recommendation systems. His insights helped improve our project."}
    ]
)


