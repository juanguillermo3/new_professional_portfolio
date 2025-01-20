# cv_data_loader.py
import json

def experience_items():
    """
    Fetches or generates a list of work experience items.
    Can be extended to fetch from a file, API, or database.
    """
    return [
        {
            'title': 'Software Developer',
            'company': 'Tech Solutions Inc.',
            'description': 'Developed and maintained software solutions for various clients, focusing on full-stack development and optimization.',
            'date_range': 'January 2020 - Present'
        },
        {
            'title': 'Data Scientist',
            'company': 'Data Insights Ltd.',
            'description': 'Applied machine learning techniques to predict consumer behavior, significantly increasing forecast accuracy.',
            'date_range': 'June 2018 - December 2019'
        }
    ]

def education_items():
    """
    Fetches or generates a list of education items.
    Can be extended to fetch from a file, API, or database.
    """
    return [
        {
            'title': 'B.Sc. Computer Science',
            'institution': 'University of Techville',
            'description': 'Graduated with honors in Computer Science, with a focus on artificial intelligence and software engineering.',
            'date_range': 'September 2014 - June 2018'
        },
        {
            'title': 'M.Sc. Data Science',
            'institution': 'Tech University',
            'description': 'Specialized in machine learning and big data analytics.',
            'date_range': 'September 2018 - June 2020'
        }
    ]
