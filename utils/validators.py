
import re

def validate_email(email):
    """
    Validates email format using regex.
    Raises ValueError if the email is invalid.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        raise ValueError(f"Invalid email address: {email}")
