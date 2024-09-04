import re


def is_none_empty_or_zero(value):
    if value is None:
        return True

    value = str(value)
    if len(value) == 0:
        return True
    if value == '0':
        return True

    return False


def is_only_numeric(value):
    if value.isnumeric():
        return True
    return False


def is_valid_email(value):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, value):
        return True
    return False


def check_password(password):
    errors = []
    if len(password) < 12:
        errors.append("Password must be at least 12 characters long.")
    # Password must contain at least one uppercase letter.
    elif not re.search("[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    # Password must contain at least one lowercase letter.
    elif not re.search("[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    # Password must contain at least one number
    elif not re.search("[0-9]", password):
        errors.append("Password must contain at least one digit.")
        # Password must contain at least one special character.
    special_characters = re.compile(r"[@_!#$%^&*()<>?/|}{~:]")
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password should contain at least one special character.")
    return errors
