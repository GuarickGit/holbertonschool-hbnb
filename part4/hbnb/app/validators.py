from email_validator import validate_email, EmailNotValidError


def is_valid_email(email):
    """
    Validates an email address using the email_validator package.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
