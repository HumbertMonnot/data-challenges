# pylint: disable=missing-docstring

import os

def start(args = None):
    """returns the right message"""
    cle = 'flask_env'
    valeur = os.getenv(cle.upper())
    if args is None and valeur is None:
        return "Starting in production mode..."
    return f"Starting in {valeur} mode..."

if __name__ == "__main__":
    print(start())
