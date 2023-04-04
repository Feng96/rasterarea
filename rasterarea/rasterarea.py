"""Main module."""

import random
import string
import ipyleaflet

def generate_password(length=8):
    """Generate a random password

    Args:
        length (int, optional): _description_. Defaults to 8.

    Returns:
        _type_: _description_
    """
    # Define the set of characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the password
    password = "".join(random.choice(characters) for i in range(length))

    return password


def gnerate_lucky_number(length = 1):
    """Generate your lucky number 

    Args:
        length (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """    
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return int(result_str)


