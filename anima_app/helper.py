import secrets


def get_token(length=8):
    return secrets.token_hex(length)