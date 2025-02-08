import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class HeroArea:
    def __init__(self, quote, avatar_image: str = None, avatar_caption: str = "", 
                 code_samples: list = None, code_samples_intro: str = "Explore the code samples below:",
                 whatsapp_number: str = None, contact_button_intro: str = "Let's work together. Connect to talk about your specific requirements. I can start working for you almost instantly",
                 professional_offering: str = "Simply put, I can develop application code for analytics applications at any stage of the ML/Data Analysis development workflow. I offer several key differentiators compared to typical data analysts: expertise in developing high-performance predictive analytics (Artificial Intelligence, Machine Learning, Genetic Optimization, Ensemble Models, Forecasting models); full commitment to research modern information tools for data analytics (Python, R, Stata, Airflow, Spark, SQL, Bash scripting, Cloud computing, GPT, SQLAlchemy, APIs, development frameworks, Git, and more); strong automation capabilities in complex empirical environments with multiple sources, schemas, data types, and mixes of structured/unstructured data; robust algorithm and application development skills in Python, including libraries like Requests, Selenium, Airflow, Pandas, Scikit-Learn, TensorFlow, Plotly, Flask, and Dash, as well as logging systems and object-oriented programming; knowledge of formal software development topics (architectural and design patterns, development methodologies, distributed systems, computing resources); and a very efficient development workflow supported by technologies like GPT.",
                 detailed_offering: str ="This is amore detailed offering"
                ):
        """
        Initialize the HeroArea class with a focus on a quote-styled main statement.
        :param quote: Main statement or quote to display as a single string or list of strings (paragraphs).
        :param avatar_image: File name of the avatar image to display.
        :param avatar_caption: Caption for the avatar image.
        :param code_samples: List of dictionaries with 'title' and 'url' for code sample links.
        :param code_samples_intro: Introductory text to display above the code samples.
        :param whatsapp_number: WhatsApp number for contact (optional). If None, it will be fetched from .env.
        :param contact_button_intro: Introductory text to display above the WhatsApp contact button.
        :param professional_offering: Key professional offering to display inside the expandable content section.
        """
        self.quote = quote if isinstance(quote, list) else [quote]
        self.avatar_image = avatar_image
        self.avatar_caption = avatar_caption
        self.code_samples = code_samples if code_samples is not None else [
            {"title": "Genetic Algorithms for forecasting app sales", "url": "https://colab.research.google.com/drive/1QKFY5zfiRkUUPrnhlsOrtRlqGJ14oFf3#scrollTo=sxBOaWZ9uabz"},
            {"title": "Ensemble models to automate hirings from Human Resources", "url": "https://colab.research.google.com/drive/1sPdB-uoOEdw2xIKPQCx1aGp5QUuu1ooK#scrollTo=_Ycax1ucXvAO"}
        ]
        self.code_samples_intro = code_samples_intro
        self.whatsapp_number = whatsapp_number or os.getenv("WHATSAPP_NUMBER")
        self.contact_button_intro = contact_button_intro
        self.professional_offering = professional_offering
        self.detailed_offering=detailed_offering

    def render_code_samples(self):
        """
        Render code sample buttons as GitHub-styled buttons with an introductory text.
        """
        st.markdown(f'<p class="code-samples-intro">{self.code_samples_intro}</p>', unsafe_allow_html=True)
        
        # Create a grid layout for the buttons
        st.markdown("<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px;'>", unsafe_allow_html=True)
        
        for sample in self.code_samples:
            st.markdown(f"""
            <a href="{sample['url']}" target="_blank">
                <button style="background-color: #24292f; color: white; border: 1px solid white; padding: 10px 20px; font-size: 14px; border-radius: 5px; text-align: center; width: 100%;">
                    {sample['title']}
                </button>
            </a>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    def render_contact_button(self):
        """
        Render a single WhatsApp contact button to facilitate first contact via WhatsApp.
        """
        if not self.whatsapp_number:
            st.warning("WhatsApp number is not available.")
            return

        # Display contact button intro
        st.markdown(f'<p class="contact-button-intro">{self.contact_button_intro}</p>', unsafe_allow_html=True)
        
        # WhatsApp button styled similarly to code sample buttons
        button_url = f"https://wa.me/{self.whatsapp_number}?text=Hi,%20I%27d%20like%20to%20get%20in%20touch!"
        
        st.markdown(f"""
        <a href="{button_url}" target="_blank">
            <button style="background-color: #25d366; color: white; border: 1px solid white; padding: 10px 20px; font-size: 14px; border-radius: 5px; text-align: center; width: 100%;">
                Contact Me on WhatsApp
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    def render(self):
        """
        Render the Hero area in Streamlit with the main content always visible
        and the code samples + contact button inside expandable content.
        """
        # Two-column layout for quote and avatar
        col1, col2 = st.columns([2, 1])
    
        # Render the quote (always visible)
        with col1:
            st.markdown("""<style>
            .hero-quote {
                font-style: italic;
                font-size: 1.5em;
                line-height: 1.8;
                margin: 0 auto;
                max-width: 800px;
                color: #333333;
                text-align: justify;
                padding-bottom: 20px;
            }
            .hero-avatar-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            </style>""", unsafe_allow_html=True)
    
            # Render each paragraph separately in the quote
            for paragraph in self.quote:
                st.markdown(f'<p class="hero-quote">{paragraph}</p>', unsafe_allow_html=True)
    
        # Render the avatar with caption (always visible)
        if self.avatar_image:
            with col2:
                st.markdown('<div class="hero-avatar-container">', unsafe_allow_html=True)
                st.image(f"assets/{self.avatar_image}", caption=self.avatar_caption, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
        # Create a container for the state toggle
        expander_label = "Explore more (details)"  # Label for closed expander
        with st.expander(expander_label, expanded=True):  # Make the expander open by default
            # Add a dynamic label depending on whether the expander is open or closed
            if st.session_state.get("expander_open", False):
                expander_label = "Explore more (less details)"
                st.session_state.expander_open = False
            else:
                expander_label = "Explore more (details)"
                st.session_state.expander_open = True
    
            # Render the 5+1 key differentials section
            st.markdown(self.detailed_offering)
    
            # Render the code samples (hidden by default)
            self.render_code_samples()
    
        # Render the contact button (hidden by default)
        self.render_contact_button()

    


# Example data for HeroArea with multiple paragraphs in the quote and code sample links
quote = [
    "Modern data analysis requires engaging with substantial software, such as data gathering and information processing applications. "
    "Moreover, software automation is key to distributing inferences from statistical analysis, such as insights from econometric analysis "
    "or predictions from machine learning models. Bottom line, I recognize the tight dependencies between data analysis and software development, "
    "hence my effort to serve both within a unified framework."
    "",
    "I am Juan Guillermo. I am a professional economist. I have made a living developing data analysis and application "
    "development scripts. My larger professional project aims for a holistic vision, interconnecting all the technology for modern data analysis, "
    "comprising data mining and artificial intelligence models, algorithms, workflows, and information tools."
]

hero_caption = "God told me I could either be good-looking or an excellent worker."

detailed_offering="""
              ### (5+1) Key Differentials of My Professional Offering
            
            - **High-Performance Predictive Analytics**: I research and implement techniques for regression, classification, and forecasting use cases, 
              with applications ranging from macroeconomic and financial forecasting to microdata predictions in various systems.
            - **Software for Inference Distribution**: I develop applications (batch scripts, APIs, dashboards, web applications) to distribute insights 
              and predictions across corporate environments.
            - **Data Transformation Expertise**: As my former boss Susana Martinez Restrepo said, "I can perform data miracles." This refers to my 
              ability to clean and organize datasets from complex, multi-source environments for research and model development.
            - **Holistic Understanding of Modern Tooling**: I integrate tools and technologies for modern data analysis, committing to research the 
              unique purposes of each tool and efficiently write workflows around them using GPT.
                - *Excellence Tier* (I know the code line by heart): Python, R Studio, Stata, GPT.
                - *Proficiency Tier*: Airflow, SQL, Spark, Bash scripting.
                - *Currently Learning*: Docker, Kubernetes, GitHub, Big Data Cloud tools, SQLAlchemy, Django.
            - **AI & LLM Disruption in Software Development**: I prepare myself by means of self-learning for the disruption of Artificial Intelligence in software development and the rise of LLM-powered applications.
            - **Bonus: Rigorous Economic Mindset**: As an economist, I approach data analysis with a focus on causal reasoning, marginal effects, and 
              counterfactual analysis.
              """
            

# Instantiate and render HeroArea with code samples
hero = HeroArea(
quote=quote, 
avatar_image="jg_pick.jpg", 
avatar_caption=hero_caption,  
code_samples_intro="As an easy entry-point to my work, you can check these selected code samples from my ML consultancies:",
whatsapp_number="573053658650",
detailed_offering=detailed_offering
)
#hero.render()





