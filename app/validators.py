import re

# from dotenv import load_dotenv
# load_dotenv()
def validate_email(email):
    """
    Validates if the given string is a valid email address.

    Args:
        email (str): The input string to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return bool(email_pattern.match(email))

import re

def validate_phone_number(phone):
    """
    Validates if the given string is a valid 10-digit phone number.

    Args:
        phone (str): The input string to validate.

    Returns:
        bool: True if the phone number is valid, False otherwise.
    """
    phone_pattern = re.compile(r"^\d{10}$")  # Regex pattern for 10-digit phone number
    return bool(phone_pattern.match(phone))

# Example usage:
if __name__=="__main__":
    user_email = "abcemail.com"
    is_valid = validate_email(user_email)
    if is_valid:
        print(f"{user_email} is a valid email address.")
    else:
        print(f"{user_email} is not a valid email address.")
        
    print(validate_phone_number("123-456-7890"))
    # os.chdir("backendwork")
    # print(os.getcwd())
    
    # print(os.environ['APP_PASSWORD'])
    # print(user)

    