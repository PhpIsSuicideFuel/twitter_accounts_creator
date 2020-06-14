import secrets
import string

symbols = string.ascii_letters + string.digits


def generate_password():
    return ''.join(secrets.choice(symbols) for _ in range(15))


def generate_username():
    raise NotImplementedError
