import secrets
import string


def make_random_password():
    character = string.ascii_letters + string.digits
    password = "".join(secrets.choice(character) for i in range(12))

    return password
