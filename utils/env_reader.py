import os
from dotenv import load_dotenv

load_dotenv()

def env(key):
    value = os.getenv(key)
    if value is None:
        raise Exception(f"Missing env key: {key}")
    return value
