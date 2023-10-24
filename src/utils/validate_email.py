def validate_email(email: str):
    try:
        splitted_email = email.split('@')
        splitted_domain = splitted_email[1].split('.')
        if (
            len(splitted_email[0]) < 2
            or len(splitted_domain[0]) < 2
            or len(splitted_domain[1]) < 2
        ):
            raise ValueError()
    except Exception:
        raise ValueError('Wrong email')
