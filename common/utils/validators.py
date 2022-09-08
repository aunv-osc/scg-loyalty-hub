from pydantic.networks import email_validator


def validate_email(email: str):
    try:
        email_validator.validate_email(email, check_deliverability=False)
        return True
    except email_validator.EmailNotValidError as e:
        return False