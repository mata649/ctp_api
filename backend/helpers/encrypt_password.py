import bcrypt
def encrypt_password(password: str) -> str:
    """Encrypt the provided password.
    -------------------------------------------------------

    Args:
        password (str): A string to encrpyt.

    Returns:
        str: A string with the encrypted password
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return str(hashed_password).split("'")[1]