import re
from uuid import uuid4
from battle import play, start
from history import save

def trainer_name(text):
    """Check the trainer name"""
    name = text.strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{1, 15}", name):
        raise ValueError("Use 2-16 letters, numbers or underscores. Start with a letter")
    return name
