import re
from uuid import uuid4
from battle import play, start
from history import save

def trainer_name(text):
    """Check the trainer name"""
    name = text.strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{1,15}", name):
        raise ValueError("Use 2-16 letters, numbers or underscores. Start with a letter")
    return name
 
def begin(name, starter):
    """Save the opening matchup"""
    trainer = rainer_name(name)
    battle = start(starter)
    battle["trainer"] = trainer
    battle["id"] = uuid4().hex
    battle["turn"] = 0
    player, rival = battle["fighters"]
    message = f"{player['name']} faces {rival['name']}"
    save(battle, starter, message)
    return battle, message
