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


def gnerate_lucky_number(length = 1):
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return int(result_str)