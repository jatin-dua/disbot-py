import random

def get_random_greeting() -> str:
    """Returns a random greeting string"""
    greetings = [
        "Hello",
        "Hi",
        "Hey there",
        "Greetings",
        "Salutations",
        "Howdy"
    ]

    return random.choice(greetings)
