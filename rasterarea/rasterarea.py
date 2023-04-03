"""Main module."""

import random
import string

def generate_password(length=8):
    """
    This function generates a random password consisting of lowercase and uppercase letters,
    digits, and special characters.

    :param length: the length of the password to be generated (default is 8)
    :return: a string containing the generated password
    """
    # Define the set of characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the password
    password = "".join(random.choice(characters) for i in range(length))

    return password

# Example usage: generate a password of length 12
password = generate_password(12)
print(password)