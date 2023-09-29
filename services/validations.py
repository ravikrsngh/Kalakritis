import re

# Validate email address
def is_valid_email(email):
    # Regular expression for validating email addresses
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

# Validate phone number
def is_valid_phone_number(phone_number):
    # Regular expression for validating phone numbers with 10 digits, starting with 6, 7, 8, or 9
    phone_pattern = r'^[6-9]\d{9}$'
    return re.match(phone_pattern, phone_number) is not None
